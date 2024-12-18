#!/usr/bin/env python
# coding: utf-8

'''
Dependencies:
pip install pandas numpy matplotlib scipy requests nrrd voxcell
External dependencies: calculate_density_mm3(), get_all_filenames(), get_csv_filenames(), extract_prefix_from_filenames()

chmod +x script.py

In this code we estimate densities:
- density1: official pipeline step 1
- estimation: we only have access to a subset of the cells
- all_region: whole mouse brain 
- XX slices: MERFISH slices only 53
- average: we don't split sides, but we combine slices for average if a region is crossed by multiple slices
- reconstcords: we use the reconstructed coordinates from Allen (and not CCF or RAW coords)
- voxvol: we estimate the area/volume using voxelised crossection between slice and CCFv3 (done in density0 as cells df)

load_manifest(): Handles the download or local cache access.
preprocess_cell_data(): Combines all preprocessing steps.
prepare_output_directories(): Ensures necessary directories are set up.
process_and_calculate_density(): Loops through each region, calculates density, and writes results.
validate_csv_files(): Ensures integrity of output data.

Execute with: python density1_estimation_all_region_53slices_average_reconstcords_voxvolx.py
'''

import os
import sys
import shutil
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import requests
from scipy.spatial import Delaunay
import nrrd
from voxcell import RegionMap

# Add the helper_functions path
sys.path.append('/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/notebooks/scripts/')

from helper_functions import calculate_density_mm3, get_all_filenames, get_csv_filenames, extract_prefix_from_filenames

# =============================================================================
# Paths and Configuration
# =============================================================================
BASE_DIR = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/'
VERSION = '20231215'
DOWNLOAD_BASE = os.path.join(BASE_DIR, 'releases', VERSION)
USE_LOCAL_CACHE = False


# =============================================================================
# Functions
# =============================================================================
def load_manifest():
    """
    Load manifest either from remote or local cache.
    """
    manifest_path = 'releases/%s/manifest.json' % VERSION
    if not USE_LOCAL_CACHE:
        url = 'https://allen-brain-cell-atlas.s3-us-west-2.amazonaws.com/' + manifest_path
        manifest = json.loads(requests.get(url).text)
    else:
        file = os.path.join(DOWNLOAD_BASE, manifest_path)
        with open(file, 'rb') as f:
            manifest = json.load(f)
    return manifest


def preprocess_cell_data():
    """
    Load and preprocess the cell data to set up the initial DataFrame for analysis.
    """
    manifest = load_manifest()
    view_directory = os.path.join(DOWNLOAD_BASE,
                                  manifest['directory_listing']['MERFISH-C57BL6J-638850-CCF']['directories']['metadata']['relative_path'], 
                                  'views')
    cell_file_path = os.path.join(view_directory, 'cell_metadata_with_parcellation_annotation.csv')
    cell_joined = pd.read_csv(cell_file_path)
    cell_joined.set_index('cell_label', inplace=True)

    # Load voxelized region volume data
    view_directory = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/nmi_scores/'
    voxelized_region_data_path = os.path.join(view_directory, 'cells_in_respective_volumes.csv')
    cells = pd.read_csv(voxelized_region_data_path)
    cells.set_index('cell_label', inplace=True)

    # Filter and merge data
    common_rows = cells.index.intersection(cell_joined.index)
    columns_to_add = ['template_nr', 'parcellation_substructure', 'parcellation_term_name', 'region_id', 'voxel_vol']
    cell_joined = cell_joined.loc[common_rows].merge(cells[columns_to_add], left_index=True, right_index=True, how='left')

    # Drop unnecessary columns
    columns_to_drop = [
        'cluster_alias', 'average_correlation_score', 'feature_matrix_label', 'donor_label',
        'donor_genotype', 'donor_sex', 'neurotransmitter_color', 'class_color',
        'parcellation_organ', 'parcellation_category', 'parcellation_division',
        'parcellation_structure'
    ]
    cell_joined.drop(columns=columns_to_drop, inplace=True)

    # Load extended parcellation annotation
    parcellation_annotation_path = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/parcellation_to_parcellation_term_membership_extend.csv'
    parcellation_annotation = pd.read_csv(parcellation_annotation_path)

    # Filter parcellation annotations
    parcellation_indexes = list(np.unique(cell_joined['parcellation_index']))
    description_of_all_indexes = parcellation_annotation[parcellation_annotation['parcellation_index'].isin(parcellation_indexes)]
    substructure_info = description_of_all_indexes[description_of_all_indexes['parcellation_term_set_name'] == 'substructure']

    return cell_joined, substructure_info


def prepare_output_directories():
    """
    Prepare necessary directories for saving results.
    """
    output_dir_csv = f"{DOWNLOAD_BASE}results/density_calculations/csv"
    output_dir_log = f"{DOWNLOAD_BASE}results/density_calculations/log"
    output_dir_nrrd = f"{DOWNLOAD_BASE}results/density_calculations/nrrd"

    # Remove old directories if they exist
    if os.path.exists(output_dir_csv):
        shutil.rmtree(output_dir_csv)
    if os.path.exists(output_dir_log):
        shutil.rmtree(output_dir_log)

    # Create new directories
    os.makedirs(output_dir_csv, exist_ok=True)
    os.makedirs(output_dir_log, exist_ok=True)
    os.makedirs(output_dir_nrrd, exist_ok=True)

    return output_dir_csv, output_dir_log, output_dir_nrrd


def process_and_calculate_density(cell_joined, substructure_info, output_dir):
    """
    Loop through each region and calculate density.
    """
    volume_single_cube_mm3 = 1e-06  # Volume of a single voxel in mm^3
    all_section_count = len(np.unique(cell_joined['brain_section_label']))

    log_file_path = f"{output_dir}/log/print_log_density1_part.txt"
    with open(log_file_path, "w") as log_file:
        for selected_region in substructure_info['parcellation_term_acronym']:
            cells_in_region = cell_joined[cell_joined['parcellation_substructure_x'] == selected_region]
            nr_of_cells = cells_in_region.shape[0]
            sections = len(np.unique(cells_in_region['brain_section_label']))
            ctype_in_region = len(np.unique(cells_in_region['cluster']))

            print(f"\nCells in {selected_region}: {nr_of_cells} cells, {ctype_in_region} types, {sections} sections",
                  file=log_file)

            # Calculate density
            result_df = calculate_density_mm3(cells_in_region, volume_single_cube_mm3, selected_region)

            if not result_df.empty:
                cluster_as_filename = selected_region.translate(str.maketrans({" ": "", "/": "", "-": ""}))
                result_df.to_csv(os.path.join(output_dir, f"{cluster_as_filename}_density_two_sides.csv"), index=True)
            else:
                print(f"Empty DataFrame for {selected_region}.", file=log_file)


def validate_csv_files(folder_path, unique_prefixes):
    """
    Validate that CSV files are correctly formatted and contain required data.
    """
    filenames = get_all_filenames(folder_path)
    csv_files = get_csv_filenames(folder_path)

    for prefix in unique_prefixes:
        matching_files = [filename for filename in filenames if filename.startswith(prefix)]
        for filename in matching_files:
            try:
                df = pd.read_csv(os.path.join(folder_path, filename), index_col='cluster')
                if df.empty:
                    print(f"{filename}: DataFrame is empty.")
                    continue
                if df.index.name != 'cluster' or 'density_mm3' not in df.columns:
                    print(f"{filename}: Incorrect structure or missing 'density_mm3' column.")
            except Exception as e:
                print(f"Error validating {filename}: {e}")


# =============================================================================
# Main Execution
# =============================================================================
if __name__ == "__main__":
    # Preprocess and load data
    cell_joined, substructure_info = preprocess_cell_data()
    
    # Prepare directories
    output_dir_csv, output_dir_log, output_dir_nrrd = prepare_output_directories()
    
    # Process density calculations
    process_and_calculate_density(cell_joined, substructure_info, output_dir_csv)
    
    # Validate CSV files
    unique_prefixes = extract_prefix_from_filenames(get_csv_filenames(output_dir_csv))
    validate_csv_files(output_dir_csv, unique_prefixes)



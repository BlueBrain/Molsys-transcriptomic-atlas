#!/usr/bin/env python
# coding: utf-8

'''
Dependencies:
pip install pandas numpy pynrrd voxcell
External dependencies: get_all_filenames, get_csv_filenames, extract_prefix_from_filenames, extract_regions_from_column_names, read_and_concat_csv_files_new, combine_rows_and_calculate_average

chmod +x script.py

In this code We create a pickle file fom csv files
- dict of dataframes

Possible atlas versions to choose from: nr 3 is default
# #1
# data_folder = "/gpfs/bbp.cscs.ch/project/proj84/piluso/share/general/warped_augmented_CCFv3/"
# CCFv3_0, _ = nrrd.read(f'{data_folder}annotation_25_2022_CCFv3_0.nrrd')
# #2
# data_folder = "/gpfs/bbp.cscs.ch/data/project/proj62/csaba/atlas/bbp_prod_files/2022/"
# CCFv3_0, _ = nrrd.read(f'{data_folder}annotation_25.nrrd')
# #3
data_folder = "/gpfs/bbp.cscs.ch/project/proj84/piluso/share/general/warped_augmented_CCFv3/"
CCFv3_0, _ = nrrd.read(f'{data_folder}annotation_25_2022_CCFv3a.nrrd')
# CCFv3_0, _ = nrrd.read("/gpfs/bbp.cscs.ch/data/project/proj84/atlas_pipeline_runs/2024-05-15T22:44:26+02:00/annotation_ccfv3_l23split_barrelsplit_validated.nrrd")

Execute with: pdensity1.2_test_total_neuron_count_pickle_create.py
'''

# Import necessary libraries
import pandas as pd
import numpy as np
import re
import pickle
import copy
import os
import nrrd
from voxcell import RegionMap

# Custom imports - Assuming helper_functions are provided in your path
import sys
sys.path.append('/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/notebooks/scripts/')
from helper_functions import (
    get_all_filenames, 
    get_csv_filenames, 
    extract_prefix_from_filenames,
    extract_regions_from_column_names,
    read_and_concat_csv_files_new,
    combine_rows_and_calculate_average
)


# ============================================================
# Set constants
# ============================================================
EDGE_LENGTH_25UM_MM = 25.0 / 1000.0
EDGE_LENGTH_10UM_MM = 10.0 / 1000.0
volume_25_mm3 = round(EDGE_LENGTH_25UM_MM ** 3, 10)
volume_10_mm3 = round(EDGE_LENGTH_10UM_MM ** 3, 10)
save_nrrd_folder = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/density_calculations/nrrd/'


# ============================================================
# Load Parcellation & Substructure Data
# ============================================================
def load_substructure_volumes():
    """Load substructure parcellation data and filter the data."""
    file_path = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/parcellation_to_parcellation_term_membership_extend.csv'
    parcellation_annotation = pd.read_csv(file_path)
    
    # Filter by substructure membership
    parcellation_annotation = parcellation_annotation[parcellation_annotation['parcellation_term_set_name'] == 'substructure']
    print("Number of memberships at substructure level:", len(parcellation_annotation))
    
    # Extract columns of interest
    volumes = parcellation_annotation[['parcellation_label', 'parcellation_index', 'parcellation_term_acronym', 
                                       'parcellation_term_set_name', 'parcellation_term_name', 'voxel_count', 'volume_mm3']]
    return volumes


# ============================================================
# Process NRRD files & Missing number calculations
# ============================================================
def extract_nrrd_files():
    """Retrieve NRRD files and identify missing ones."""
    filenames = get_all_filenames(save_nrrd_folder)
    created_nrrds, nrrd_files_without_extension = get_nrrd_files(save_nrrd_folder)
    
    # Regular expression pattern
    pattern = re.compile(r'(\d{4})')
    existing_numbers = {int(pattern.search(f).group(1)) for f in nrrd_files_without_extension}
    
    # Find missing numbers
    missing_numbers = sorted(set(range(1, 5323)) - existing_numbers)
    print("Missing NRRD numbers:", len(missing_numbers))
    return missing_numbers


# ============================================================
# Process CSV data to compute density
# ============================================================
def process_csv_densities():
    """Read and process density calculations from CSV."""
    folder_path = save_nrrd_folder.replace("nrrd/", "csv/")
    filenames = get_all_filenames(folder_path)
    csv_files = get_csv_filenames(folder_path)
    unique_prefixes = extract_prefix_from_filenames(csv_files)
    
    # Process CSV files & compute densities
    allen_regions = extract_regions_from_column_names(folder_path, csv_files)
    result_dataframes = read_and_concat_csv_files_new(csv_files, unique_prefixes, folder_path)
    result_dataframes = {allen_regions[i]: df for i, (_, df) in enumerate(result_dataframes.items())}
    
    combined_dfs = combine_rows_and_calculate_average(result_dataframes)
    return combined_dfs


# ============================================================
# Map regions to their volumes and calculate total number of cells
# ============================================================
def map_densities_to_volumes(CCF_25_shape, total_cells):
    """Map calculated densities to voxel counts based on region volumes."""
    region_volumes = load_substructure_volumes()
    
    total_cells_mapped = {}
    
    if CCF_25_shape == (528, 320, 456):
        for region, df in total_cells.items():
            label = region_volumes.loc[region_volumes['parcellation_term_acronym'] == region, 'parcellation_label'].values[0]
            id_ = int(label.rsplit('-', 1)[-1])
            volume = np.count_nonzero(CCFv3_0 == id_) * volume_25_mm3
            total_cells_mapped[region] = df['density_mm3'] * volume
    elif CCF_25_shape == (1320, 800, 1140):
        for region, df in total_cells.items():
            label = region_volumes.loc[region_volumes['parcellation_term_acronym'] == region, 'parcellation_label'].values[0]
            id_ = int(label.rsplit('-', 1)[-1])
            volume = np.count_nonzero(CCFv3_0 == id_) * volume_10_mm3
            total_cells_mapped[region] = df['density_mm3'] * volume
            
    return total_cells_mapped


# ============================================================
# Save computed data
# ============================================================
def save_total_cell_data(data_to_save):
    """Save processed data for later use."""
    save_path = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/total_cells.pickle'
    with open(save_path, 'wb') as file:
        pickle.dump(data_to_save, file)
    print(f"Total cell data saved at: {save_path}")


# ============================================================
# Main processing script
# ============================================================
def main():
    print("Starting pipeline...")
    
    # Process CSV files
    densities = process_csv_densities()
    print("Processed densities")
    
    # Map densities into volumetric regions
    mapped_cells = map_densities_to_volumes(CCF_25_shape=(528, 320, 456), total_cells=densities)
    print("Mapped total cells to brain regions")
    
    # Save the processed data
    save_total_cell_data(mapped_cells)
    
    print("Pipeline complete")


if __name__ == "__main__":
    main()


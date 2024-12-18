#!/usr/bin/env python
# coding: utf-8

'''
Dependencies:
pip install pandas numpy voxcell matplotlib scipy
External dependencies: calculate_density_mm3(), get_all_filenames(), get_csv_filenames(), extract_prefix_from_filenames()

chmod +x script.py

In this code we're going to improve region coverage which is already built in the metadata. 
Cerebellar lobes will be split in teir leaf regions (Purkinje, Molecular, Granular layers)
OLF glomerular layer will be created from unassigned regions

Execute with: python density1.1_missing_regions.py
'''

import os
import sys
import pandas as pd
import numpy as np
from voxcell import RegionMap


# Add the path to helper functions
sys.path.append('/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/notebooks/scripts/')
from helper_functions import get_all_filenames, get_csv_filenames, extract_prefix_from_filenames


# ------------------------------
# Load Parcellation Metadata
# ------------------------------
def load_metadata():
    """Load initial cerebellar metadata and annotations."""
    metadata_file = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/parcellation_to_parcellation_term_membership_extend.csv'
    parcellation_annotation = pd.read_csv(metadata_file)
    
    # Load cerebellum-specific cell types
    cb_cells_file = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/MERFISH-C57BL6J-638850-CCF/20231215/views/CB_cells_small.csv'
    cb_cells = pd.read_csv(cb_cells_file)
    cb_cells.set_index('cell_label', inplace=True)
    cb_clusters = np.unique(cb_cells['cluster'])
    
    return parcellation_annotation, cb_cells, cb_clusters


# ------------------------------
# Identify Cell Layers
# ------------------------------
def classify_cell_types(cb_cells):
    """Classify different cell types into Purkinje, molecular, granular, etc."""
    Purkinje_cells = cb_cells[cb_cells['supertype'].str.contains('Purkinje', na=False)]
    purkinjes = np.unique(Purkinje_cells['cluster'])
    
    Bergman_cells = cb_cells[cb_cells['supertype'].str.contains('Bergman', na=False)]
    bergmann_glia = np.unique(Bergman_cells['cluster'])
    
    microglia_cells = cb_cells[cb_cells['supertype'].str.contains('Microglia', na=False)]
    microglia = np.unique(microglia_cells['cluster'])
    
    excitatory_cells = cb_cells[cb_cells['neurotransmitter'].isin(['Glut'])]
    excitatory = np.unique(excitatory_cells['cluster'])
    
    inhibitory_cells = cb_cells[cb_cells['neurotransmitter'].isin(['GABA', 'GABA-Glyc', 'Glut-GABA'])]
    inhibitory = np.unique(inhibitory_cells['cluster'])
    
    inhibitory_exc_golgi_cells = inhibitory_cells[~inhibitory_cells['cluster'].isin([
        '5186 CBX Golgi Gly-Gaba_1', '5187 CBX Golgi Gly-Gaba_1'
    ])]
    inhibitory_exc_golgi = np.unique(inhibitory_exc_golgi_cells['cluster'])

    # Define cell type groups
    l_purkinje_ctypes = [*purkinjes, *bergmann_glia, *microglia]
    l_molecular_ctypes = [ctype for ctype in [*cb_clusters] if ctype not in l_purkinje_ctypes and ctype not in bergmann_glia and ctype not in excitatory]
    l_molecular_ctypes.extend(microglia)

    l_granular_ctypes = [ctype for ctype in [*cb_clusters] if ctype not in l_purkinje_ctypes and ctype not in bergmann_glia and ctype not in inhibitory_exc_golgi]
    l_granular_ctypes.extend(microglia)

    return l_purkinje_ctypes, l_molecular_ctypes, l_granular_ctypes


# ------------------------------
# Filter and Prepare CSV Files
# ------------------------------
def prepare_csv_files(root_folder, crb_keys, l_purkinje_ctypes, l_molecular_ctypes, l_granular_ctypes):
    """Process density data for Purkinje, molecular, and granular layers."""
    csv_folder = os.path.join(root_folder, 'csv/')
    filenames = get_all_filenames(csv_folder)
    csv_filenames = get_csv_filenames(csv_folder)

    # Filter filenames based on keys
    crb_filenames = [filename for filename in csv_filenames if any(filename.startswith(prefix + "_") for prefix in crb_keys)]

    for file in crb_filenames:
        print(file)
        region = file.split('_')[0]
        cb_lobule = pd.read_csv(root_folder + 'csv/' + file, usecols=['cluster', 'density_mm3'])

        # Filter data by layers
        cb_purkinje = cb_lobule[cb_lobule['cluster'].isin(l_purkinje_ctypes)]
        cb_molecular = cb_lobule[cb_lobule['cluster'].isin(l_molecular_ctypes)]
        cb_granular = cb_lobule[cb_lobule['cluster'].isin(l_granular_ctypes)]

        # Rename indexes for clarity
        cb_purkinje.index.name = region + 'purkinjelayer'
        cb_molecular.index.name = region + 'molecularlayer'
        cb_granular.index.name = region + 'granularlayer'

        # Save processed CSVs
        cb_purkinje.to_csv(csv_folder + cb_purkinje.index.name + '_density_two_sides.csv', index=True)
        cb_molecular.to_csv(csv_folder + cb_molecular.index.name + '_density_two_sides.csv', index=True)
        cb_granular.to_csv(csv_folder + cb_granular.index.name + '_density_two_sides.csv', index=True)

        # Rename processed files
        new_file = os.path.splitext(file)[0] + '.bak'
        os.rename(csv_folder + file, csv_folder + new_file)
        print(f"Renamed {file} to {new_file}")


# ------------------------------
# Handle Region Map Queries
# ------------------------------
def load_region_map():
    """Load region map JSON."""
    region_map_path = '/gpfs/bbp.cscs.ch/data/project/proj84/atlas_pipeline_runs/2024-05-15T22:44:26+02:00/hierarchy_ccfv3_l23split_barrelsplit.json'
    region_map = RegionMap.load_json(region_map_path)
    print(region_map.get(507, "name", with_ascendants=False))
    print(region_map.get(212, "name", with_ascendants=False))
    return region_map


# Main Function
def main():
    """Main function to orchestrate execution."""
    parcellation_annotation, cb_cells, cb_clusters = load_metadata()
    l_purkinje_ctypes, l_molecular_ctypes, l_granular_ctypes = classify_cell_types(cb_cells)

    root_folder = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/density_calculations/'
    crb_keys = ['ANcr1', 'ANcr2', 'CBunassigned', 'CENT2', 'CENT3', 'COPY', 'CUL45', 'DEC', 'DN', 'FL', 'FN', 'FOTU', 'IP', 'LING', 'NOD', 'PFL', 'PRM', 'PYR', 'SIM', 'UVU']

    # Exclude irrelevant regions
    items_to_remove = ['arb', 'IP', 'DN', 'FN', 'VeCB', 'CBunassigned']
    crb_keys = [key for key in crb_keys if key not in items_to_remove]

    # Process CSV files
    prepare_csv_files(root_folder, crb_keys, l_purkinje_ctypes, l_molecular_ctypes, l_granular_ctypes)

    # Load Region Map
    region_map = load_region_map()


if __name__ == "__main__":
    main()

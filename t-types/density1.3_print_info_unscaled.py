#!/usr/bin/env python
# coding: utf-8

'''
Dependencies:
pip install pandas numpy voxcell
chmod +x script.py

In this code we calculate total neuron numbers and save it in a txt file

Execute with: density1.3_print_info_unscaled.py
'''
import pickle
import pandas as pd
import json
from voxcell import RegionMap
import numpy as np
import os
import copy
import logging

# Configure logging
logging.basicConfig(filename='neuron_numbers.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Paths
path = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/density_calculations/'
region_map_path = '/gpfs/bbp.cscs.ch/data/project/proj84/atlas_pipeline_runs/2024-05-15T22:44:26+02:00/hierarchy_ccfv3_l23split_barrelsplit.json'
parcellation_file = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/parcellation_to_parcellation_term_membership_extend.csv'
output_missing_regions = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/missing_regions.csv'
meta_path = "/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/WMB-10X/20231215/views/cell_metadata_with_cluster_annotation.csv"

# Load Data
total_cells = pd.read_pickle(f'{path}total_cells.pickle')
region_map = RegionMap.load_json(region_map_path)
parcellation_annotation = pd.read_csv(parcellation_file)
metadata = pd.read_csv(meta_path, dtype={'cell_label': str})
metadata = metadata[['class', 'subclass', 'cluster']]

# Remove unwanted regions
regions = list(total_cells.keys())
unwanted_regions = ['unassigned', 'brain-unassigned']
# Exclude 'unassigned' and 'brain-unassigned' regions to focus on valid data.
regions = [region for region in regions if region not in unwanted_regions]

# Identify missing regions
missing_regions = parcellation_annotation[~parcellation_annotation['parcellation_term_acronym'].isin(regions)]
missing_substructures = missing_regions[missing_regions['parcellation_term_set_name'] == 'substructure']

processed_data = []
for name in missing_substructures['parcellation_term_name'].values:
    try:
        matches = list(region_map.find(name, attr='name', ignore_case=True, with_descendants=True))
        if matches:
            first_match = int(matches[0])
            upstream = region_map.get(first_match, 'name', with_ascendants=True)
            closest = upstream[1]
            processed_data.append({'id': first_match, 'name': name, 'closest_region': closest, 'parent_region': upstream})
        else:
            processed_data.append({'id': None, 'name': name, 'parent_region': None})
    except Exception as e:
        logging.error(f"Error processing name '{name}': {e}")
        processed_data.append({'id': None, 'name': name, 'parent_region': None})

df = pd.DataFrame(processed_data)
df.to_csv(output_missing_regions, index=False)

# Filter region info
region_info = parcellation_annotation[parcellation_annotation['parcellation_term_acronym'].isin(regions)]
duplicates = region_info[region_info.duplicated('parcellation_term_acronym', keep=False)]
substructure_filter = duplicates['parcellation_term_set_name'] == 'substructure'
filtered_region_info = pd.concat([
    region_info[~region_info['parcellation_term_acronym'].isin(duplicates['parcellation_term_acronym'])],
    duplicates[substructure_filter]
]).reset_index(drop=True)

# Area definitions
areas = {
    'isocortex': region_map.find("Isocortex", attr="name", with_descendants=True) |
                 region_map.find("Entorhinal area", attr="name", with_descendants=True) |
                 region_map.find("Piriform area", attr="name", with_descendants=True),
    'cerebellum': region_map.find("Cerebellum", attr="name", with_descendants=True) |
                  region_map.find("arbor vitae", attr="name", with_descendants=True),
    'fiber_tracts': region_map.find("fiber tracts", attr="name", with_descendants=True) |
                    region_map.find("grooves", attr="name", with_descendants=True) |
                    region_map.find("ventricular systems", attr="name", with_descendants=True),
    'hippocampus': region_map.find("Hippocampal region", attr="name", with_descendants=True),
    'thalamus': region_map.find("Thalamus", attr="name", with_descendants=True),
    'wholebrain': region_map.find("root", attr="name", with_descendants=True)
}

# Calculate total cells
for key, value in areas.items():
    keys_to_drop = [region for region in regions if int(region_info.loc[region_info['parcellation_term_acronym'] == region, 'label_numbers'].iloc[0]) not in value]
    total_cells_filtered = {k: v for k, v in total_cells.items() if k not in keys_to_drop}
    concatenated_df = pd.concat(total_cells_filtered.values())
    summed_df = concatenated_df.groupby(concatenated_df.index).sum()
    logging.info(f"The brain area {key} has {summed_df.shape[0]} different cell types")
    logging.info("Total sum of cells: {:,.0f}".format(summed_df['total_cellnumber'].sum()))

# Filter neurons and calculate types
neurontypes = np.unique(metadata[metadata['class'].isin(['01 IT-ET Glut', '02 NP-CT-L6b Glut', '03 OB-CR Glut'])]['cluster'].values)
total_cells_neurons = copy.deepcopy(total_cells)
for key, df in total_cells_neurons.items():
    total_cells_neurons[key] = df[df.index.isin(neurontypes)]

for key, value in areas.items():
    keys_to_drop = [region for region in regions if int(region_info.loc[region_info['parcellation_term_acronym'] == region, 'label_numbers'].iloc[0]) not in value]
    total_cells_filtered = {k: v for k, v in total_cells_neurons.items() if k not in keys_to_drop}
    concatenated_df = pd.concat(total_cells_filtered.values())
    summed_df = concatenated_df.groupby(concatenated_df.index).sum()
    logging.info(f"The brain area {key} has {summed_df.shape[0]} different neuron types")
    logging.info("Total sum of neurons: {:,.0f}".format(summed_df['total_cellnumber'].sum()))

#!/usr/bin/env python
# coding: utf-8

'''
Dependencies:
pip install numpy pandas pynrrd
or pip install -r requirements.txt
chmod +x script.py

This step will scale total densities globally compared to multi-scaling. Thus, this does not deal with cell transplant.

In this code we start after data was created from MERFISH slices and stored as csv and pickle files. 
We examine scaling individual cell groups based on literature: https://www.pnas.org/doi/full/10.1073/pnas.0604911103
- Total cells (M): 108.69 ± 16.25
- Total neurons (M): 70.89 ± 10.41
- CCTX: 17.8 ± 3.4% of neurons (this is not the isocortex)
- CRB: 59.0 ± 5.0% of neurons

    - "Cerebral cortex" 688 = "Cortical plate" 695 + "Cortical subplate" 703
        - "Cerebral nuclei is not part of the cer.ctx)
        - Cerebral cortex is not the Cerebellar cortex (the Cerebellar cortex is part of the Cerebellum)
     
Note, that we cannot scale glia because we don't have information on that. only all non-neuron types number is known.
     
From test_tutorial_cerebellum.ipynb we decided to only scale exc cells (ie granular layer) in the CRB. 

Execute with: python density1.5_scaling.py
'''

import os
import re
import sys
import pickle
import numpy as np
import pandas as pd
from voxcell.nexus.voxelbrain import RegionMap
import multiprocessing as mp
import nrrd

# Append the script path
sys.path.append('/scripts/')

# Import helper functions
from helper_functions import (
    get_all_filenames,
    get_csv_filenames,
    extract_prefix_from_filenames,
    read_and_concat_csv_files_new,
    combine_rows_and_calculate_average,
    create_combined_dataframe
)

# Define constants
TOTAL_CELLS = 108.69 * 1_000_000
TOTAL_NEURONS = 70.89 * 1_000_000
TOTAL_CTX = TOTAL_NEURONS * 17.8 / 100  # 17.8% of total neurons
TOTAL_CRB = TOTAL_NEURONS * 59.0 / 100  # 59% of total neurons
TOTAL_REST = TOTAL_NEURONS * (100 - 59.0 - 17.8) / 100
TOTAL_NONNEURON = TOTAL_CELLS - TOTAL_NEURONS

# Metadata path
META_PATH = "/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/WMB-10X/20231215/views/cell_metadata_with_cluster_annotation.csv"
COLUMNS_TO_READ = ['class', 'subclass', 'cluster']

# Load metadata
metadata = pd.read_csv(META_PATH, usecols=COLUMNS_TO_READ)

# Define cell type classes
EXC_CLASSES = ['01 IT-ET Glut', '02 NP-CT-L6b Glut', '03 OB-CR Glut',
    '04 DG-IMN Glut', '13 CNU-HYa Glut', '14 HY Glut', '15 HY Gnrh1 Glut',
    '16 HY MM Glut', '17 MH-LH Glut', '18 TH Glut', '19 MB Glut', '23 P Glut',
    '24 MY Glut', '25 Pineal Glut', '29 CB Glut']
INH_CLASSES = ['05 OB-IMN GABA', '06 CTX-CGE GABA', '07 CTX-MGE GABA',
    '08 CNU-MGE GABA', '09 CNU-LGE GABA', '10 LSX GABA', '11 CNU-HYa GABA',
    '12 HY GABA', '20 MB GABA', '26 P GABA', '27 MY GABA', '28 CB GABA']
NON_NEURON_CLASSES = ['30 Astro-Epen', '31 OPC-Oligo', '32 OEC', '33 Vascular', '34 Immune']

# Derived clusters
NEURON_TYPES = np.unique(metadata[metadata['class'].isin(EXC_CLASSES + INH_CLASSES)]['cluster'].values)
NON_NEURON_TYPES = np.unique(metadata[metadata['class'].isin(NON_NEURON_CLASSES)]['cluster'].values)

# Load hierarchy and parcellation data
HIERARCHY_JSON = '/gpfs/bbp.cscs.ch/data/project/proj84/atlas_pipeline_runs/2024-05-15T22:44:26+02:00/hierarchy_ccfv3_l23split_barrelsplit.json'
PARECELLATION_FILE = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/parcellation_to_parcellation_term_membership_extend.csv'

region_map = RegionMap.load_json(HIERARCHY_JSON)
parcellation_annotation = pd.read_csv(PARECELLATION_FILE)

# Get all regional density data
DOWNLOAD_BASE = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/'
ROOT_FOLDER = f"{DOWNLOAD_BASE}results/density_calculations/"
CSV_FOLDER_PATH = f"{ROOT_FOLDER}csv/"
csv_filenames = get_csv_filenames(CSV_FOLDER_PATH)
prefixes = extract_prefix_from_filenames(csv_filenames)
unique_prefixes = sorted(list(set(prefixes)))
result_dataframes = read_and_concat_csv_files_new(csv_filenames, unique_prefixes, CSV_FOLDER_PATH)
combined_result_dataframes = combine_rows_and_calculate_average(result_dataframes)

# Perform scaling
scaled_combined_result_dataframes = {}
for key, df in combined_result_dataframes.items():
    if key in region_map.find("Cerebral cortex", attr="name", with_descendants=True):
        neuron_mask = df.index.isin(NEURON_TYPES)
        df.loc[neuron_mask, 'density_mm3'] /= (mfish_ctx / TOTAL_CTX)
        non_neuron_mask = df.index.isin(NON_NEURON_TYPES)
        df.loc[non_neuron_mask, 'density_mm3'] /= (mfish_nonneuron / TOTAL_NONNEURON)
    elif key in region_map.find("Cerebellum", attr="name", with_descendants=True):
        exc_mask = df.index.isin(EXC_CLASSES)
        df.loc[exc_mask, 'density_mm3'] /= (mfish_crb / TOTAL_CRB)
    else:
        neuron_mask = df.index.isin(NEURON_TYPES)
        df.loc[neuron_mask, 'density_mm3'] /= (mfish_rest / TOTAL_REST)
    scaled_combined_result_dataframes[key] = df

# Save scaled data
SCALED_PICKLE_PATH = f"{ROOT_FOLDER}scaled_densities_global_only.pickle"
with open(SCALED_PICKLE_PATH, 'wb') as f:
    pickle.dump(scaled_combined_result_dataframes, f)

print(f"Scaled data saved to {SCALED_PICKLE_PATH}")

# %% Load the scaled data
file = os.path.join(ROOT_FOLDER, 'scaled_densities_global_only.pickle')
with open(file, 'rb') as pickle_file:
    scaled_combined_result_dataframes = pickle.load(pickle_file)
print("Loaded pickle file.")

# %% Prepare combined dataframes
shuffled_combined_dataframes = create_combined_dataframe(scaled_combined_result_dataframes)

# Reorder the dataframes alphabetically by key
sorted_data = {k: shuffled_combined_dataframes[k] for k in sorted(shuffled_combined_dataframes)}

# %% Save the sorted data
folder = ROOT_FOLDER
with open(f'{folder}scaled_densities_global_only_t_types_as_keys.pickle', 'wb') as f:
    pickle.dump(sorted_data, f)

print(f"Saved here: {folder}")

# %% Sort by highest density
pd.options.display.float_format = '{:.2f}'.format
df_sorted = scaled_combined_result_dataframes['UVUgranularlayer'].sort_values(by='density_mm3', ascending=False)

# %% Iterate and print highest density per key
for key, df in combined_result_dataframes.items():
    if 'granularlayer' in key:
        max_density_index = df['density_mm3'].idxmax()
        max_density = df.loc[max_density_index, 'density_mm3']
        print(f"Highest density for {key} at index {max_density_index}: {max_density}")

# %% Load other datasets
fetypes = pd.read_csv("/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/density_calculations/mean_bbp_atlas_densities.csv")
fttypes = pd.read_csv("/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/density_calculations/mean_tr_densities.csv")

columns_to_check = ['neurons_mm3', 'inh_mm3', 'exc_mm3', 'glia_mm3', 'astro_mm3', 'oligo_mm3', 'microglia_mm3', 'nonneuron_mm3']
ttypes = fttypes.dropna(subset=columns_to_check, how='all')
ttypes = ttypes.loc[:, ['acronym'] + columns_to_check]

# Function for validation and NRRD creation
def nrrd_for_validation(df, parcellation_annotation, CCFv3):
    all_ids_for_df = []
    df_comb = pd.DataFrame()

    for regionname in df.index:
        density = df.loc[regionname, 'density_mm3']
        annotation_id_info = parcellation_annotation[parcellation_annotation['cluster_as_filename'] == regionname]
        Annotation2020ids = [int(re.search(r'\d+$', s).group()) for s in annotation_id_info['parcellation_label'].values]
        df_sub = pd.DataFrame({'density': density}, index=Annotation2020ids)
        df_comb = pd.concat([df_comb, df_sub])
        all_ids_for_df.append(Annotation2020ids)

    all_ids_for_df = [value for sublist in all_ids_for_df for value in sublist]
    all_ids_for_df.append(0)

    outside = 0
    outsideid = [0]
    df_sub = pd.DataFrame({'density': outside}, index=outsideid)
    df_comb = pd.concat([df_comb, df_sub])

    CCFv3_copy = CCFv3.copy()

    CCFv3_copy[~np.isin(CCFv3_copy, all_ids_for_df)] = 0.0 

    for index, row in df_comb.iterrows():
        density_value = row['density']
        region_id = index
        CCFv3_copy[np.isin(CCFv3, region_id)] = density_value

    CCFv3_copy[np.isin(CCFv3, 0)] = 0

    return CCFv3_copy

# %% Process type function for multiprocessing
def process_type(types, file_name):
    filtered_dataframes = {key: value for key, value in shuffled_combined_dataframes.items() if key in types}
    combined_df = pd.concat(filtered_dataframes.values())
    summed_df = combined_df.groupby(combined_df.index).sum()
    result = nrrd_for_validation(summed_df, parcellation_annotation, CCFv3)
    del combined_df, summed_df, filtered_dataframes
    return (result, file_name)

# Main function for multiprocessing
def main():
    tasks = [
        (neurontypes, "scaled_total_neuron_densities"),
        (exctypes, "scaled_total_excitatory_densities"),
        (inhtypes, "scaled_total_inhibitory_densities"),
        (astrotypes, "scaled_total_astrotypes_densities"),
        (microglia, "scaled_total_microglia_densities"),
        (oligos, "scaled_total_oligocyte_densities"),
        (glia, "scaled_total_glia_densities"),
        (exci_inhib_sum, "scaled_total_excinh_densities"),
        (celltypes, "scaled_total_celltypes_densities"),
        (nonneurontypes, "scaled_total_nonneuron_densities")
    ]
    
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.starmap(process_type, tasks)
    
    for result, file_name in results:
        nrrd.write(f"{ROOT_FOLDER}total_nrrd_global_only/{file_name}.nrrd", result)
        print(f"{ROOT_FOLDER}total_nrrd/{file_name}.nrrd")
        
if __name__ == "__main__":
    main()
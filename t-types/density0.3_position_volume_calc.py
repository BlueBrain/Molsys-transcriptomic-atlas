#!/usr/bin/env python
# coding: utf-8

'''
Dependencies:
pip install numpy pandas
chmod +x script.py

In this code we loop through all MERFISH cells and add a new metadata to them: their region information and its estimated volume in the slice. 
So if a cell sits in the MOB we calculate the intersected volume of the MOB in the respective slice (with slice position)

Execute with: python density0.3_position_volume_calc-Copy1.py
    view_directory = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/MERFISH-C57BL6J-638850-CCF/20231215/views/'
    output_directory = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/nmi_scores/'
    parcellation_file = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/MERFISH-C57BL6J-638850-CCF/20231215/views/'
    positions_file = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/results/nmi_scores/average_template_array/output.csv'

'''

import os
import pandas as pd
import numpy as np
import pickle
import ast

# Helper Functions
def load_cell_metadata(view_directory):
    """Load cell metadata into a DataFrame."""
    file = os.path.join(view_directory, 'cell_metadata_with_parcellation_annotation.csv')
    cell_joined = pd.read_csv(file)
    cell_joined.set_index('cell_label', inplace=True)
    return cell_joined

def clean_cells(cell_joined):
    """Remove cells with no x, y, z CCF coordinates."""
    return cell_joined[~((cell_joined['x_ccf'] == 0) & (cell_joined['y_ccf'] == 0) & (cell_joined['z_ccf'] == 0))]

def prepare_cells_dataframe(cell_joined):
    """Create and prepare a smaller cells DataFrame."""
    cells = cell_joined[['brain_section_label', 'x_reconstructed', 'y_reconstructed', 'z_reconstructed']].copy()
    cells['template_nr'] = (cells['z_reconstructed'].values / 0.2).round()
    cells['parcellation_substructure'] = cell_joined['parcellation_substructure']
    return cells

def load_parcellation_info(file_path, cell_joined):
    """Load parcellation annotation and substructure info."""
    parcellation_annotation = pd.read_csv(file_path)
    parcellation_indexes = list(np.unique(cell_joined['parcellation_index']))
    return parcellation_annotation[parcellation_annotation['parcellation_index'].isin(parcellation_indexes)]

def get_region_id_mapping(substructure_info):
    """Map substructures to region IDs."""
    def get_region_id(substructure):
        return int(substructure_info[substructure_info['parcellation_term_acronym'] == substructure]
                   ['parcellation_label'].values[0].split('-')[-1])
    return get_region_id

def resolve_voxel_volume(row, template_with_regids, key_errors, templ_errors):
    """Resolve voxel volumes with error handling."""
    template_nr = row['template_nr']
    region_id = row['region_id']
    mappings = {229: 794, 326: [812, 850, 866], 956: 579}
    try:
        return template_with_regids[template_nr][region_id]
    except KeyError:
        key_errors.append(region_id)
        templ_errors.append(template_nr)
        new_ids = mappings.get(region_id, [])
        if not isinstance(new_ids, list):
            new_ids = [new_ids]
        for new_id in new_ids:
            try:
                return template_with_regids[template_nr][new_id]
            except KeyError:
                continue
        print(f"Key not found: template {template_nr}, region {region_id}")
        return None

def update_best_position(cells, positions_file):
    """Add best position based on the template_nr column."""
    positions = pd.read_csv(positions_file)
    positions['best_pos'] = positions['10um_cortical_pos'].apply(lambda x: ast.literal_eval(x)[0])
    positions['template_nr'] = positions['X_as_first_dim'].apply(lambda x: x.split('_')[3]).astype(float)
    pos_dict = dict(zip(positions['template_nr'], positions['best_pos']))
    cells['best_position'] = cells['template_nr'].map(pos_dict)
    return cells

# Main Execution
def main():
    """Main function to execute the entire workflow."""
    # Prompt user for directories
    view_directory = input("Enter the directory for input cell metadata: ").strip()
    output_directory = input("Enter the directory to save results: ").strip()
    parcellation_file = input("Enter the path for parcellation annotation CSV: ").strip()
    positions_file = input("Enter the path for positions CSV: ").strip()
    pickle_file = input("Enter the path for the template_with_regids pickle file: ").strip()

    # Step 1: Load and clean data
    print("Loading cell metadata...")
    cell_joined = load_cell_metadata(view_directory)
    cell_joined = clean_cells(cell_joined)
    cells = prepare_cells_dataframe(cell_joined)
    
    # Step 2: Load parcellation info and add region IDs
    print("Loading parcellation information...")
    substructure_info = load_parcellation_info(parcellation_file, cell_joined)
    get_region_id = get_region_id_mapping(substructure_info)
    cells['region_id'] = cells['parcellation_substructure'].apply(lambda x: get_region_id(x))
    
    # Step 3: Load template volumes and calculate voxel volume
    print("Loading region volumes from pickle...")
    with open(pickle_file, 'rb') as f:
        template_with_regids = pickle.load(f)

    print("Calculating voxel volumes...")
    key_errors, templ_errors = [], []
    cells['voxel_vol'] = cells.apply(lambda row: resolve_voxel_volume(row, template_with_regids, key_errors, templ_errors), axis=1)
    
    # Step 4: Add best position to cells
    print("Adding best positions...")
    cells = update_best_position(cells, positions_file)
    
    # Step 5: Save final results
    os.makedirs(output_directory, exist_ok=True)
    output_file = os.path.join(output_directory, 'cells_in_respective_volumes.csv')
    print(f"Saving results to {output_file}...")
    cells.to_csv(output_file, index=True)
    print("Process completed successfully.")

if __name__ == "__main__":
    main()

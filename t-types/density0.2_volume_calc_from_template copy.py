#!/usr/bin/env python
# coding: utf-8

'''
Dependencies:
pip install SimpleITK nrrd requests matplotlib pandas cv2
chmod +x script.py

In this code we leverage the rotated resampled and aligned annotation volumes. 
We have to guess the anontations in each voxel though as they were changed to an INT between 0 and 3000 for visualisation purposes

Execute with: python density0.2_volume_calc_from_template.py
'''

import os
import SimpleITK as sitk
import json
import numpy as np
import matplotlib.pyplot as plt
import requests
import nrrd
import pandas as pd
import cv2
import pickle
from collections import Counter


# Constants
VERSION = '20231215'
DOWNLOAD_BASE = '/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/'
USE_LOCAL_CACHE = False
MANIFEST_PATH = f'releases/{VERSION}/manifest.json'

save_path = input("Please enter a save path for the processed voxel counts (e.g., /path/to/save): ").strip()
save_file = os.path.join(save_path, 'template_with_regids.pkl')

def get_manifest():
    """Retrieve manifest information either from Allen Brain Atlas URL or local cache."""
    if not USE_LOCAL_CACHE:
        url = f'https://allen-brain-cell-atlas.s3-us-west-2.amazonaws.com/{MANIFEST_PATH}'
        manifest = json.loads(requests.get(url).text)
    else:
        file_path = os.path.join(DOWNLOAD_BASE, MANIFEST_PATH)
        with open(file_path, 'rb') as f:
            manifest = json.load(f)
    return manifest

def read_and_process_nrrd():
    """Read annotation data from an NRRD file and process it into numpy arrays."""
    nrrd_file_path = '/gpfs/bbp.cscs.ch/home/veraszto/bbp_prod_files/2022/annotation_10.nrrd'
    avol, _ = nrrd.read(nrrd_file_path)
    avol = avol.flatten()
    
    # Get unique counts
    unique_elements, counts = np.unique(avol, return_counts=True)
    nrrd_counts = dict(zip(unique_elements, counts))
    
    # Log any duplicates
    duplicates = Counter(nrrd_counts.values())
    print("Found duplicates in NRRD counts:", duplicates)
    
    return nrrd_counts

def read_image_data(file_path):
    """Read a NIfTI file into a numpy array."""
    image = sitk.ReadImage(file_path)
    return sitk.GetArrayViewFromImage(image)


def clean_and_deduplicate(df):
    """Remove duplicates and ensure only unique values are processed."""
    dict1 = {}
    dict2 = {}
    
    # Find duplicates and adjust values
    for key, value in df.items():
        if value in dict2:
            dict2[key] = f"{value}a"
    return dict2

def preprocess_annotation_array(annotation_array):
    """Transpose annotation arrays for consistent processing."""
    return np.transpose(annotation_array).astype(np.uint16)

def analyze_annotation_volumes(manifest):
    """Read specific annotation images and prepare arrays."""
    # Read annotations from the manifest
    annotation_paths = manifest['file_listing']['MERFISH-C57BL6J-638850-CCF']['image_volumes']
    average_template_path = os.path.join(DOWNLOAD_BASE, annotation_paths['resampled_average_template']['files']['nii.gz']['relative_path'])
    annotation_path = os.path.join(DOWNLOAD_BASE, annotation_paths['resampled_annotation']['files']['nii.gz']['relative_path'])
    
    average_template_array = read_image_data(average_template_path)
    annotation_array = read_image_data(annotation_path)

    return average_template_array, annotation_array


def save_voxel_counts(data, save_path):
    """Save voxel count data as pickle for downstream processing."""
    with open(save_path, 'wb') as f:
        pickle.dump(data, f)

def main():
    # Retrieve manifest data
    manifest = get_manifest()

    # Read and preprocess data
    average_template_array, annotation_array = preprocess_annotation_array(
        analyze_annotation_volumes(manifest))

    # Read and process NRRD annotations
    nrrd_counts = read_and_process_nrrd()
    print("Processed NRRD data:", nrrd_counts)

    # Map annotation array to region IDs
    template_numbers = [4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                         21, 22, 23, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 38]

    # Process annotation arrays and voxel counts
    slice_voxel_counts = {}
    for tnum in template_numbers:
        annotation_slice = annotation_array[tnum].flatten()
        unique_ids, counts = np.unique(annotation_slice, return_counts=True)
        mapping = dict(zip(unique_ids, counts))

        # Save mappings to dataframe
        region_df = pd.DataFrame({'Region_id': list(mapping.values())})
        
        save_voxel_counts(region_df, save_file)
        
    print("Completed processing slices")


if __name__ == "__main__":
    main()


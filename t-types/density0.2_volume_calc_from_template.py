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
import pickle
import numpy as np
import pandas as pd
import SimpleITK as sitk

def load_data(template_path, data_paths):
    """
    Load template and data images.
    Args:
        template_path (str): Path to the template image.
        data_paths (list): List of paths to data images.
    Returns:
        tuple: Template image and list of data images.
    """
    template_image = sitk.ReadImage(template_path)
    data_images = [sitk.ReadImage(path) for path in data_paths]
    return template_image, data_images

def calculate_volumes(template_image, data_images, density_threshold=0.2):
    """
    Calculate volumes based on density threshold.
    Args:
        template_image: Template SimpleITK image.
        data_images (list): List of SimpleITK data images.
        density_threshold (float): Threshold for volume calculation.
    Returns:
        dict: Calculated volumes for each image.
    """
    template_array = sitk.GetArrayFromImage(template_image)
    results = {}
    for i, image in enumerate(data_images):
        data_array = sitk.GetArrayFromImage(image)
        mask = data_array > density_threshold
        volume = np.sum(mask) * np.prod(template_image.GetSpacing())
        results[f'image_{i+1}'] = volume
    return results

def save_results(output_dir, results):
    """
    Save the results to a pickle file.
    Args:
        output_dir (str): Directory to save the results.
        results (dict): Volume calculation results.
    """
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'volume_results.pkl')
    with open(output_path, 'wb') as f:
        pickle.dump(results, f)
    print(f"Results saved to: {output_path}")

def main():
    """
    Main execution function.
    """
    # Prompt user for input
    template_path = input("Enter the path to the template image: ").strip()
    data_paths = input("Enter the paths to the data images (comma-separated): ").strip().split(',')
    output_dir = input("Enter the output directory to save the results: ").strip()
    
    # Validate paths
    if not os.path.exists(template_path):
        print("Error: Template path does not exist.")
        return
    for path in data_paths:
        if not os.path.exists(path.strip()):
            print(f"Error: Data image path {path} does not exist.")
            return

    # Load data
    print("Loading data...")
    template_image, data_images = load_data(template_path, data_paths)
    
    # Calculate volumes
    print("Calculating volumes...")
    results = calculate_volumes(template_image, data_images)
    
    # Save results
    print("Saving results...")
    save_results(output_dir, results)

    print("Process completed successfully.")

if __name__ == "__main__":
    main()
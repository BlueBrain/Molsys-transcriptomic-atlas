#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import argparse

''' 
We are editing the AIBS csv file on parcellation_to_parcellation_term_membership. This step is not necessarily required but it makes working with this metadata easier. 
parcellation_annotation is located here: /gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/parcellation_to_parcellation_term_membership_extend_backup.csv
Save it like this:
'/gpfs/bbp.cscs.ch/data/project/proj84/csaba/aibs_10x_mouse_wholebrain/metadata/parcellation_to_parcellation_term_membership_extend.csv'

Execute code: python process_annotations.py /path/to/your/output.csv
'''


def main(output_file):
    # Initialize empty parcellation_annotation DataFrame
    parcellation_annotation = pd.DataFrame()

    mob_data = {
    'Unnamed: 0': [3440],
    'parcellation_label': ['AllenCCF-Annotation-2020-212'],
    'parcellation_term_label': ['ABC-Ontology-2023-MOB-substructure'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [497],
    'voxel_count': [743860],
    'volume_mm3': [0.0074386],
    'color_hex_triplet': ['#9AD2BD'],
    'red': [154],
    'green': [210],
    'blue': [189],
    'parcellation_term_name': ['Main olfactory bulb, glomerular layer'],
    'parcellation_term_acronym': ['MOBglomerularlayer'],
    'parcellation_term_set_name': ['substructure'],
    'term_set_order': [4],
    'term_order': [252],
    'parent_term_label': ['AllenCCF-Ontology-2017-507'],
    'label_numbers': [212],
    'cluster_as_filename': ['MOBglomerularlayer']
    }
    df = pd.DataFrame(mob_data, index=[0])
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3441, 3442, 3443],
    'parcellation_label': ['AllenCCF-Annotation-2020-10708', 'AllenCCF-Annotation-2020-10709', 'AllenCCF-Annotation-2020-10710'],
    'parcellation_term_label': ['AllenCCF-Ontology-2017-976', 'AllenCCF-Ontology-2017-976', 'AllenCCF-Ontology-2017-976'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [966, 966, 966],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Lobule II, granular layer', 'Lobule II, Purkinje layer', 'Lobule II, molecular layer'],
    'parcellation_term_acronym': ['CENT2granularlayer', 'CENT2purkinjelayer', 'CENT2molecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [711, 711, 711],
    'parent_term_label': ['AllenCCF-Ontology-2017-976', 'AllenCCF-Ontology-2017-976', 'AllenCCF-Ontology-2017-976'],
    'label_numbers': [10708, 10709, 10710],
    'cluster_as_filename': ['CENT2granularlayer', 'CENT2purkinjelayer', 'CENT2molecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3444, 3445, 3446],
    'parcellation_label': ['AllenCCF-Annotation-2020-10711', 'AllenCCF-Annotation-2020-10712', 'AllenCCF-Annotation-2020-10713'],
    'parcellation_term_label': ['AllenCCF-Ontology-2017-984', 'AllenCCF-Ontology-2017-984', 'AllenCCF-Ontology-2017-984'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [974, 974, 974],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Lobule III, granular layer', 'Lobule III, Purkinje layer', 'Lobule III, molecular layer'],
    'parcellation_term_acronym': ['CENT3granularlayer', 'CENT3purkinjelayer', 'CENT3molecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [712, 712, 712],
    'parent_term_label': ['AllenCCF-Ontology-2017-984', 'AllenCCF-Ontology-2017-984', 'AllenCCF-Ontology-2017-984'],
    'label_numbers': [10711, 10712, 10713],
    'cluster_as_filename': ['CENT3granularlayer', 'CENT3purkinjelayer', 'CENT3molecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3447, 3448, 3449],
    'parcellation_label': ['AllenCCF-Annotation-2020-10675', 'AllenCCF-Annotation-2020-10676', 'AllenCCF-Annotation-2020-10677'],
    'parcellation_term_label': ['AllenCCF-Ontology-2017-1056', 'AllenCCF-Ontology-2017-1056', 'AllenCCF-Ontology-2017-1056'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [1045, 1045, 1045],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Crus 1, granular layer', 'Crus 1, Purkinje layer', 'Crus 1, molecular layer'],
    'parcellation_term_acronym': ['ANcr1granularlayer', 'ANcr1purkinjelayer', 'ANcr1molecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [740, 740, 740],
    'parent_term_label': ['AllenCCF-Ontology-2017-1056', 'AllenCCF-Ontology-2017-1056', 'AllenCCF-Ontology-2017-1056'],
    'label_numbers': [10675, 10676, 10677],
    'cluster_as_filename': ['ANcr1granularlayer', 'ANcr1purkinjelayer', 'ANcr1molecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3450, 3451, 3452],
    'parcellation_label': ['AllenCCF-Annotation-2020-10678', 'AllenCCF-Annotation-2020-10679', 'AllenCCF-Annotation-2020-10680'],
    'parcellation_term_label': ['AllenCCF-Ontology-2017-1064', 'AllenCCF-Ontology-2017-1064', 'AllenCCF-Ontology-2017-1064'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [1053, 1053, 1053],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Crus 2, granular layer', 'Crus 2, Purkinje layer', 'Crus 2, molecular layer'],
    'parcellation_term_acronym': ['ANcr2granularlayer', 'ANcr2purkinjelayer', 'ANcr2molecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [741, 741, 741],
    'parent_term_label': ['AllenCCF-Ontology-2017-1064', 'AllenCCF-Ontology-2017-1064', 'AllenCCF-Ontology-2017-1064'],
    'label_numbers': [10678, 10679, 10680],
    'cluster_as_filename': ['ANcr2granularlayer', 'ANcr2purkinjelayer', 'ANcr2molecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3453, 3454, 3455],
    'parcellation_label': ['AllenCCF-Annotation-2020-10705', 'AllenCCF-Annotation-2020-10706', 'AllenCCF-Annotation-2020-10707'],
    'parcellation_term_label': ['ABC-Ontology-2023-LING-substructure', 'ABC-Ontology-2023-LING-substructure', 'ABC-Ontology-2023-LING-substructure'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [902, 902, 902],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Lingula (I), granular layer', 'Lingula (I), Purkinje layer', 'Lingula (I), molecular layer'],
    'parcellation_term_acronym': ['LINGgranularlayer', 'LINGpurkinjelayer', 'LINGmolecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [707, 707, 707],
    'parent_term_label': ['AllenCCF-Ontology-2017-912', 'AllenCCF-Ontology-2017-912', 'AllenCCF-Ontology-2017-912'],
    'label_numbers': [10705, 10706, 10707],
    'cluster_as_filename': ['LINGgranularlayer', 'LINGpurkinjelayer', 'LINGmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3456, 3457, 3458],
    'parcellation_label': ['AllenCCF-Annotation-2020-10723', 'AllenCCF-Annotation-2020-10724', 'AllenCCF-Annotation-2020-10725'],
    'parcellation_term_label': ['ABC-Ontology-2023-DEC-substructure', 'ABC-Ontology-2023-DEC-substructure', 'ABC-Ontology-2023-DEC-substructure'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [926, 926, 926],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Declive (VI), granular layer', 'Declive (VI), Purkinje layer', 'Declive (VI), molecular layer'],
    'parcellation_term_acronym': ['DECgranularlayer', 'DECpurkinjelayer', 'DECmolecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [716, 716, 716],
    'parent_term_label': ['AllenCCF-Ontology-2017-936', 'AllenCCF-Ontology-2017-936', 'AllenCCF-Ontology-2017-936'],
    'label_numbers': [10723, 10724, 10725],
    'cluster_as_filename': ['DECgranularlayer', 'DECpurkinjelayer', 'DECmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3459, 3460, 3461],
    'parcellation_label': ['AllenCCF-Annotation-2020-10726', 'AllenCCF-Annotation-2020-10727', 'AllenCCF-Annotation-2020-10728'],
    'parcellation_term_label': ['ABC-Ontology-2023-FOTU-substructure', 'ABC-Ontology-2023-FOTU-substructure', 'ABC-Ontology-2023-FOTU-substructure'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [934, 934, 934],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Folium-tuber vermis (VII), granular layer', 'Folium-tuber vermis (VII), Purkinje layer', 'Folium-tuber vermis (VII), molecular layer'],
    'parcellation_term_acronym': ['FOTUgranularlayer', 'FOTUpurkinjelayer', 'FOTUmolecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [720, 720, 720],
    'parent_term_label': ['AllenCCF-Ontology-2017-944', 'AllenCCF-Ontology-2017-944', 'AllenCCF-Ontology-2017-944'],
    'label_numbers': [10726, 10727, 10728],
    'cluster_as_filename': ['FOTUgranularlayer', 'FOTUpurkinjelayer', 'FOTUmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3462, 3463, 3464],
    'parcellation_label': ['AllenCCF-Annotation-2020-10729', 'AllenCCF-Annotation-2020-10730', 'AllenCCF-Annotation-2020-10731'],
    'parcellation_term_label': ['ABC-Ontology-2023-PYR-substructure', 'ABC-Ontology-2023-PYR-substructure', 'ABC-Ontology-2023-PYR-substructure'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [941, 941, 941],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Pyramus (VIII), granular layer', 'Pyramus (VIII), Purkinje layer', 'Pyramus (VIII), molecular layer'],
    'parcellation_term_acronym': ['PYRgranularlayer', 'PYRpurkinjelayer', 'PYRmolecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [724, 724, 724],
    'parent_term_label': ['AllenCCF-Ontology-2017-951', 'AllenCCF-Ontology-2017-951', 'AllenCCF-Ontology-2017-951'],
    'label_numbers': [10729, 10730, 10731],
    'cluster_as_filename': ['PYRgranularlayer', 'PYRpurkinjelayer', 'PYRmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3465, 3466, 3467],
    'parcellation_label': ['AllenCCF-Annotation-2020-10732', 'AllenCCF-Annotation-2020-10733', 'AllenCCF-Annotation-2020-10734'],
    'parcellation_term_label': ['ABC-Ontology-2023-UVU-substructure', 'ABC-Ontology-2023-UVU-substructure', 'ABC-Ontology-2023-UVU-substructure'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [947, 947, 947],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Uvula (IX), granular layer', 'Uvula (IX), Purkinje layer', 'Uvula (IX), molecular layer'],
    'parcellation_term_acronym': ['UVUgranularlayer', 'UVUpurkinjelayer', 'UVUmolecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [728, 728, 728],
    'parent_term_label': ['AllenCCF-Ontology-2017-957', 'AllenCCF-Ontology-2017-957', 'AllenCCF-Ontology-2017-957'],
    'label_numbers': [10732, 10733, 10734],
    'cluster_as_filename': ['UVUgranularlayer', 'UVUpurkinjelayer', 'UVUmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3468, 3469, 3470],
    'parcellation_label': ['AllenCCF-Annotation-2020-10735', 'AllenCCF-Annotation-2020-10736', 'AllenCCF-Annotation-2020-10737'],
    'parcellation_term_label': ['ABC-Ontology-2023-NOD-substructure', 'ABC-Ontology-2023-NOD-substructure', 'ABC-Ontology-2023-NOD-substructure'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [958, 958, 958],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Nodulus (X), granular layer', 'Nodulus (X), Purkinje layer', 'Nodulus (X), molecular layer'],
    'parcellation_term_acronym': ['NODgranularlayer', 'NODpurkinjelayer', 'NODmolecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [732, 732, 732],
    'parent_term_label': ['AllenCCF-Ontology-2017-968', 'AllenCCF-Ontology-2017-968', 'AllenCCF-Ontology-2017-968'],
    'label_numbers': [10735, 10736, 10737],
    'cluster_as_filename': ['NODgranularlayer', 'NODpurkinjelayer', 'NODmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3471, 3472, 3473],
    'parcellation_label': ['AllenCCF-Annotation-2020-10672', 'AllenCCF-Annotation-2020-10673', 'AllenCCF-Annotation-2020-10674'],
    'parcellation_term_label': ['ABC-Ontology-2023-SIM-substructure', 'ABC-Ontology-2023-SIM-substructure', 'ABC-Ontology-2023-SIM-substructure'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [997, 997, 997],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Simple lobule, granular layer', 'Simple lobule, Purkinje layer', 'Simple lobule, molecular layer'],
    'parcellation_term_acronym': ['SIMgranularlayer', 'SIMpurkinjelayer', 'SIMmolecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [736, 736, 736],
    'parent_term_label': ['AllenCCF-Ontology-2017-1007', 'AllenCCF-Ontology-2017-1007', 'AllenCCF-Ontology-2017-1007'],
    'label_numbers': [10672, 10673, 10674],
    'cluster_as_filename': ['SIMgranularlayer', 'SIMpurkinjelayer', 'SIMmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
    'Unnamed: 0': [3474, 3475, 3476],
    'parcellation_label': ['AllenCCF-Annotation-2020-10681', 'AllenCCF-Annotation-2020-10682', 'AllenCCF-Annotation-2020-10683'],
    'parcellation_term_label': ['ABC-Ontology-2023-PRM-substructure', 'ABC-Ontology-2023-PRM-substructure', 'ABC-Ontology-2023-PRM-substructure'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [1014, 1014, 1014],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Paramedian lobule, granular layer', 'Paramedian lobule, Purkinje layer', 'Paramedian lobule, molecular layer'],
    'parcellation_term_acronym': ['PRMgranularlayer', 'PRMpurkinjelayer', 'PRMmolecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [742, 742, 742],
    'parent_term_label': ['AllenCCF-Ontology-2017-1025', 'AllenCCF-Ontology-2017-1025', 'AllenCCF-Ontology-2017-1025'],
    'label_numbers': [10681, 10682, 10683],
    'cluster_as_filename': ['PRMgranularlayer', 'PRMpurkinjelayer', 'PRMmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)

    new_data = {
        'Unnamed: 0': [3477, 3478, 3479],
        'parcellation_label': ['AllenCCF-Annotation-2020-10687', 'AllenCCF-Annotation-2020-10688', 'AllenCCF-Annotation-2020-10689'],
        'parcellation_term_label': ['ABC-Ontology-2023-PFL-substructure', 'ABC-Ontology-PFL-substructure', 'ABC-Ontology-2023-PFL-substructure'],
        'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
        'parcellation_index': [1030, 1030, 1030],
        'voxel_count': [np.nan, np.nan, np.nan],
        'volume_mm3': [np.nan, np.nan, np.nan],
        'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
        'red': [255, 255, 255],
        'green': [252, 252, 252],
        'blue': [145, 145, 145],
        'parcellation_term_name': ['Paraflocculus, granular layer', 'Paraflocculus, Purkinje layer', 'Paraflocculus, molecular layer'],
        'parcellation_term_acronym': ['PFLgranularlayer', 'PFLpurkinjelayer', 'PFLmolecularlayer'],
        'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
        'term_set_order': [4, 4, 4],
        'term_order': [750, 750, 750],
        'parent_term_label': ['AllenCCF-Ontology-2017-1041', 'AllenCCF-Ontology-2017-1041', 'AllenCCF-Ontology-2017-1041'],
        'label_numbers': [10687, 10688, 10689],
        'cluster_as_filename': ['PFLgranularlayer', 'PFLpurkinjelayer', 'PFLmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)
    
    new_data = {
        'Unnamed: 0': [3480, 3481, 3482],
        'parcellation_label': ['AllenCCF-Annotation-2020-10690', 'AllenCCF-Annotation-2020-10691', 'AllenCCF-Annotation-2020-10692'],
        'parcellation_term_label': ['ABC-Ontology-2023-FL-substructure', 'ABC-Ontology-FL-COPY-substructure', 'ABC-Ontology-2023-FL-substructure'],
        'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
        'parcellation_index': [1038, 1038, 1038],
        'voxel_count': [np.nan, np.nan, np.nan],
        'volume_mm3': [np.nan, np.nan, np.nan],
        'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
        'red': [255, 255, 255],
        'green': [252, 252, 252],
        'blue': [145, 145, 145],
        'parcellation_term_name': ['Flocculus, granular layer', 'Flocculus, Purkinje layer', 'Flocculus, molecular layer'],
        'parcellation_term_acronym': ['FLgranularlayer', 'FLpurkinjelayer', 'FLmolecularlayer'],
        'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
        'term_set_order': [4, 4, 4],
        'term_order': [754, 754, 754],
        'parent_term_label': ['AllenCCF-Ontology-2017-1049', 'AllenCCF-Ontology-2017-1049', 'AllenCCF-Ontology-2017-1049'],
        'label_numbers': [10690, 10691, 10692],
        'cluster_as_filename': ['FLgranularlayer', 'FLpurkinjelayer', 'FLmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)


    new_data = {
        'Unnamed: 0': [3483, 3484, 3485],
        'parcellation_label': ['AllenCCF-Annotation-2020-10684', 'AllenCCF-Annotation-2020-10685', 'AllenCCF-Annotation-2020-10686'],
        'parcellation_term_label': ['ABC-Ontology-2023-COPY-substructure', 'ABC-Ontology-COPY-substructure', 'ABC-Ontology-2023-COPY-substructure'],
        'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
        'parcellation_index': [1022, 1022, 1022],
        'voxel_count': [np.nan, np.nan, np.nan],
        'volume_mm3': [np.nan, np.nan, np.nan],
        'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
        'red': [255, 255, 255],
        'green': [252, 252, 252],
        'blue': [145, 145, 145],
        'parcellation_term_name': ['Copula pyramidis, granular layer', 'Copula pyramidis, Purkinje layer', 'Copula pyramidis, molecular layer'],
        'parcellation_term_acronym': ['COPYgranularlayer', 'COPYpurkinjelayer', 'COPYmolecularlayer'],
        'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
        'term_set_order': [4, 4, 4],
        'term_order': [746, 746, 746],
        'parent_term_label': ['AllenCCF-Ontology-2017-1049', 'AllenCCF-Ontology-2017-1049', 'AllenCCF-Ontology-2017-1049'],
        'label_numbers': [10684, 10685, 10686],
        'cluster_as_filename': ['COPYgranularlayer', 'COPYpurkinjelayer', 'COPYmolecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)


    new_data = {
    'Unnamed: 0': [3486, 3487, 3488],
    'parcellation_label': ['AllenCCF-Annotation-2020-10720', 'AllenCCF-Annotation-2020-10721', 'AllenCCF-Annotation-2020-10722'],
    'parcellation_term_label': ['AllenCCF-Ontology-2017-1091', 'AllenCCF-Ontology-2017-1091', 'AllenCCF-Ontology-2017-1091'],
    'parcellation_term_set_label': ['AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS', 'AllenCCF-Ontology-2017-SUBS'],
    'parcellation_index': [1080, 1080, 1080],
    'voxel_count': [np.nan, np.nan, np.nan],
    'volume_mm3': [np.nan, np.nan, np.nan],
    'color_hex_triplet': ['#FFFC91', '#FFFC91', '#FFFC91'],
    'red': [255, 255, 255],
    'green': [252, 252, 252],
    'blue': [145, 145, 145],
    'parcellation_term_name': ['Lobules IV-V, granular layer', 'Lobules IV-V, Purkinje layer', 'Lobules IV-V, molecular layer'],
    'parcellation_term_acronym': ['CUL45granularlayer', 'CUL45purkinjelayer', 'CUL45molecularlayer'],
    'parcellation_term_set_name': ['substructure', 'substructure', 'substructure'],
    'term_set_order': [4, 4, 4],
    'term_order': [715, 715, 715],
    'parent_term_label': ['AllenCCF-Ontology-2017-1091', 'AllenCCF-Ontology-2017-1091', 'AllenCCF-Ontology-2017-1091'],
    'label_numbers': [10720, 10721, 10722],
    'cluster_as_filename': ['CUL45granularlayer', 'CUL45purkinjelayer', 'CUL45molecularlayer']
    }
    df = pd.DataFrame(new_data)
    parcellation_annotation = pd.concat([parcellation_annotation, df], ignore_index=True)
    
    # Save the data to CSV
    parcellation_annotation.set_index('Unnamed: 0', inplace=True)
    parcellation_annotation.to_csv(output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update parcellation annotations and save to CSV.")
    parser.add_argument("output_file", type=str, help="Path to save the CSV output.")
    args = parser.parse_args()
    main(args.output_file)

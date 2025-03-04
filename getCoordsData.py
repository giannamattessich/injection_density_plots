import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
# allen institute CCF mouse atlas 25 um reference CSV
allen_df = pd.read_csv(r'structure_tree_safe_2017.csv')
test_csv = r"C:\Users\Public\OneDrive - Montefiore Medicine\Desktop\SliceData\nelson_brains\2020_points.csv"
# function to read outputs from NeuroInfo csv output
# data has 2 different possible CSV formats depending on brain, this function accounts for these differences in data format by checking first column name
# Args:
    # csv (str) -> path of neuroinfo csv file
# Outputs (tuple):
    # cell_count_acronym_dict (dict) -> dictionary mapping CCF acronym to cell count
    # cell_count_name_dict (dict) -> dictionary mapping region name to cell count
def read_points_csv(csv):
    points_df = pd.read_csv(csv, header=None)
    # remove unnecessary header row and reassign columns
    columns = points_df.iloc[1]
    points_df.drop([0, 1], inplace=True)
    points_df.columns = columns
    points_df.reset_index(drop=True, inplace=True)
    # check if first column is "name"
    if points_df.columns[0] == 'name':
        # get all columns labeled 'count' and sum them 
        points_df['total count'] = points_df['count'].astype(int).sum(axis=1)
        # get all rows, and name, acronym, count cols
        count_df = points_df.loc[:, ['name', 'acronym', 'total count']]
        acronym_dict = {}
        name_dict = {}
        # iter through rows, update acronym and name dicts and their counts
        for idx in range(len(count_df)):
            next_acronym = count_df.iloc[idx]['acronym']
            if next_acronym in acronym_dict.keys():
                acronym_dict[next_acronym] += count_df.iloc[idx]['total count']
                name_dict[count_df.iloc[idx]['name']] += count_df.iloc[idx]['total count']
            else:
                acronym_dict[next_acronym] = count_df.iloc[idx]['total count']
                name_dict[count_df.iloc[idx]['name']] = count_df.iloc[idx]['total count']
        cell_count_acronym_dict = acronym_dict
        cell_count_name_dict = name_dict
    else:
        # if csv in other format, use number of times acronym/name appears as markers for cell counts
        cell_count_acronym_dict = dict(points_df.value_counts('acronym'))
        cell_count_name_dict = dict(points_df.value_counts('name'))
    return cell_count_acronym_dict, cell_count_name_dict

# Combine data from all point csvs in provided folder
# Args
    # folder (str) -> folder with point csvs
# Output (tuple)
    # acronym dict (dict) -> acronyms as keys and cell counts as values for ALL csvs
    # name dict (dict) -> region names as keys and cell counts as values for ALL csvs from folder
def get_combined_data(folder):
    acronym_dict_combined = {}
    name_dict_combined = {}
    for csv_file in os.listdir(folder):
        if csv_file.endswith('.csv'):
            csv = os.path.join(folder, csv_file)
            count_acronym_dict, count_name_dict = read_points_csv(csv)
            for key, val in count_acronym_dict.items():
                if key in acronym_dict_combined.keys():
                    acronym_dict_combined[key] += val
                else:
                    acronym_dict_combined[key] = val
            for key, val in count_name_dict.items():
                if key in name_dict_combined.keys():
                    name_dict_combined[key] += val
                else:
                    name_dict_combined[key] = val
    return acronym_dict_combined, name_dict_combined

# Get a dictionary for visual region cell counts
# Args
    # folder(str) -> path to folder with neuroinfo csvs
# Output
    # name dict -> dictionary with vision regions only as keys and cell counts as values
def get_combined_visual_count(folder):
    name_dict_combined = {}
    for csv_file in os.listdir(folder):
        csv = os.path.join(folder, csv_file)
        count_acronym_dict, count_name_dict = read_points_csv(csv)
        for key, val in count_name_dict.items():
            if 'visual' in key:
                if key in name_dict_combined.keys():
                    name_dict_combined[key] += val
                else:
                    name_dict_combined[key] = val
    return name_dict_combined



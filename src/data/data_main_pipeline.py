"""
Main pipeline for data processing.
Gets a path to a folder with all conversation transcripts in JSON format.
Cleans the data and returns a pandas dataframe with all utterances from all conversations.
"""
import os
from data_pipeline_functions import (import_data,
                                     clean_data,
                                     nlp_preprocessing,
                                     identify_care_manager)
from src.utils.common import get_project_root


# Getting folder's path
project_root = get_project_root()
raw_files_path = os.path.join(project_root, 'data', 'raw_files')
cities_file = os.path.join(project_root, 'src', 'data', 'us_cities.csv')


# Importing data
raw_df = import_data(raw_files_path)
df = raw_df.copy()

# Identify CM and add Boolean column to the df
df = identify_care_manager(df)

# Cleaning data
df = clean_data(df, cities_file=cities_file, cities_threshold=3)


print(df.columns)
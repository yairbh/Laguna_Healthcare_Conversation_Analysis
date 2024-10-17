"""
This script merges multiple JSON files from a specified folder into a single JSON file. It performs the following operations:
1. Reads JSON files from a given source folder.
2. Merges the content of all JSON files into a single JSON object.
3. Writes the merged JSON content to a specified target file.
"""

import json
import os
from src.utils.common import get_project_root

def merge_json_files(source_folder_path, target_file_path):
    '''
    This function takes as input a folder path with JSON files
    and creates a new JSON file that includes the content
    of all files in the folder.
    The string 'target_file_path' should include ".json"

    General structure of the output file:
    #####################################

    Root Object (Dictionary)
    |
    |-- Filename (=entire conversation) (Dictionary)
    |   |-- Transcript (=entire conversation) (List)
    |       |-- Utterance (Dictionary)
    |           |-- Speaker (String)
    |           |-- Time (Integer)
    |           |-- Text (String)
    |           |-- ID (String)
    |
    |       |-- Utterance (Dictionary)
    |           |-- Speaker (String)
    |           |-- Time (Integer)
    |           |-- Text (String)
    |           |-- ID (String)
    |       ...
    |
    |-- Filename (=entire conversation) (Dictionary)
    |   |-- Transcript (List)
    |       |-- Utterance (Dictionary)
    |           |-- Speaker (String)
    |           |-- Time (Integer)
    |           |-- Text (String)
    |           |-- ID (String)
    |       ...
    ...

    #####################################

    '''

    # Get a list of all files in the folder
    file_names = os.listdir(source_folder_path)

    # Filter out only the JSON files
    json_files = [file for file in file_names if file.endswith('.json')]
    files_count = len(json_files)

    # Read each JSON file in the folder and save the data
    data = {}
    for source_file_name in json_files:
        source_file_path = os.path.join(source_folder_path, source_file_name)

        with open(source_file_path, 'r') as source_file:
            data[source_file_name] = json.load(source_file)

    with open(target_file_path, 'w') as target_file:
        json.dump(data, target_file, indent=4)

    print(f'Finished loading content of {files_count} files')

project_root = get_project_root()
source_folder_path = os.path.join(project_root, 'data', 'raw_files')
target_file_path = os.path.join(project_root, 'data', 'processed', 'merged_conversations', 'all_conversations_merged.json')
merge_json_files(source_folder_path, target_file_path)

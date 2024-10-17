### NOT UPDATED ###

"""
This script processes JSON files containing conversation details and organizes them
by patient ID into separate folders.

The script performs the following steps:
1. Reads JSON files from the source folder (NOTE: these should be the processed files after 'initial JSON extraction.py')
2. Extracts the patient ID from each JSON file.
3. Creates a new folder for each patient ID in the target folder.
4. Copies the JSON files to the corresponding patient ID folders.

NOTE: notice the source and target folder paths
"""

import json
import os
import shutil
from src.utils.common import get_project_root, create_folder

# Source and target folders
project_root = get_project_root()
source_folder_path = os.path.join(project_root, 'data', 'only_long_convs')
target_folder_path = os.path.join(project_root, 'data', 'sorted_by_patients')
create_folder(target_folder_path)

# Get a list of all files in the folder
file_names = os.listdir(source_folder_path)

# Filter out only the JSON files
json_files = [file for file in file_names if file.endswith('.json')]

# Process each JSON file in the folder
for source_file_name in json_files:
    source_file_path = os.path.join(source_folder_path, source_file_name)

    with open(source_file_path, 'r') as source_file:
        data = json.load(source_file)
        patient_id = data['conv_details']['patient_id']

        # Create a new folder for the patient_id if it doesn't exist
        patient_folder_path = os.path.join(target_folder_path, str(patient_id))
        create_folder(patient_folder_path)

        # Copy the file to the patient folder
        target_file_path = os.path.join(patient_folder_path, source_file_name)
        shutil.copy(source_file_path, target_file_path)
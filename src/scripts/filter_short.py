### NOT UPDATED ###

"""
This script filters JSON files based on the number of utterances they contain and copies the selected files to a
new folder.

The script performs the following steps:
1. Reads JSON files from the source folder, each containing processed conversation data.
2. Extracts the number of utterances from each JSON file.
3. Filters files based on a threshold value for utterance count, retaining only those with a count above the threshold.
4. Copies the selected files to a new folder, creating a collection of files with long conversations.

NOTE: notice the source and target folder paths
"""

import json
import os
import shutil
from src.utils.common import get_project_root, create_folder

# Source and target folders
project_root = get_project_root()
source_folder_path = os.path.join(project_root, 'data', 'processed_files')
target_folder_path = os.path.join(project_root, 'data', 'only_long_convs')
create_folder(target_folder_path)

# Get a list of all files in the folder
file_names = os.listdir(source_folder_path)

# Filter out only the JSON files
json_files = [file for file in file_names if file.endswith('.json')]

utterance_threshold = 10
good_files = []

# Process each JSON file in the folder
for source_file_name in json_files:
    source_file_path = os.path.join(source_folder_path, source_file_name)

    with open(source_file_path, 'r') as source_file:
        data = json.load(source_file)
        ut_count = data['statistics']['utterances_count']

        if ut_count > utterance_threshold:
            good_files.append(source_file_name)

# Copy files from source to target folder
for file_name in good_files:
    source_file_path = os.path.join(source_folder_path, file_name)
    target_file_path = os.path.join(target_folder_path, file_name)
    shutil.copy(source_file_path, target_file_path)

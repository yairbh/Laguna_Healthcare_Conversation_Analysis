"""
This script processes conversation data stored in JSON format and converts it into a structured CSV file. It performs the following operations:
1. Loads JSON data from a specified file path.
2. Processes the conversation data by extracting relevant details and calculates the duration of each utterance.
3. Converts the processed data into a pandas DataFrame.
4. Saves the DataFrame to a CSV file for further analysis.
"""

import json
import numpy as np
import pandas as pd
import os
from src.utils.common import load_json_data


# Function to process conversation data and convert it to a DataFrame
def process_conversations(data):
    data_for_dataframe = []
    for file, content in data.items():
        member_id, recording_id = file.split('_')
        recording_id = recording_id.split('.')[0]
        utterances = content['transcript']
        times = []
        start_index = len(data_for_dataframe)
        for utterance in utterances:
            data_for_dataframe.append({
                "file_name": file,
                "recording_id": recording_id,
                "member_id": member_id,
                'utterance_id': utterance['id'],
                'speaker': utterance['speaker'][-1],
                'time': utterance['time'],
                'text': utterance['text']
            })
            times.append(utterance['time'])
        if times:
            times = np.array(times)
            times_shifted = np.append(times[1:], 0)
            durations = times_shifted - times
            for ind in range(len(durations)):
                data_for_dataframe[start_index + ind]['duration'] = durations[ind]
        else:
            for ind in range(start_index, len(data_for_dataframe)):
                data_for_dataframe[ind]['duration'] = None
    return pd.DataFrame(data_for_dataframe)

# Main script execution
if __name__ == "__main__":
    # Determine the project's root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


    # Define the relative paths
    source_file_path = os.path.join(project_root, 'data', 'raw_files', 'merged_conversations', 'all_conversations_raw_files.json')
    output_file_path = os.path.join(project_root, 'data', 'processed', 'all_raw_utterances_df.csv')

    # Load and process the data
    data = load_json_data(source_file_path)
    all_data_df = process_conversations(data)

    # Save the DataFrame to a CSV file
    all_data_df.to_csv(output_file_path, index=False)

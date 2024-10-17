"""
This script processes a JSON file containing raw_files conversation data from multiple files.

The script extracts relevant metrics for each conversation.
These metrics are compiled into a pandas DataFrame and exported to a csv file.
Each row in the DataFrame represents one conversation.
"""

import json
import pandas as pd
import re
from src.utils.common import get_project_root
import os

def _count_single_question_marks(text):
    text = text.replace(' ', '')
    pattern = r'(\? *)(?!\?)'
    matches = re.findall(pattern, text)
    return len(matches)

project_root = get_project_root()
source_file_path = os.path.join(project_root, 'data', 'raw_files', 'merged_conversations', 'all_conversations_raw_files.json')
with open(source_file_path, 'r') as source_file:
    data = json.load(source_file)

data_for_dataframe = []

for file, content in data.items():  # iterate through each file
    patient_id, recording_id = file.split('_')
    recording_id = recording_id.split('_')
    utterances = content['transcript']
    num_of_utterances = len(utterances)
    min_utterance_length = float('inf')
    max_utterance_length = 0
    min_utterance_duration = float('inf')
    max_utterance_duration = 0
    speakers_in_conversation = set()
    previous_utterance_starting_time = 0
    conversation_duration = 0
    previous_speaker = None
    questions_count = {}
    time_count = {}

    for utterance in utterances:  # Iterate all utterances in each of the files
        current_speaker = utterance['speaker'][-1]
        speakers_in_conversation.add(current_speaker)
        time_count[current_speaker] = 0
        current_text = utterance['text']
        utterance_length = len(current_text.split())
        min_utterance_length = min(min_utterance_length, utterance_length)
        max_utterance_length = max(max_utterance_length, utterance_length)

        previous_utterance_duration = utterance['time'] - previous_utterance_starting_time
        previous_utterance_starting_time = utterance['time']
        min_utterance_duration = min(min_utterance_duration, previous_utterance_duration)
        max_utterance_duration = max(max_utterance_duration, previous_utterance_duration)
        conversation_duration += previous_utterance_duration
        time_count[previous_speaker] = time_count.get(previous_speaker, 0) + previous_utterance_duration
        previous_speaker = current_speaker

        question_marks_count = _count_single_question_marks(current_text)
        if question_marks_count > 0:
            questions_count[current_speaker] = questions_count.get(current_speaker, 0) + question_marks_count

    if num_of_utterances == 0:
        min_utterance_length = 0
        max_utterance_length = 0
        min_utterance_duration = 0
        max_utterance_duration = 0

    talk_listen_ratio = {
        speaker: time_count.get(speaker, 0) / conversation_duration
        for speaker in speakers_in_conversation if conversation_duration != 0
    }

    speaker_with_highest_talk_listen_ratio = max(talk_listen_ratio, key=talk_listen_ratio.get, default=None)
    speaker_with_max_question_marks = max(questions_count, key=questions_count.get, default=None)

    # Append data for each file to the list (will be rows in the dataframe)
    data_for_dataframe.append({
        "file_name": file,
        "recording_id": recording_id,
        "patient_id": patient_id,
        "num_of_utterances": num_of_utterances,
        "conversation_duration": conversation_duration,
        "num_of_speakers": len(speakers_in_conversation),
        "min_utterance_length": min_utterance_length,
        "max_utterance_length": max_utterance_length,
        "min_utterance_duration": min_utterance_duration,
        "max_utterance_duration": max_utterance_duration,
        "speaker_with_max_question_marks": speaker_with_max_question_marks,
        "speaker_with_highest_talk_listen_ratio": speaker_with_highest_talk_listen_ratio
    })

# Create DataFrame
df = pd.DataFrame(data_for_dataframe)

# Save DataFrame to CSV
output_file_path = os.path.join(project_root, 'data', 'processed', 'all_convs_with_statistics_df.csv')
df.to_csv(output_file_path, index=False)

print(f"DataFrame saved to {output_file_path}")
print(df.head())

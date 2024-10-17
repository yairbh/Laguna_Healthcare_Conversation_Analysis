### NOT UPDATED ###

"""
This script processes raw_files JSON files containing conversation details, calculates various statistics, and saves the
processed data to new JSON files.

The script performs the following steps:
1. Reads JSON files from the source folder, each containing conversation data. (NOTE: should receive raw_files, unprocessed,
   JSON files)
2. Extracts information such as patient ID, speaker details, and transcript from each JSON file.
3. Calculates statistics such as word count, question count, and speaker duration.
4. Creates a new JSON object containing the processed data and writes it to new JSON files in the target folder.

NOTE: notice the source and target folder paths
"""
import json
import os
import re
from src.utils.common import get_project_root, create_folder

def count_single_question_marks(text):
    text = text.replace(' ', '')
    pattern = r'(\? *)(?!\?)'  # look for '?' (one or more in a row, ignoring whitespaces)
    matches = re.findall(pattern, text)
    return len(matches)

# Source and target folders
project_root = get_project_root()
source_folder_path = os.path.join(project_root, 'data', 'raw_files', 'merged_conversations')
target_folder_path = os.path.join(project_root, 'data', 'processed')
create_folder(target_folder_path)

# Get a list of all files in the folder
file_names = os.listdir(source_folder_path)

# Filter out only the JSON files
json_files = [file for file in file_names if file.endswith('.json')]
files_count = len(json_files)

# Process each JSON file in the folder
for source_file_name in json_files:
    source_file_path = os.path.join(source_folder_path, source_file_name)
    target_file_name = os.path.splitext(source_file_name)[0] + '_PROCESSED.json'
    target_file_path = os.path.join(target_folder_path, target_file_name)  # Define target file path here

    with open(source_file_path, 'r') as source_file:
        data = json.load(source_file)
        data['entire_text'] = []  # new entire_text list
        data['statistics'] = {}  # new statistics dictionary

        patient_id, recording_id = source_file_name.split('_')
        patient_id = patient_id.split('.')[0]  # what?
        # new conversation details dictionary:
        data['conv_details'] = {'patient_id': patient_id, 'recording_id': recording_id}

        ut_count = len(data['transcript'])
        words_count = {}
        questions_count = {}
        time_count = {}
        previous_utterance_starting_time = 0
        previous_speaker = None

        for utterance in data['transcript']:
            current_speaker = utterance['speaker'][-1]  # gets the last character in speaker's name
            current_text = utterance['text']
            word_count = len(current_text.split())
            question_marks_count = count_single_question_marks(current_text)

            # Calculating previous utterance duration using current utterance time
            if previous_speaker is not None:
                previous_utterance_duration = utterance['time'] - previous_utterance_starting_time
                previous_utterance_starting_time = utterance['time']
                time_count[previous_speaker] = time_count.get(previous_speaker, 0) + previous_utterance_duration  # adds previous duration to previous speaker's total duration count
            previous_speaker = current_speaker

            words_count[current_speaker] = words_count.get(current_speaker, 0) + word_count  # adds current word_count to speaker's total word count
            if question_marks_count > 0:  # only when the current utterance includes a question
                questions_count[current_speaker] = questions_count.get(current_speaker, 0) + question_marks_count

            line = current_speaker + ': ' + current_text  # rewrites the utterance in an easy to read format
            data['entire_text'].append(line)

        speakers = sorted(words_count.keys())
        speakers_count = len(speakers)  # number of speakers identified by the auto-transcription
        total_time = sum(time_count.values())  # total time of conversation

        # Creating statistics dictionary entries:
        avg_word_duration = {}
        talk_listen_ratio = {}
        for speaker in speakers:
            speaker_time_count = time_count.get(speaker)
            if speaker_time_count is not None:
                avg_word_duration[speaker] = words_count[speaker] / time_count[speaker] if time_count[speaker] != 0 else 'N/A'
                talk_listen_ratio[speaker] = time_count[speaker] / total_time if total_time != 0 else 'N/A'

        data['statistics']['avg_word_duration'] = avg_word_duration
        data['statistics']['talk_listen_ratio'] = talk_listen_ratio
        data['statistics']['speakers_count'] = speakers_count
        data['statistics']['utterances_count'] = ut_count
        data['statistics']['words_count'] = words_count
        data['statistics']['questions_count'] = questions_count
        data['statistics']['time_count'] = time_count
        if questions_count:
            data['statistics']['care_manager'] = max(questions_count, key=questions_count.get)
        else:
            data['statistics']['care_manager'] = 'N/A'

        with open(target_file_path, 'w') as target_file:  # write the modified 'data' dictionary into the new target JSON file
            json.dump(data, target_file, indent=4)

print(f'Finished processing {files_count} files')

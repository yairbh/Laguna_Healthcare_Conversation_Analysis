"""
This is the main pipeline for data processing.
Gets all conversations each in a JSON file.
Returns a Pandas DataFrame containing the clean data.

Conversations are both filtered and fixed in this file.
"""

# TODO: function: get only 2 speakers - clean excessive and remove convs wtih 1 speaker

import numpy as np
import pandas as pd
import os
import json
import regex as re

# Data
# todo: organize data import functions from raw_files json
from src.utils.common import (get_project_root,
                              load_json_data)

# Functions to fix de-identification issues
from src.data.fixes_modify_df import (fix_apostrophes,
                             fix_strings_with_I,
                             fix_portland)

# Filter short conversations
from src.data.fixes_filter import get_long_convs


def add_file_data_to_data_list(file: str, content: dict,
                               data_for_dataframe: list):
    """
    Unpacks file data into the data_for_dataframe list
    :param file: File name.
    :param content: A dictionary with key: transcript, value: list of dictionaries containing the data of all utterances
                    of the transcript
    :param data_for_dataframe: The list of unpacked utterances data to be updated
    :returns: Updates the list 'data_for_dataframe'.
    """
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

    return data_for_dataframe


def import_data(folder_path):
    """
    Unpack all json files into a Pandas DataFrame.
    :param folder_path: Path of the folder containing the json files.
    """

    data_for_dataframe = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        content = load_json_data(file_path)
        file = filename.split('.')[0]
        add_file_data_to_data_list(file, content,
                                   data_for_dataframe)

    raw_df = pd.DataFrame(data_for_dataframe)
    return raw_df


def clean_data(raw_df: pd.DataFrame, cities_file, cities_threshold=3):
    """
    :type raw_df: input utterances dataframe to be processed
    :param cities_file: path of csv file with US cities names (for fix_portland function)
    :param cities_threshold: for fix_portland function
    """
    def clean_de_identification(df: pd.DataFrame, cities_file, cities_threshold):
        """
        Run all functions that fix de-identification problems.
        """
        df_copy = df.copy()
        df_copy = fix_apostrophes(df_copy, plot_cases=False)
        df_copy = fix_strings_with_I(df_copy)
        df_copy = fix_portland(df_copy, cities_file=cities_file, cities_threshold=cities_threshold)
        return df_copy

    def clean_conversations(df: pd.DataFrame):
        """
        Filter utterances by conditions from different functions according to need.
        """
        # todo: function to filter short convs with long utterances (answering machine)
        df_copy = df.copy()
        # Filter long conversations and answering machines
        recordings_to_keep = list(set(get_long_convs(df_copy))) # & set(NEW FUNCTION))
        df_copy = df_copy[df_copy['recording_id'].isin(recordings_to_keep)]
        return df_copy

    df = raw_df.copy()
    df = clean_de_identification(df, cities_file=cities_file, cities_threshold=cities_threshold)
    df = clean_conversations(df)
    return df


def identify_care_manager(df: pd.DataFrame):
    """
    Identifies the care manager in a dataset of conversation transcripts.

    This function processes a DataFrame containing conversation transcripts and identifies
    the care manager based on the following criteria:
    1. The speaker has lines with the word 'recorded'.
    2. The speaker has the maximum number of single question marks in the conversation.

    The function creates and returns a new DataFrame with an additional column 'is_cm'
    indicating whether the speaker is identified as the care manager.

    Args:
    df (pd.DataFrame): The input DataFrame with columns 'recording_id', 'speaker', and 'text'.

    Returns:
    pd.DataFrame: A copy of the input DataFrame with an added column 'is_cm'
                  indicating the identified care manager.
    """
    def _count_single_question_marks(row_text):
        text = row_text.replace(' ', '')
        pattern = r'(\? *)(?!\?)'
        matches = re.findall(pattern, text)
        return len(matches)

    def _has_recorded(row_text):
        return 'recorded' in row_text.lower()


    # Create copies of the data frame
    df_temp = df.copy()

    # Count question marks and check for 'recorded'
    df_temp['num_of_qmarks'] = df_temp['text'].apply(_count_single_question_marks)
    df_temp['has_recorded'] = df_temp['text'].apply(_has_recorded)

    # Aggregate information by recording_id and speaker
    agg_funcs = {
        'num_of_qmarks': 'sum',
        'has_recorded': 'sum'
    }
    df_agg = df_temp.groupby(['recording_id', 'speaker']).agg(agg_funcs).reset_index()

    # Determine the speaker with the maximum question marks per recording
    df_agg['max_qmarks'] = df_agg.groupby('recording_id')['num_of_qmarks'].transform('max')
    df_agg['is_speaker_with_max_qmarks'] = df_agg['num_of_qmarks'] == df_agg['max_qmarks']

    # Determine the speaker with 'recorded' in their utterances per recording
    df_agg['is_speaker_with_recorded'] = df_agg['has_recorded'] > 0

    # Resolve conflicts: prioritize 'recorded' over max question marks
    df_agg['priority'] = df_agg['is_speaker_with_recorded'].astype(int) * 2 + df_agg[
        'is_speaker_with_max_qmarks'].astype(int)
    df_agg['is_cm'] = df_agg.groupby('recording_id')['priority'].rank(method='first', ascending=False) == 1

    # Merge the 'is_cm' flag back to the original dataframe
    df_result = df.merge(df_agg[['recording_id', 'speaker', 'is_cm']], on=['recording_id', 'speaker'], how='left')

    return df_result


def nlp_preprocessing(df: pd.DataFrame):
    # todo: documentation
    # todo:
    #    for each utterance in the dataframe:
    #       tokenize
    #       lemmatize
    #       stop words
    #       create a new column with processed utterance

    pass


def main():
    # Getting folder's path
    project_root = get_project_root()
    folder_path = os.path.join(project_root, 'data', 'raw_files')

    # Importing data
    raw_df = import_data(folder_path)

if __name__ == '__main__':
    main()
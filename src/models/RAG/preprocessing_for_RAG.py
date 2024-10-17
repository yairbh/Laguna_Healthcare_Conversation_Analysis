"""
Preprocessing for RAG:
1. Receives df with utterances.
2. Adds a column with "Speaker #" + text.
3. Joins the combined utterances into a single text per recording_id.
4. Returns a dictionary with enrire text for each recording.
"""

import pandas as pd

from src.data.fixes_filter import get_long_convs
from src.utils.constants import raw_data_df


def preprocess_for_RAG(dataframe: pd.DataFrame, enumerate_file_names=False) -> dict:
    """
    Main function to preprocess the dataframe for RAG model.

    :param dataframe: DataFrame containing the utterances (from one or more recording_ids).
    :returns: A dictionary with recording_id (keys) and concatenated utterance texts (values).
    """
    df = dataframe.copy()
    df = combine_speaker_and_text(df)
    full_text_per_recording_id = concatenate_all_recordings(df)

    # Replace recording id with an enumerated index in the format "recording#" where # is a running number.
    if enumerate_file_names:
        enumerated_full_text_per_recording_id = {f'recording{i}': value for i, value in enumerate(full_text_per_recording_id.values())}
        return enumerated_full_text_per_recording_id

    return full_text_per_recording_id


def combine_speaker_and_text(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess each utterance in the dataframe by combining the speaker letter with the utterance text.

    :param dataframe: Dataframe containing 'speaker' and 'text' columns.
    :return: A modified dataframe with a new column 'text_with_speaker'.
    """
    df = dataframe.copy()
    df['text_with_speaker'] = df.apply(
        lambda row: 'Speaker ' + row['speaker'] + ': ' + row['text'], axis=1
    )
    return df


def concatenate_all_recordings(dataframe):
    """
    Processes each recording in the dataframe separately and concatenates text segments into a single text.

    :param dataframe: DataFrame containing the utterances.
    :returns: A dictionary with recording_id (keys) and concatenated utterance texts (values).
    """
    full_text_per_recording_id = {}
    for recording_id, subset_of_utterances in dataframe.groupby('recording_id'):
        full_text_per_recording_id[recording_id] = " ".join(subset_of_utterances['text_with_speaker'].tolist())
    return full_text_per_recording_id


if __name__ == '__main__':
    # Example usage

    # Load raw dataframe
    df = raw_data_df.copy()

    # Filter long conversations
    # todo maybe set here a threshold?
    recordings_to_keep = list(set(get_long_convs(df)))
    df = df[df['recording_id'].isin(recordings_to_keep)]

    full_text_per_recording_id = preprocess_for_RAG(df)
    enumerated_full_text_per_recording_id = preprocess_for_RAG(df, enumerate_file_names=True)

    print('Example:')
    example_recording_id = list(full_text_per_recording_id.keys())[5]
    example_full_text = full_text_per_recording_id[example_recording_id]
    print(f'Recording_id: {example_recording_id}')
    print(f'Full text: {example_full_text[:500]}...')  # Print the first 500 characters for brevity

pass
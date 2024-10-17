from src.utils.constants import raw_data_df
import pandas as pd
import plotly.express as px


def read_conv(df: pd.DataFrame, recording_id):
    df = df.loc[df['recording_id'] == recording_id, ['speaker', 'text']]
    df['combined'] = df['speaker'] + ': ' + df['text']
    entire_conv = '\n'.join(df['combined'])
    return entire_conv


# Get a list of long conversations (above threshold number of utterances)
def get_long_convs(df: pd.DataFrame, min_num_of_utterances=11):
    grouped = df.groupby('recording_id').size()
    long_convs = grouped[grouped >= min_num_of_utterances]
    return long_convs.index.to_list()


# Get a list of short conversations (below threshold of number of utterances)
def get_short_convs(df: pd.DataFrame, max_number_of_utterances=10):
    grouped = df.groupby('recording_id').size()
    short_convs = grouped[grouped <= max_number_of_utterances]
    return short_convs.index.to_list()


# Get a list of short conversations with long duration
def get_short_convs_with_long_duration(df: pd.DataFrame, min_total_duration, max_number_of_utterances=5):
    convs_with_few_utterances = get_short_convs(df, max_number_of_utterances)
    convs_with_long_total_duration = df.loc[df['duration'] < -min_total_duration, 'recording_id'].to_list()
    short_convs_with_long_duration = list(set(convs_with_few_utterances) & set(convs_with_long_total_duration))
    return short_convs_with_long_duration


# Get a list of conversations that include very long-duration utterances
def get_convs_with_long_utterances(df: pd.DataFrame, max_utterance_duration):
    convs = df.loc[df['duration'] > max_utterance_duration, 'recording_id'].to_list()
    return convs


def plot_duration_vs_utterances(df: pd.DataFrame): #TODO use it to check weird/extreem/outliers cases
    """
    Plots the correlation between the total duration of a recording_id and the number of utterances in this recording_id.
    Displays the recording_id when hovering over a datapoint.

    Args:
        df (pd.DataFrame): The input DataFrame with columns 'recording_id' and 'duration'.
    """
    # Extract total duration for each recording_id (absolute value of negative duration)
    total_durations = df[df['duration'] < 0].copy()
    total_durations['total_duration'] = total_durations['duration'].abs()

    # Count the number of utterances for each recording_id
    num_utterances = df.groupby('recording_id').size().reset_index(name='num_utterances')

    # Merge the total duration and number of utterances dataframes
    merged_df = pd.merge(total_durations[['recording_id', 'total_duration']], num_utterances, on='recording_id')

    # Create the scatter plot using Plotly
    fig = px.scatter(merged_df, x='num_utterances', y='total_duration', hover_data=['recording_id'],
                     labels={'num_utterances': 'Number of Utterances', 'total_duration': 'Total Duration'},
                     title='Correlation between Total Duration and Number of Utterances')

    # Show the plot
    fig.show()


def get_convs_with_short_avg_utterance_duration(df: pd.DataFrame, threshold = 20) -> list:
    """
    Returns a list of recording IDs where the total duration divided by the number of rows
    for each recording_id is greater than the threshold.

    Args:
        df (pd.DataFrame): The input DataFrame with columns 'recording_id' and 'duration'.
        threshold (float): The duration threshold.

    Returns:
        list: A list of recording IDs with the calculated duration per row greater than the threshold.
    """
    # Calculate the total duration and the count of rows for each recording_id
    grouped = df.groupby('recording_id').agg(total_duration=('duration', 'sum'), count=('duration', 'size'))

    # Calculate the duration per row for each recording_id
    grouped['duration_per_row'] = grouped['total_duration'] / grouped['count']

    # Filter recording_ids where duration_per_row is greater than the threshold
    recording_ids_above_threshold = grouped[grouped['duration_per_row'] > threshold].index.tolist()

    return recording_ids_above_threshold


# plot_duration_vs_utterances(raw_data_df)

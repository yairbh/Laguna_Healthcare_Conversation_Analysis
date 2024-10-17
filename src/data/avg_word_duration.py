from src.utils.constants import raw_data_df
from src.data.fixes_modify_df import fix_apostrophes
import pandas as pd
import string
import plotly.express as px

#TODO maybe use it to find bad conversations with very long durations (like with answering machines)
def process_and_plot_avg_word_duration(df: pd.DataFrame, plot: bool = True) -> pd.DataFrame:
    """
    Process the DataFrame to calculate the average word duration and optionally plot the results.

    Args:
        df (pd.DataFrame): The input DataFrame with columns 'text' and 'duration'.
        plot (bool): If True, plot the results using Plotly.

    Returns:
        pd.DataFrame: The processed DataFrame with the average word duration calculated.
    """

    def get_avg_word_duration(df_row):
        words = df_row['text']
        words = words.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation before splitt
        words = words.split()
        num_of_words = len(words)
        duration = df_row['duration']

        if duration < 0:  # Negative duration represents final utterance of conversation
            duration = 0

        if num_of_words == 0:
            return 0
        else:
            return duration / num_of_words

    # Apply fixes and calculate average word duration
    new_df = fix_apostrophes(df)
    new_df['avg_word_duration'] = new_df.apply(get_avg_word_duration, axis=1)

    # Optionally plot the results
    if plot:
        fig = px.box(new_df, y='avg_word_duration', hover_data=['text', 'duration'])
        fig.show()

    return new_df


process_and_plot_avg_word_duration(raw_data_df)
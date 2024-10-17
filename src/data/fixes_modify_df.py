"""
This script includes all functions that fix problems in the raw_files data and return a modified dataframe.
They take as an input df and return df.
They can be used in a sequence (pipeline) to exert several modifications to a df.
"""

from src.utils.constants import raw_data_df
from src.utils.common import create_file_path
import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from collections import Counter


def fix_apostrophes(df: pd.DataFrame, plot_cases=False) -> pd.DataFrame:
    """
    Processes each row in the 'text' column of the DataFrame to replace problematic patterns
    with correct apostrophes. Optionally plots the counts of different contraction types.

    Args:
        df (pd.DataFrame): The input DataFrame with a 'text' column.
        plot_cases (bool): If True, plots the counts of different contraction types.

    Returns:
        pd.DataFrame: The DataFrame with corrected text in the 'text' column.
    """
    df_copy = df.copy()
    pattern = re.compile(r'([A-Z](?:\s[A-Z])+)(re|m|s|ll|ve|d|t|am)')
    case_counter = Counter()

    def replacement(match):
        case_counter[match.group(2)] += 1
        return "'" + match.group(2)

    def fix_text(text):
        return re.sub(pattern, replacement, text)

    df_copy['text'] = df_copy['text'].apply(fix_text)

    if plot_cases:
        cases = list(case_counter.keys())
        counts = list(case_counter.values())

        plt.figure(figsize=(10, 6))
        plt.bar(cases, counts, color='skyblue')
        plt.xlabel('Contraction Type')
        plt.ylabel('Count')
        plt.title('Counts of Different Contraction Types')
        plt.show()

    return df_copy


def fix_strings_with_I(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replaces specified strings in the 'text' column of the DataFrame with the word "I".

    Args:
        df (pd.DataFrame): The input DataFrame with a 'text' column.

    Returns:
        pd.DataFrame: The DataFrame with modified text in the 'text' column.
    """
    df_copy = df.copy()
    strings_to_replace = ["A M I R", "J A M E S", "H A D A S", "M I C H A E L",
                          "A I D E N A M E S", "N U N E Z", "A V A", "G A B I"]

    def replace_text(text):
        for string in strings_to_replace:
            text = text.replace(string, "I")
        return text

    df_copy['text'] = df_copy['text'].apply(replace_text)

    return df_copy


def fix_portland(df: pd.DataFrame, cities_file: str, cities_threshold=10, plot_cases=False) -> pd.DataFrame:
    """
    Processes a DataFrame to replace US city names with the word "Okay" based on specific criteria.

    Args:
        df (pd.DataFrame): The input DataFrame with a 'text' column and 'recording_id' column.
        cities_file (str): Path to the CSV file containing US city names.
        cities_threshold (int): Threshold for the number of city mentions to apply the replacement.
        plot_cases (bool): If True, plots the counts of different city names replaced.

    Returns:
        pd.DataFrame: The DataFrame with city names replaced by "Okay.".
    """
    df_copy = df.copy()

    if os.path.exists(cities_file):
        cities_df = pd.read_csv(cities_file)
    else:
        raise FileNotFoundError(f"File not found: {cities_file}")

    us_cities = cities_df['City'].tolist()
    pattern = '|'.join(re.escape(city) + r'[.,?]' for city in us_cities) # will look for city name + "." or "," or "?"

    # Initialize a counter to keep track of different city names replaced
    city_counter = Counter()

    df_copy['us_city'] = df_copy['text'].str.extract(f'({pattern})', expand=False)
    only_convs_with_cities = df_copy[['recording_id', 'us_city']].dropna(subset=['us_city'])

    cities_count_per_conv = only_convs_with_cities.pivot_table(
        index='recording_id',
        columns='us_city',
        aggfunc='size',
        fill_value=0
    )

    cities_count_per_conv['top_city'] = cities_count_per_conv.idxmax(axis=1)
    cities_count_per_conv['num_mentions'] = cities_count_per_conv.max(axis=1, numeric_only=True)
    top_city_per_conv = cities_count_per_conv[['top_city', 'num_mentions']]
    filtered_recordings = top_city_per_conv[top_city_per_conv['num_mentions'] > cities_threshold].index

    for recording_id in filtered_recordings:
        top_city = top_city_per_conv.loc[recording_id, 'top_city']
        pattern = re.escape(top_city)
        # Count each replacement
        city_counter[top_city] += df_copy.loc[df_copy['recording_id'] == recording_id, 'text'].str.count(pattern).sum()

        df_copy.loc[df_copy['recording_id'] == recording_id, 'text'] = df_copy.loc[
            df_copy['recording_id'] == recording_id, 'text'].str.replace(pattern, 'Okay.', regex=True)

        # Plot the counts if requested
    if plot_cases:
        total_count = sum(city_counter.values())
        sorted_cities_counts = sorted(city_counter.items())
        cities, counts = zip(*sorted_cities_counts)

        plt.figure(figsize=(10, 6))
        plt.bar(cities, counts, color='skyblue')
        plt.xlabel('City Name')
        plt.ylabel('Count')
        plt.title('Counts of Different City Names Replaced', pad=20)
        plt.text(0.5, 1.02, f'Threshold = {cities_threshold} | Total Count: {total_count}', ha='center', transform=plt.gca().transAxes)
        plt.xticks(rotation=90)
        plt.show()

    return df_copy.drop('us_city', axis=1)

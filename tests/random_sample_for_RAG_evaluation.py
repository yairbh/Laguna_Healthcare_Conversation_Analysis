"""
Initial code for creating random samples of the classified (FLAN model) recordings for manual evaluation.
"""
from src.utils.common import create_file_path, get_project_root
import pandas as pd
import os

# input_file_path = create_file_path(['output', 'classified_recordings_RAG_FLAN_batch_1.csv'])
# output_file_path = create_file_path(['output', 'RAG_random_samples', 'RAG_random_samples_batch_1.csv'])


def concatenate_csv_files(folder_path, output_file_path):
    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Initialize an empty list to hold DataFrames
    dataframes = []

    # Read each CSV file and append the DataFrame to the list
    for csv_file in csv_files:
        csv_file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(csv_file_path)
        dataframes.append(df)

    # Concatenate all DataFrames
    concatenated_df = pd.concat(dataframes, ignore_index=True)

    # Save the concatenated DataFrame to a new CSV file
    concatenated_df.to_csv(output_file_path, index=False)


folder_path = create_file_path(['output'])
concatenated_file_path = create_file_path(['output', 'classified_recordings_combined.csv'])

# Concatenate CSV files
concatenate_csv_files(folder_path, concatenated_file_path)

# Load concatenated data
full_df = pd.read_csv(concatenated_file_path)


output_file_path = create_file_path(['output', 'RAG_random_samples', 'RAG_random_samples_batches_1_15.csv'])


# full_df = pd.read_csv(input_file_path)

# 100 samples in general
# rand_samples = original_df.sample(n=100, random_state=42)

# # Sample up to 10 samples per question_id
# rand_samples = full_df.groupby('question_id').apply(lambda x: x.sample(n=min(len(x), 10), random_state=42)).reset_index(drop=True)

# Function to sample up to 10 samples per question_id, ensuring both classes are represented
def stratified_sample(df, n, random_state=None):
    return df.groupby(['question_id', 'class'], group_keys=False).apply(lambda x: x.sample(n=min(len(x), n//2), random_state=random_state)).reset_index(drop=True)

# Sample up to 10 samples per question_id, ensuring both classes are represented
rand_samples = stratified_sample(full_df, 10, random_state=42)


rand_samples.drop(columns=['general_prompt', 'question_prompt'], inplace=True)

rand_samples.to_csv(output_file_path, index=False)
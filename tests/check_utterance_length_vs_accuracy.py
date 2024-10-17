import pandas as pd
import os
from src.utils.common import get_project_root
from src.models.Rule_Based.keywords_rule_based_classifier_V2 import clean_text
from src.utils.constants import MY_STOPS
from matplotlib import pyplot as plt

"""
This script evaluates the error rates of utterance classifications by their lengths.
It processes evaluation data from two experiments, identifies consistent misclassifications,
and plots the error rate distribution by utterance length. The script normalizes the utterance lengths
by calculating the error rates for each length bin, allowing for a fair comparison across different lengths.
"""


# Getting the project's root folder path
project_root = get_project_root()

# Constructing the file paths for the evaluation files
df1_evaluation_file_path = os.path.join(project_root, 'tests', 'evaluation_RB_exp1_complete.csv')
df2_evaluation_file_path = os.path.join(project_root, 'tests', 'evaluation_RB_exp2_complete.csv')

# Reading the CSV files into DataFrames
df1 = pd.read_csv(df1_evaluation_file_path)
df2 = pd.read_csv(df2_evaluation_file_path)

# Aggregate evaluation only on utterances said by the care manager
df1 = df1[df1['is_cm']]
df2 = df2[df2['is_cm']]

# Replace NaN values in the "prediction" column with "no_topic"
df1.loc[df1['prediction'].isna(), 'prediction'] = 'no_topic'

# Replace values in "Good prediction" with values from "Adir " where they exist
df1['Good prediction'] = df1['Adir '].combine_first(df1['Good prediction'])

# Drop the "Adir " column as it is no longer needed
df1.drop(columns=['Adir '], inplace=True)

# Rename "Good prediction" column to "model_is_correct"
df1.rename(columns={'Good prediction': 'model_is_correct'}, inplace=True)

# Merge dataframes
df_combined = df1.merge(
    right=df2[['utterance_id', 'prediction', 'model_is_correct']],
    on='utterance_id',
    how='outer',
    suffixes=['_exp1', '_exp2']
)

# Apply the clean_text function to the text column
df_combined['clean_text'] = df_combined['text'].apply(lambda text: clean_text(text, MY_STOPS))

# Calculate text length after cleaning
df_combined['text_length'] = df_combined['clean_text'].apply(lambda text: len(text.split()))

# Identify consistent misclassifications
df_consistent_misclassifications = df_combined[(df_combined['model_is_correct_exp1'] == 0) & (df_combined['model_is_correct_exp2'] == 0)]

# Create bins for text lengths
bins = range(0, df_combined['text_length'].max() + 10, 10)  # Adjust bin size as needed

# Calculate the total number of utterances and the number of misclassified utterances for each bin
df_combined['length_bin'] = pd.cut(df_combined['text_length'], bins=bins)
df_consistent_misclassifications['length_bin'] = pd.cut(df_consistent_misclassifications['text_length'], bins=bins)

total_counts = df_combined['length_bin'].value_counts().sort_index()
error_counts = df_consistent_misclassifications['length_bin'].value_counts().sort_index()

# Compute the error rate for each bin
error_rate = (error_counts / total_counts).fillna(0)

# Plot the error rates
plt.figure(figsize=(10,6))
error_rate.plot(kind='bar')
plt.xlabel('Text Length (binned)')
plt.ylabel('Error Rate')
plt.title('Error Rate by Utterance Length')
plt.show()

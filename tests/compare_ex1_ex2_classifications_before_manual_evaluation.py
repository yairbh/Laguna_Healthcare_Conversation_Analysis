"""
This script compares classifications from two experiments and creates a new CSV file with evaluations copied from
experiment 1 to experiment 2 for rows where classifications remain unchanged. This assists in manually evaluating
experiment 2 results.

Steps:
1. Load data from CSV files for experiment 1 and experiment 2.
2. Process experiment 1 data by filling missing predictions and combining evaluation columns.
3. Filter rows in both dataframes where `is_cm` is True.
4. Identify rows from experiment 1 that are not present in experiment 2.
5. Create a mapping of `utterance_id` to 'Good prediction' from experiment 1.
6. Add 'df1_good_prediction' and 'df1_prediction' columns to experiment 2 data.
7. Compare predictions and copy evaluations for rows where classifications are unchanged.
8. Save the processed dataframe to a new CSV file.

"""

import pandas as pd

# Load Data
df1 = pd.read_csv('C:\\Users\\yairb\\PycharmProjects\\Laguna_June\\tests\\evaluation_RB_exp1_complete.csv')
print(df1.columns)

# Process df1
df1.loc[df1['prediction'].isna(), 'prediction'] = 'no_topic'
df1['Good prediction'] = df1['Adir '].combine_first(df1['Good prediction'])
df1.drop(columns=['Adir '], inplace=True)

print("DataFrame columns after processing:", df1.columns)
print(df1[df1['is_cm']].shape)

# Load df2
df2 = pd.read_csv('C:\\Users\\yairb\\PycharmProjects\\Laguna_June\\tests\\classified_utterances_RB_exp2.csv')
print(df2[df2['is_cm']].shape)

# Filter DataFrames
df1_cm = df1[df1['is_cm']]
df2_cm = df2[df2['is_cm']]

# Identify rows in df1_cm not present in df2_cm based on utterance_id
df_leftout = df1_cm[~df1_cm['utterance_id'].isin(df2_cm['utterance_id'])]
print(df_leftout.columns)
print(df_leftout.shape)

# Create a dictionary to map utterance_id to Good prediction from df1_cm
good_prediction_dict = dict(zip(df1_cm['utterance_id'], df1_cm['Good prediction']))

# Create the good_prediction column in df2
df2['df1_good_prediction'] = df2.apply(
    lambda row: good_prediction_dict.get(row['utterance_id']) if row['is_cm'] else None,
    axis=1
)

# Ensure df1 and df2 are aligned on utterance_id for prediction column
df2 = df2.merge(df1[['utterance_id', 'prediction']], on='utterance_id', suffixes=('', '_df1'))
df2.rename(columns={'prediction_df1': 'df1_prediction'}, inplace=True)

# Define function to label correct predictions
def copy_only_certain_labels(row):
    if row['df1_good_prediction'] == 1 and row['df1_prediction'] == row['prediction']:
        return 1
    elif row['df1_good_prediction'] == 0 and row['df1_prediction'] == row['prediction']:
        return 0
    else:
        return None

# Apply function to create model_is_correct column
df2['model_is_correct'] = df2.apply(copy_only_certain_labels, axis=1)

# Drop temporary columns
df2.drop(['df1_good_prediction', 'df1_prediction'], axis=1, inplace=True)

# Save processed df2 to a CSV file
df2.to_csv('c:/Users/yairb/PycharmProjects/Laguna_June/tests/classified_utterances_RB_exp2_processed.csv', index=False)

print(df2.columns)
print(df2.shape)
print("that's it!")

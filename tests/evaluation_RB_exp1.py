"""
This script calculates the total accuracy and accuracy by topic from an evaluation file.

Steps:
1. Read the evaluation CSV file into a DataFrame.
2. Replace NaN values in the "prediction" column with "no_topic".
3. Combine values from the "Adir " column into the "Good prediction" column where they exist.
4. Drop the "Adir " column as it is no longer needed.
5. Calculate and print the total accuracy.
6. Calculate and print the accuracy by topic.
"""
import pandas as pd
import os
from src.utils.common import get_project_root

# Getting the project's root folder path
project_root = get_project_root()

# Constructing the file path for the evaluation file
# evaluation_file_path = os.path.join(project_root, 'tests', 'evaluation_RB_exp1.csv') #first (not complete) csv file)
evaluation_file_path = os.path.join(project_root, 'tests', 'evaluation_RB_exp1_complete.csv')

# Reading the CSV file into a DataFrame
df = pd.read_csv(evaluation_file_path)

# We will aggregate evaluation only on utterances said by the care manager
df = df[df['is_cm']]

# Print the columns of the DataFrame to verify the structure
print("DataFrame columns before processing:", df.columns)

# Replace NaN values in the "prediction" column with "no_topic"
df.loc[df['prediction'].isna(), 'prediction'] = 'no_topic'

# Replace values in "Good prediction" with values from "Adir " where they exist
df['Good prediction'] = df['Adir '].combine_first(df['Good prediction'])

# Drop the "Adir " column as it is no longer needed
df.drop(columns=['Adir '], inplace=True)

# Print the columns of the modified DataFrame to verify changes
print("DataFrame columns after processing:", df.columns)

# Calculate accuracy by topic by taking the mean of "Good prediction" for each topic
accuracy_by_topic = df.groupby('prediction')['Good prediction'].agg('mean')

# Calculate total accuracy by taking the mean of "Good prediction" across all rows
total_accuracy = df['Good prediction'].mean()
total_accuracy_without_no_topic = df.loc[df['prediction'] != 'no_topic', 'Good prediction'].mean()


# Print accuracy results
print('Total accuracy: ', total_accuracy)
print('Total accuracy without "no_topic": ', total_accuracy_without_no_topic)

print()
print('Accuracy by topic:')
print(accuracy_by_topic)

print('Total number of utterances: ', df.shape[0])
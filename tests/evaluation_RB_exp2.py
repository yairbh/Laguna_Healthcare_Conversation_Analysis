"""
This script calculates the total accuracy and accuracy by topic from an evaluation file.

Steps:
1. Read the evaluation CSV file into a DataFrame.
2. Calculate and print the total accuracy.
3. Calculate and print the accuracy by topic.
"""
import pandas as pd
import os
from src.utils.common import get_project_root

# Getting the project's root folder path
project_root = get_project_root()

# Constructing the file path for the evaluation file
evaluation_file_path = os.path.join(project_root, 'tests', 'evaluation_RB_exp2_complete.csv')

# Reading the CSV file into a DataFrame
df = pd.read_csv(evaluation_file_path)

# We will aggregate evaluation only on utterances said by the care manager
df = df[df['is_cm']]

# Print the columns of the DataFrame to verify the structure
print("DataFrame columns before processing:", df.columns)


# Calculate accuracy by topic by taking the mean of "Good prediction" for each topic
accuracy_by_topic = df.groupby('prediction')['model_is_correct'].agg('mean')

# Calculate total accuracy by taking the mean of "Good prediction" across all rows
total_accuracy = df['model_is_correct'].mean()
total_accuracy_without_no_topic = df.loc[df['prediction'] != 'no_topic', 'model_is_correct'].mean()

# Print accuracy results
print('Total accuracy: ', total_accuracy)
print('Total accuracy without "no_topic": ', total_accuracy_without_no_topic)
print()
print('Accuracy by topic:')
print(accuracy_by_topic)

print('Total number of utterances: ', df.shape[0])
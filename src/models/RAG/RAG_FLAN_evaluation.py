from src.utils.common import create_file_path, get_project_root
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
concatenated_file_path = create_file_path(['output', 'classified_recordings_combined.csv'])
full_df = pd.read_csv(concatenated_file_path)

# Map class to class_absolute, ensuring -9 is handled correctly
full_df['class_absolute'] = full_df['class'].map({0: 0, 1: 1, -9: 0})

# Filter out rows with class -9 before creating recording_class_question
filtered_df = full_df[full_df['class'] != -9]

# Create a new column for recording class per question_id
filtered_df['recording_class_question'] = filtered_df.groupby(['recording_id', 'question_id'])['class'].transform('max')

# Calculate the percentage of recording_ids with recording_class_question==1 for each question_id
percentage_df = filtered_df[filtered_df['recording_class_question'] == 1].groupby('question_id')['recording_id'].nunique().reset_index()
total_recordings_per_question = filtered_df.groupby('question_id')['recording_id'].nunique().reset_index()
total_recordings_per_question.columns = ['question_id', 'total_recordings']
percentage_df = percentage_df.merge(total_recordings_per_question, on='question_id')
percentage_df['percentage_recording_class_1'] = (percentage_df['recording_id'] / percentage_df['total_recordings']) * 100
percentage_df.drop(columns=['recording_id', 'total_recordings'], inplace=True)

# Ensure the order of question_id
question_order = ['Q1', 'Q2', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11']
percentage_df['question_id'] = pd.Categorical(percentage_df['question_id'], categories=question_order, ordered=True)
percentage_df = percentage_df.sort_values('question_id')

# Plot the results
plt.figure(figsize=(10, 6))
plt.bar(percentage_df['question_id'], percentage_df['percentage_recording_class_1'], color='skyblue')
plt.xlabel('Question ID')
plt.ylabel('Percentage of Recording Class 1')
plt.title('Percentage of Recording IDs with Recording Class 1 by Question ID')
plt.xticks(rotation=45)
plt.show()

######################
# Create a binary matrix indicating the presence of each question_id for each recording_id
binary_matrix = filtered_df.pivot_table(index='recording_id', columns='question_id', values='recording_class_question', aggfunc='max').fillna(0)
binary_matrix[binary_matrix > 0] = 1

# Ensure binary_matrix only contains 0s and 1s
binary_matrix = binary_matrix.astype(int)

# Initialize an empty DataFrame for the correlation matrix
question_ids = binary_matrix.columns
correlation_matrix = pd.DataFrame(index=question_ids, columns=question_ids, dtype=float)

# Calculate the percentage of recordings that have both question IDs
for question1 in question_ids:
    for question2 in question_ids:
        both_present = (binary_matrix[question1] & binary_matrix[question2]).sum()
        total_recordings = binary_matrix.shape[0]
        percentage = (both_present / total_recordings) * 100
        correlation_matrix.loc[question1, question2] = percentage

# Ensure the main diagonal is set to 100%
np.fill_diagonal(correlation_matrix.values, 100)

# Plot the correlation matrix
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=0, vmax=100)
plt.title('Percentage of Recordings with Both Questions')
plt.xlabel('Question ID')
plt.ylabel('Question ID')
plt.show()

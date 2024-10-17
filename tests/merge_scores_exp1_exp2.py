"""
This script calculates and visualizes the accuracy of predictions from two different experiments.

Steps:
1. **Calculate Accuracy**:
   - Reads evaluation files.
   - Filters data to include only care manager utterances.
   - Computes accuracy by topic and overall accuracy.

2. **Merge and Prepare Data**:
   - Merges accuracy results from both experiments.
   - Maps and updates topic names.
   - Orders topics correctly and fills NaN values.

3. **Plotting**:
   - Creates bar plots using Seaborn and Matplotlib.
   - First plot compares overall accuracy excluding "no_topic".
   - Second plot compares accuracy per topic between the two experiments.

The script provides visual comparisons to evaluate model performance across different topics and experiments.
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from src.utils.common import get_project_root

def calculate_accuracy(file_path, prediction_col='Good prediction'):
    """
    Calculate total accuracy and accuracy by topic from the given evaluation file.
    """
    # Reading the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # We will aggregate evaluation only on utterances said by the care manager
    df = df[df['is_cm']]

    # Print the columns of the DataFrame to verify the structure
    print("DataFrame columns before processing:", df.columns)

    # Replace NaN values in the "prediction" column with "no_topic"
    df.loc[df['prediction'].isna(), 'prediction'] = 'no_topic'

    # Replace values in "Good prediction" with values from "Adir " where they exist (for the first script)
    if 'Adir ' in df.columns:
        df['Good prediction'] = df['Adir '].combine_first(df['Good prediction'])
        # Drop the "Adir " column as it is no longer needed
        df.drop(columns=['Adir '], inplace=True)

    # Calculate accuracy by topic by taking the mean of the relevant column for each topic
    accuracy_by_topic = df.groupby('prediction')[prediction_col].agg('mean')
    total_accuracy = df[prediction_col].mean()
    total_accuracy_without_no_topic = df.loc[df['prediction'] != 'no_topic', prediction_col].mean()

    return accuracy_by_topic, total_accuracy, total_accuracy_without_no_topic

# Getting the project's root folder path
project_root = get_project_root()

# Constructing the file paths for the evaluation files
evaluation_file_path1 = os.path.join(project_root, 'tests', 'evaluation_RB_exp1_complete.csv')
evaluation_file_path2 = os.path.join(project_root, 'tests', 'evaluation_RB_exp2_complete.csv')

# Calculate accuracies for both files
accuracy_by_topic1, total_accuracy1, total_accuracy_without_no_topic1 = calculate_accuracy(evaluation_file_path1, 'Good prediction')
accuracy_by_topic2, total_accuracy2, total_accuracy_without_no_topic2 = calculate_accuracy(evaluation_file_path2, 'model_is_correct')

# Create a DataFrame to display total accuracies
accuracy_summary = pd.DataFrame({
    'Metric': ['Total accuracy', 'Total accuracy without "no_topic"'],
    'exp_1': [total_accuracy1, total_accuracy_without_no_topic1],
    'exp_2': [total_accuracy2, total_accuracy_without_no_topic2]
})

# Print the accuracy summary table
print('\nAccuracy Summary:')
print(accuracy_summary)

# Create DataFrames from the accuracy by topic results
df_accuracy1 = accuracy_by_topic1.reset_index().rename(columns={'Good prediction': 'accuracy_exp1'})
df_accuracy2 = accuracy_by_topic2.reset_index().rename(columns={'model_is_correct': 'accuracy_exp2'})

# Merge the results on the "prediction" column
merged_accuracy = pd.merge(df_accuracy1, df_accuracy2, on='prediction', how='outer')

# Print the merged accuracy results
print('\nMerged accuracy by topic:')
print(merged_accuracy)



### Creating plots ###

# Set the Seaborn style for the plots
sns.set(style="whitegrid")

# Define the order of topics for the plot, excluding 'no_topic'
topic_order = ['1', '2', '2+4', '1+2+4', '4', '5', '6', '7', '8', '9', '10']

# Update topic names for the merged accuracy DataFrame
topic_mapping = {
    '1_member_identification': '1',
    '2_call_recording_disclosure': '2',
    '2+4': '2+4',
    '1+2+4': '1+2+4',
    '4_cm_introduction': '4',
    '5_handling_phi': '5',
    '6_tcpa_compliance': '6',
    '7_sensitive_information_protocol': '7',
    '8_medical_consultation_advice': '8',
    '9_care_coordination': '9',
    '10_log_protocol': '10'
}

# Apply the corrected topic mapping
merged_accuracy['prediction'] = merged_accuracy['prediction'].map(topic_mapping)

# Drop any duplicates
merged_accuracy = merged_accuracy.drop_duplicates(subset=['prediction'])

# Remove 'no_topic' if present
merged_accuracy = merged_accuracy[merged_accuracy['prediction'].isin(topic_order)]

# Ensure the order of topics and fill NaN values with 0
merged_accuracy['prediction'] = pd.Categorical(merged_accuracy['prediction'], categories=topic_order, ordered=True)
merged_accuracy = merged_accuracy.set_index('prediction').reindex(topic_order).reset_index()
merged_accuracy[['accuracy_exp1', 'accuracy_exp2']] = merged_accuracy[['accuracy_exp1', 'accuracy_exp2']].fillna(0)

# Define a new color palette
color_palette = sns.color_palette("Paired", 12)

# Plot the overall accuracy comparison excluding "no_topic"
plt.figure(figsize=(10, 6))
sns.barplot(x=['Experiment 1', 'Experiment 2'], y=[total_accuracy_without_no_topic1, total_accuracy_without_no_topic2],
            palette=color_palette[:2])
plt.xlabel('Experiment', fontsize=14)
plt.ylabel('Accuracy', fontsize=14)
plt.title('Overall Accuracy Comparison (excluding "no_topic")', fontsize=16)
plt.ylim(0, 1)
for i, v in enumerate([total_accuracy_without_no_topic1, total_accuracy_without_no_topic2]):
    plt.text(i, v + 0.02, f"{v:.2f}", ha='center', fontsize=12)
plt.show()

# Plot accuracy per topic comparison between exp_1 and exp_2
plt.figure(figsize=(16, 9))
bar_width = 0.35
index = np.arange(len(topic_order))

# Plotting bars for exp_1 and exp_2 with a professional color palette
plt.bar(index, merged_accuracy['accuracy_exp1'], bar_width, label='Experiment 1', color=color_palette[2], edgecolor='k')
plt.bar(index + bar_width, merged_accuracy['accuracy_exp2'], bar_width, label='Experiment 2', color=color_palette[3], edgecolor='k')

plt.xlabel('Topics', fontsize=14)
plt.ylabel('Accuracy', fontsize=14)
plt.title('Exp1 vs. Exp2: Accuracy per Topic Comparison', fontsize=16)
plt.xticks(index + bar_width / 2, topic_order, rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=14)
plt.ylim(0, 1)
plt.tight_layout()
plt.show()

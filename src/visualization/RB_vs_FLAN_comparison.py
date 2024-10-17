"""
This script compares the accuracy of three experiments: two Rule-Based models (Experiment 1 and Experiment 2) and a FLAN-T5 model.
It generates two plots:
1. Overall accuracy comparison excluding "no_topic".
2. Accuracy per topic comparison between the three experiments.

The data for experiments 1 and 2 includes overall accuracy and accuracy per topic, while the FLAN-T5 model data includes overall accuracy and accuracy for specific questions.
The topics are mapped between the experiments and organized in a specific order for comparison.
The script uses Seaborn for styling and Matplotlib for plotting the bar charts.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Data for experiments 1 and 2 (Rule-Based Model)
accuracy_summary_exp1_exp2 = pd.DataFrame({
    'Metric': ['Total accuracy', 'Total accuracy without "no_topic"'],
    'exp_1': [0.470149, 0.153509],
    'exp_2': [0.676880, 0.208791]
})

merged_accuracy_exp1_exp2 = pd.DataFrame({
    'prediction': ['1+2+4', '10_log_protocol', '1_member_identification', '2+4', '2_call_recording_disclosure',
                   '3_participant_verification', '4_cm_introduction', '5_handling_phi', '6_tcpa_compliance',
                   '7_sensitive_information_protocol', '8_medical_consultation_advice', '9_care_coordination',
                   'no_topic'],
    'accuracy_exp1': [np.nan, 0.586207, 0.303030, np.nan, 0.500000, 0.000000, 0.067568, 0.100000, 0.016000, 0.052632, 0.000000, 0.269231, 0.885057],
    'accuracy_exp2': [0.300000, 0.330000, 0.264706, 0.700000, 0.000000, np.nan, 0.000000, 0.142857, np.nan, 0.018182, np.nan, np.nan, 0.964045],
    'best_experiment': [0.300000, 0.586207, 0.303030, 0.700000, 0.500000, 0.000000, 0.067568, 0.142857, 0.016000, 0.052632, 0.000000, 0.269231, 0.964045],
})

# Data for FLAN-T5_LARGE (third experiment)
accuracy_summary_flan_t5 = pd.DataFrame({
    'Metric': ['Total accuracy'],
    'FLAN-T5': [0.82]
})

accuracy_by_topic_flan_t5 = pd.DataFrame({
    'question': ['1', '2', '4', '5', '6', '7', '8', '9', '10', '11'],
    'accuracy_flan_t5': [0.93, 0.60, 0.60, 0.87, 0.87, 0.73, 0.80, 0.87, 1.00, 0.93]
})

# Mapping of topics between Rule-Based and FLAN-T5 experiments
topic_mapping = {
    '1_member_identification': '1',
    '2_call_recording_disclosure': '2',
    '4_cm_introduction': '4',
    '5_handling_phi': '5',
    '6_tcpa_compliance': '6',
    '7_sensitive_information_protocol': '7',
    '8_medical_consultation_advice': '8',
    '9_care_coordination': '9',
    '10_log_protocol': '10'
}

# Apply mapping to merged_accuracy_exp1_exp2
merged_accuracy_exp1_exp2['question'] = merged_accuracy_exp1_exp2['prediction'].map(topic_mapping)

# Preserve '11' as distinct topics
merged_accuracy_exp1_exp2['question'] = merged_accuracy_exp1_exp2.apply(
    lambda row: row['prediction'] if row['prediction'] in ['11'] else row['question'], axis=1)

# Drop 'no_topic' and '2+4', '1+2+4' from the data
merged_accuracy_exp1_exp2 = merged_accuracy_exp1_exp2[~merged_accuracy_exp1_exp2['question'].isin(['no_topic', '2+4', '1+2+4'])]

# Remove any duplicates in 'question' column
merged_accuracy_exp1_exp2 = merged_accuracy_exp1_exp2.drop_duplicates(subset=['question'])

# Merge the data from all three experiments
merged_accuracy = pd.merge(merged_accuracy_exp1_exp2, accuracy_by_topic_flan_t5, left_on='question', right_on='question', how='outer')

# Define the order of topics for the plot
topic_order = ['1', '2', '4', '5', '6', '7', '8', '9', '10', '11']

# Ensure the order of topics and fill NaN values with 0
merged_accuracy['question'] = pd.Categorical(merged_accuracy['question'], categories=topic_order, ordered=True)
merged_accuracy = merged_accuracy.set_index('question').reindex(topic_order).reset_index()
merged_accuracy[['best_experiment', 'accuracy_flan_t5']] = merged_accuracy[['best_experiment', 'accuracy_flan_t5']].fillna(0)

# Set Seaborn style
sns.set(style="white")

# Plot overall accuracy comparison for the three experiments
plt.figure(figsize=(10, 6))
sns.barplot(x=['Experiment 1', 'Experiment 2', 'FLAN-T5'], y=[
    accuracy_summary_exp1_exp2.loc[1, 'exp_1'],
    accuracy_summary_exp1_exp2.loc[1, 'exp_2'],
    accuracy_summary_flan_t5.loc[0, 'FLAN-T5']],
    palette='Paired')
plt.xlabel('Experiment', fontsize=16)
plt.ylabel('Accuracy', fontsize=16)
plt.title('Overall Accuracy Comparison', fontsize=18)
plt.ylim(0, 1)
for i, v in enumerate([
    accuracy_summary_exp1_exp2.loc[1, 'exp_1'],
    accuracy_summary_exp1_exp2.loc[1, 'exp_2'],
    accuracy_summary_flan_t5.loc[0, 'FLAN-T5']]):
    plt.text(i, v + 0.02, f"{v:.2f}", ha='center', fontsize=14)
plt.grid(False)
plt.show()

# Plot accuracy per topic (FLAN)
plt.figure(figsize=(16, 9))
bar_width = 0.5
index = np.arange(len(topic_order))

bars = plt.bar(index + bar_width / 2, merged_accuracy['accuracy_flan_t5'], bar_width, color=sns.color_palette('Paired')[2], edgecolor='k')

plt.xlabel('Topics', fontsize=16)
plt.ylabel('Accuracy', fontsize=16)
plt.title('Accuracy per Topic', fontsize=18)
plt.xticks(index + bar_width / 2, topic_order, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.ylim(0, 1)
plt.tight_layout()
plt.grid(False)
plt.show()

# Plot accuracy per topic comparison between the three experiments
plt.figure(figsize=(16, 9))
bar_width = 0.35
index = np.arange(len(topic_order))

plt.bar(index - bar_width/2, merged_accuracy['best_experiment'], bar_width, label='Rule-Based', color=sns.color_palette('Paired')[0], edgecolor='k')
plt.bar(index + bar_width/2, merged_accuracy['accuracy_flan_t5'], bar_width, label='FLAN-T5', color=sns.color_palette('Paired')[2], edgecolor='k')

plt.xlabel('Topics', fontsize=16)
plt.ylabel('Accuracy', fontsize=16)
plt.title('Accuracy per Topic Comparison', fontsize=18)
plt.xticks(index, topic_order, rotation=0, fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.ylim(0, 1)
plt.tight_layout()
plt.grid(False)
plt.show()

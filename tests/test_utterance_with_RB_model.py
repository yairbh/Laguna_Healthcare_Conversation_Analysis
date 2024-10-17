"""
RB Experiment 2:
This script processes and classifies utterances from raw data using a keyword-based rule-based classifier from
file keywords_rule_based_classifier_V2.py
"""
import os
from src.data.data_pipeline_functions import (clean_data,
                                              identify_care_manager)
from src.utils.common import get_project_root
from src.utils.constants import raw_data_df
from src.models.Rule_Based.keywords_rule_based_classifier_V2 import custom_keywords, stops, classify_single_utterance

df = raw_data_df.copy()
# print(df.head)

short_recording_ids_list = ['afcf16bb-bd4e-45a8-b24a-7ffe533ff8a4',
                         'd5c13967-e360-4be9-b8d4-1485a1830c89',
                         '4e27d288-a828-4863-a5e2-3c5f580bebe1',
                         '0d241ae5-0ea0-4f68-b51d-349041d8e524',
                         'b32c4726-ffe7-48c4-bc26-be03c77d838e',
                         'c4cc5640-7a3b-44f9-8d54-78b4c6778bf6',
                         '28a21531-c70d-45b7-ad29-041b25e7dfdd',
                         '302fc9ba-b41b-4476-9416-2f4a03508f3c',
                         '4f0f231c-e42e-4f8d-a2d7-77ad2477098d',
                         '4f0f231c-e42e-4f8d-a2d7-77ad2477098d',
                         'afcf16bb-bd4e-45a8-b24a-7ffe533ff8a4',
                         '0d241ae5-0ea0-4f68-b51d-349041d8e524',
                         '1722702f-5103-4c3e-81aa-e31a67486a97',
                         '3814191c-d3c1-4058-9184-6fbd6a7b7b21',
                         ]

df = df[df['recording_id'].isin(short_recording_ids_list)]

df = df[df['utterance_id'] == 'f7d8bea6-728a-4c39-bb73-036b4d6dad51']


# Getting us_cities.csv path
project_root = get_project_root()
cities_file = os.path.join(project_root, 'src', 'data', 'us_cities.csv')

# Identify CM and add Boolean column to the df
df = identify_care_manager(df)

# Cleaning data
df = clean_data(df, cities_file=cities_file, cities_threshold=3)


# classified_utterances_df = classify_utterances(utterances_df=df, keywords=custom_keywords, stops=stops)

# output_file_path = os.path.join(project_root, 'tests', 'classified_utterances_RB_exp2.csv')
# classified_utterances_df.to_csv(output_file_path, index=False)

# classified_utterances_df = classify_utterances(utterances_df=df, keywords=custom_keywords, stops=stops)
# print(classified_utterances_df.columns)
# print(classified_utterances_df.shape)
# print("that's it!")

# print(classified_utterances_df)
ut = "Good, good, good, good. And how about, um, eating wise? Appetite's been okay."
class_ut = classify_single_utterance(utterance=ut, keywords=custom_keywords, stops=stops)
print(class_ut)
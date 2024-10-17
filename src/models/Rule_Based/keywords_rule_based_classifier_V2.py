"""
This script classifies utterances from a specified file based on predefined custom keywords associated with different topics.
1. Imports required modules and functions, including data loading, text preprocessing, and classification utilities.
2. Defines custom keywords for each topic, used for classification.
3. Implements text preprocessing functions to clean and lemmatize text.
4. Classifies each utterance based on the presence of custom keywords and associates it with the most relevant topic.
"""


import string
import nltk
from nltk import pos_tag, WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from src.utils.common import get_project_root
import json
import pandas as pd
import os
from src.utils.constants import MY_STOPS

# Custom keywords for each topic
custom_keywords = {
    '1_member_identification': ['address', 'name', 'confirm', 'full', 'could', 'verify', 'please', 'start', 'verification', 'update', 'whether', 'names', 'complete'],
    '2_call_recording_disclosure': ['record', 'call', 'call record', 'purpose', 'service', 'inform', 'recorded', 'line', 'aim', 'remind'],
    # '3_participant_verification': ['speak', 'could', 'call', 'account', 'confirm', 'know', 'conversation', 'please', 'speaking', 'would'],
    '4_cm_introduction': ['from', 'care manager', 'case manager'],
    '5_handling_phi': ['phi', 'health information', 'information', 'health', 'privacy', 'handle', 'personal', 'protect', 'assure', 'ill', 'data', 'medical', 'healthcare', 'manage'],
    # '6_tcpa_compliance': ['let know', 'receive', 'know', 'call', 'inform', 'opt out', 'time', 'right', 'want', 'option', 'provide', 'remind', 'tell'],
    '7_sensitive_information_protocol': ['sensitive', 'privacy', 'sensitive health', 'health', 'handle', 'topic', 'like', 'information', 'protect', 'confidentiality', 'mental', 'hiv', 'substance', 'manage'],
    # '8_medical_consultation_advice': ['medical', 'provide', 'health', 'concern', 'consultation', 'need', 'feel free', 'free', 'ill'],
    # '9_care_coordination': ['care', 'service', 'well', 'today', 'ensure', 'health', 'plan', 'part', 'make', 'current', 'doctor', 'nurse', 'phone call', 'visit', 'healthcare', 'medical', 'nursing', 'patient', 'system', 'provided', 'maintain', 'necessary', 'enable'],
    '10_log_protocol': ['change', 'level', 'difficulty', 'like', 'update', 'tell', 'feel', 'talk', 'let review', 'pain', 'mood', 'energy', 'sleep', 'mobility', 'mobile', 'appetite', 'improve', 'high', 'low', 'medium', 'current', 'stress'],
    # '11_treatment_compliance_medical_state': ['treatment', 'medical', 'need', 'current', 'state', 'ensure', 'review', 'issue', 'medication'],
    '2+4': ['purpose', 'remind', 'call', 'recorded', 'case manager', 'aim', 'from', 'service', 'call record', 'care manager', 'inform', 'record', 'line'],
    '1+2+4': ['from', 'complete', 'whether', 'full', 'inform', 'line', 'case manager', 'address', 'aim', 'confirm', 'service', 'care manager', 'update', 'names', 'purpose', 'recorded', 'could', 'start', 'call record', 'verification', 'please', 'verify', 'remind', 'call', 'name', 'record'],
}

# Text preprocessing
def get_wordnet_pos(treebank_tag):
    """
    Map POS tag to first character lemmatize() accepts.
    """
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatize(text, lemmatizer):
    """
    Lemmatize the given text based on POS tags.
    """
    tokens = nltk.word_tokenize(text)
    pos_tags = pos_tag(tokens)
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in pos_tags]
    return ' '.join(lemmatized_tokens)

def remove_stops(text, stops):
    """
    Remove stopwords, punctuation, and digits from the text.
    """
    words = text.split()
    final = [word for word in words if word not in stops]
    final = ' '.join(final)
    final = final.translate(str.maketrans('', '', string.punctuation))  # remove punctuations
    final = ''.join([i for i in final if not i.isdigit()])  # remove digits
    return ' '.join(final.split())  # remove extra spaces

def clean_text(text, stops):
    """
    Clean the given text by converting to lowercase, removing stopwords, punctuation, digits, and lemmatizing.
    """
    lemmatizer = WordNetLemmatizer()
    text = text.lower()
    text = remove_stops(text, stops)
    text = lemmatize(text, lemmatizer)
    return text

# Extend the list of stopwords
stops = list(set(stopwords.words("english") + MY_STOPS))
stops.remove('from')

# Function to classify topic based on keywords
def classify_single_utterance(utterance, keywords, stops):
    """
    Classify a single utterance by checking for the presence of keywords and mapping it to a topic.
    """
    utterance = clean_text(utterance, stops)

    # Check if utterance is too short
    min_number_of_words = 5
    if len(utterance.split()) < min_number_of_words:
        return 'no_topic'

    # Check for topics 2+4 by specific string matching
    recorded_line_phrases = ['calling from a recorded line', 'calling on a recorded line']
    if any(phrase in utterance for phrase in recorded_line_phrases):
        return '2_call_recording_disclosure'

    # If not topic 2, continue to check all topics using keywords
    utterance = utterance.split() #NEW ADDITION
    topic_scores = {topic: 0 for topic in keywords}
    for topic, word_list in keywords.items():
        for word in word_list:
            if word.lower() in utterance:
                topic_scores[topic] += 1
    return max(topic_scores, key=topic_scores.get) if max(topic_scores.values()) > 0 else 'no_topic'


# Function to classify utterances
def classify_utterances(utterances_df: pd.DataFrame, keywords, stops):
    """
    Takes raw_df of utterances to classify as input, classifies the utterances and return an updated df with
    a column "prediction" for each utterance.
    """
    utterances_df['prediction'] = utterances_df['text'].apply(classify_single_utterance, keywords=keywords, stops=stops)
    return utterances_df


# Select utterances to classify
project_root = get_project_root()
source_file_path = os.path.join(project_root, 'data', 'processed', 'all_raw_utterances_df.csv')
all_data_df = pd.read_csv(source_file_path)

# file_name = '6384d7ed9ba32b2c50b0094f_4f0f231c-e42e-4f8d-a2d7-77ad2477098d.json'
# utterances_to_classify = all_data_df.loc[all_data_df['file_name'] == file_name, 'text'].to_list()

# # Classify the selected utterances
# classified_utterances = classify_utterances(utterances_to_classify, custom_keywords, stops)

# # Print the results
# for utterance, topic in classified_utterances:
#     print(f"Utterance: '{utterance}' - Classified Topic: '{topic}'")

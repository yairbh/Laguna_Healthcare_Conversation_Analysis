"""
This script trains a Naive Bayes classifier to categorize utterances into predefined topics using TF-IDF vectorization. The steps include:
1. Loading and preparing data for TF-IDF vectorization.
2. Preprocessing text data by removing stop words and applying lemmatization.
3. Vectorizing the preprocessed text data using TF-IDF.
4. Training a Naive Bayes classifier and evaluating its performance using cross-validation.
5. Applying the trained model to new data and generating predictions.
"""

import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score
from src.data.generated_tagged_utterances import generated_utterances_by_topic
from src.utils.preprocessing import preprocess_data
import os
import json

# Prepare data for tf-idf (inputs and labels)
topic_dict = {
    1: 'member_identification',
    2: 'call_recording_disclosure',
    3: 'participant_verification',
    4: 'cm_introduction',
    5: 'handling_phi',
    6: 'tcpa_compliance',
    7: 'sensitive_information_protocol',
    8: 'medical_consultation_advice',
    9: 'care_coordination',
    10: 'log_protocol',
    11: 'treatment_compliance_medical_state'
}

all_utterances = []
labels = []

for topic_num in range(1, 12):
    topic = topic_dict[topic_num]
    current_topic_utterances = generated_utterances_by_topic[topic]
    current_topic_labels = [topic_num] * len(current_topic_utterances)
    all_utterances.extend(current_topic_utterances)
    labels.extend(current_topic_labels)

# Define stop words
my_stops = ['um', 'uh', 'affirmative', 'laugh', 'mmhmm', 'oh']
stops = list(set(stopwords.words("english") + my_stops))
stops.remove('from')

# Apply tf-idf
vectorizer = TfidfVectorizer(
    lowercase=True,
    max_features=100,
    max_df=0.8,
    min_df=5,
    ngram_range=(1, 2),
    stop_words=stops
)

processed_data = preprocess_data(all_utterances)
X = vectorizer.fit_transform(processed_data)

# Naive-Bayes Classifier
model = MultinomialNB()

# Cross-validation
scores = cross_val_score(model, X, labels, cv=5, scoring='accuracy')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))

# Train the model
model.fit(X, labels)

# Determine the project's root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define the relative path to the JSON file
source_file_path = os.path.join(project_root, 'data', 'raw_files', 'merged_conversations', 'all_conversations_raw_files.json')

# Predict on unseen data
with open(source_file_path, 'r') as file:
    new_data = json.load(file)

filename = '63a5c929b5b42ce1b7e2d6eb_8fda73ca-ccd2-4fe7-8244-cce5962da756.json'
all_utterances = [utterance['text'] for utterance in new_data[filename]['transcript']]

X_new = preprocess_data(all_utterances)
X_new = vectorizer.transform(X_new)

# Predict and create DataFrame with results
preds = model.predict(X_new)

results_df = pd.DataFrame(data={'utterance': all_utterances, 'topic': preds})
print(results_df)

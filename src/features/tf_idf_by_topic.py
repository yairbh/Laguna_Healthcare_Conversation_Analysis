"""
This script processes and analyzes text data to identify key words and themes associated with various topics.
It performs the following steps:
1. Data Preparation: It organizes utterances by predefined topics and performs initial text processing.
2. Text Preprocessing: It applies several cleaning steps.
3. Feature Extraction: Uses TF-IDF vectorization to transform cleaned text data into a numerical format.
4. Analysis: After transforming the text data into TF-IDF matrices, the script calculates and displays the top 10 words
for each topic based on their TF-IDF scores, highlighting the most characteristic terms used in each topic.

"""

import numpy as np
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from sklearn.feature_extraction.text import TfidfVectorizer
from src.data.generated_tagged_utterances import generated_utterances_by_topic
import nltk
from nltk import WordNetLemmatizer
import string

def get_wordnet_pos(treebank_tag):
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
    tokens = nltk.word_tokenize(text)
    pos_tags = pos_tag(tokens)
    lemmatized_tokens = [lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in pos_tags]
    return ' '.join(lemmatized_tokens)

def clean_docs(docs, stops):
    lemmatizer = WordNetLemmatizer()
    final = []
    for doc in docs:
        clean_doc = remove_stops(doc.lower(), stops)
        lemmatized_doc = lemmatize(clean_doc, lemmatizer)
        final.append(lemmatized_doc)
    return final

def remove_stops(text, stops):
    words = text.split()
    final = []
    for word in words:
        if word not in stops:
            final.append(word)
    final = ' '.join(final)
    final = final.translate(str.maketrans('', '', string.punctuation))  # remove punctuations
    final = ''.join([i for i in final if not i.isdigit()])  # remove digits
    while '  ' in final:
        final = final.replace('  ', ' ')  # replace double white space with a single white space
    return final

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

# Define stop words
my_stops = ['um', 'uh', 'affirmative', 'laugh', 'mmhmm', 'oh', 'hello', 'hi']  # update words 14.5.2024
stops = list(set(stopwords.words("english") + my_stops))
stops.remove('from')

# Apply tf-idf
vectorizer = TfidfVectorizer(
    lowercase=True,
    max_features=200,
    max_df=0.8,
    min_df=2,
    ngram_range=(1, 4),
    stop_words=stops
)

list_of_utterances_by_topics = []
for topic_num in range(1, 12):
    topic = topic_dict[topic_num]
    current_topic_utterances = generated_utterances_by_topic[topic]
    current_topic_utterances = ' '.join(current_topic_utterances)
    list_of_utterances_by_topics.append(current_topic_utterances)

processed_data = clean_docs(docs=list_of_utterances_by_topics, stops=stops)
X = vectorizer.fit_transform(processed_data)  # receives a list of utterances and returns document-term matrix
X_array = X.toarray()

feature_names = vectorizer.get_feature_names_out()

top_10_words_per_topic = {}
for ind in range(1, 12):
    topic = topic_dict[ind]
    topic_frequencies = X_array[ind - 1, :]
    top_10_indices = np.argsort(topic_frequencies)[-10:][::-1]
    top_10_words_per_topic[f'{ind}_{topic}'] = list(feature_names[top_10_indices])

for key, value in top_10_words_per_topic.items():
    print(key, value)

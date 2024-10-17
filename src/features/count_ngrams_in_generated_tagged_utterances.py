"""
This script counts n-grams in utterances of a specified topic and optionally plots a bar graph
of the most common n-grams.
"""

import string
import nltk
from nltk import WordNetLemmatizer
from collections import Counter
from matplotlib import pyplot as plt
from nltk.corpus import stopwords
import seaborn as sns
from src.data.generated_tagged_utterances import generated_utterances_by_topic

def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = ''.join([i for i in text if not i.isdigit()])
    stops = set(stopwords.words("english"))
    stops.remove('from')
    other_common_words = {'um', 'uh', 'affirmative', 'laugh', 'mmhmm', 'mm-hmm', 'oh'}
    stops = stops.union(other_common_words)
    text = ' '.join(word for word in text.split() if word not in stops)
    return text

def get_topic_name(topic_num):
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
    return topic_dict[topic_num]

def count_n_grams_per_topic(data, topic, n=1, top=10, plot=True):
    hist = Counter()
    lemmatizer = WordNetLemmatizer()
    topic = get_topic_name(topic)
    utterances = data[topic]
    for utterance in utterances:
        utterance = clean_text(utterance)
        tokens = nltk.word_tokenize(utterance)
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
        words_to_count = []
        if n > 1:
            for i in range(len(lemmatized_tokens) - n + 1):
                n_gram = ' '.join(lemmatized_tokens[i:i + n])
                words_to_count.append(n_gram)
        else:
            words_to_count = lemmatized_tokens
        hist.update((words_to_count))
    most_common_words = hist.most_common(top)
    if plot:
        words, frequencies = zip(*most_common_words)
        plt.figure(figsize=(10,12))
        sns.barplot(x=frequencies, y=words)
        plt.xlabel('N-grams')
        plt.ylabel('Frequencies')
        plt.title(f'Top {top} Most Common {n}-grams')
        plt.tight_layout()
        plt.show()
    return most_common_words

if __name__ == "__main__":
    for i in range(1, 4):
        count_n_grams_per_topic(data=generated_utterances_by_topic, topic=1, n=i, top=10, plot=True)

"""
This script provides functions to preprocess text data.
"""

import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import string


def lemmatize(text, lemmatizer):
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized_tokens)


def remove_stops(text, stops):
    words = text.split()
    final = [word for word in words if word not in stops]
    final = ' '.join(final)
    final = final.translate(str.maketrans('', '', string.punctuation))
    final = ''.join([i for i in final if not i.isdigit()])
    while '  ' in final:
        final = final.replace('  ', ' ')
    return final


def clean_docs(docs, stops):
    lemmatizer = WordNetLemmatizer()
    final = []
    for doc in docs:
        clean_doc = remove_stops(doc.lower(), stops)
        lemmatized_doc = lemmatize(clean_doc, lemmatizer)
        final.append(lemmatized_doc)
    return final


def preprocess_data(utterances):
    stops = set(stopwords.words("english"))
    stops.update(['um', 'uh', 'affirmative', 'laugh', 'mmhmm', 'oh'])
    stops.remove('from')
    cleaned_docs = clean_docs(docs=utterances, stops=stops)
    return cleaned_docs

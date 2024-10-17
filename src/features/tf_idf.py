### NOT UPDATED ###

"""
This script performs text clustering on conversation transcripts using TF-IDF vectorization and K-means clustering. It includes the following operations:
1. Loads conversation data from JSON files.
2. Cleans and preprocesses the text data by removing stop words, punctuation, and digits, and lemmatizing the text.
3. Applies TF-IDF vectorization to the cleaned text data.
4. Performs K-means clustering on the vectorized text data.
5. Outputs the top terms for each cluster to a text file.
"""

import nltk
from nltk import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import string
from nltk.corpus import stopwords
import json
import os
from src.utils.common import get_project_root

# Function to load data from a JSON file
def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# Function to lemmatize text
def lemmatize(text, lemmatizer):
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    return ' '.join(lemmatized_tokens)

# Function to clean and preprocess documents
def clean_docs(docs):
    my_stops = ['um', 'uh', 'affirmative', 'laugh', 'mmhmm', 'mm-hmm', 'oh']
    stops = set(stopwords.words("english") + my_stops)
    lemmatizer = WordNetLemmatizer()
    final = []
    for doc in docs:
        clean_doc = remove_stops(doc.lower(), stops)
        lemmatized_doc = lemmatize(clean_doc, lemmatizer)
        final.append(lemmatized_doc)
    return final

# Function to remove stop words, punctuation, and digits from text
def remove_stops(text, stops):
    words = text.split()
    final = [word for word in words if word not in stops]
    final = ' '.join(final)
    final = final.translate(str.maketrans('', '', string.punctuation))
    final = ''.join([i for i in final if not i.isdigit()])
    return ' '.join(final.split())

# Get the project root directory
project_root = get_project_root()

# Define the source folder path and list all filenames
source_folder_path = os.path.join(project_root, 'data', 'only_long_convs')
filenames = os.listdir(source_folder_path)

# Load and collect all utterances
all_utterances = []
for filename in filenames:
    file_path = os.path.join(source_folder_path, filename)
    data = load_data(file_path)

    for utterance in data['transcript']:
        text = utterance['text']
        all_utterances.append(text)

# Clean and preprocess the documents
cleaned_docs = clean_docs(all_utterances)

# Define stop words for TF-IDF vectorizer
my_stops = ['um', 'uh', 'affirmative', 'laugh', 'mmhmm', 'mm-hmm', 'oh']
stops = list(set(stopwords.words("english") + my_stops))

# Apply TF-IDF vectorization
vectorizer = TfidfVectorizer(
    lowercase=True,
    max_features=100,
    max_df=0.8,
    min_df=5,
    ngram_range=(1, 2),
    stop_words=stops
)

vectors = vectorizer.fit_transform(cleaned_docs)
feature_names = vectorizer.get_feature_names_out()

# Convert vectors to a dense list
dense = vectors.todense()
denselist = dense.tolist()

# Extract keywords for each document
all_keywords = []
for description in denselist:
    x = 0
    keywords = []
    for word in description:
        if word > 0:
            keywords.append(feature_names[x])
        x += 1
    all_keywords.append(keywords)

# Define the number of clusters
true_k = 20

# Apply K-means clustering
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(vectors)

# Get the top terms for each cluster
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names_out()

# Define the result file path and write the top terms for each cluster
result_file_path = os.path.join(project_root, 'data', 'tfidf_results.txt')
with open(result_file_path, 'w', encoding='utf-8') as f:
    for i in range(true_k):
        f.write(f'Cluster {i}\n')
        for ind in order_centroids[i, :10]:
            f.write(' %s\n' % terms[ind])
        f.write('\n\n')

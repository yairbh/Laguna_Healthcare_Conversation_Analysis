"""
This script utilizes text data and word embeddings to find similar words and clean transcripts. It's designed to help analyze large volumes of text data efficiently. The steps include:
1. Initializes and employs GloVe embeddings via Flair for word representation.
2. Implements cosine similarity to compare word embeddings and find similar words.
3. Uses NLTK for text preprocessing, including lemmatization and removing stopwords.
4. Manages and processes large datasets to create and utilize a vocabulary of significant words.
5. Finds and displays similar words for top words in each topic.
"""

import string
import nltk
from flair.embeddings import WordEmbeddings
from flair.data import Sentence
import torch
from nltk import pos_tag, WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from src.features.tf_idf_by_topic import top_10_words_per_topic
from src.data.generate_corpus_statistics_df import df
from src.utils.common import get_project_root
import json

# Initialize embeddings
glove_embedding = WordEmbeddings('glove')

# Get embeddings for top relevant words
def get_word_embedding(word):
    sentence = Sentence(word)
    glove_embedding.embed(sentence)
    if len(sentence) > 0:
        return sentence[0].embedding
    else:
        return None

# Compute cosine similarity to find similar words
def cosine_similarity(embedding1, embedding2):
    if embedding1 is None or embedding2 is None:
        return -1  # Return a low similarity score if any embedding is None
    return torch.nn.functional.cosine_similarity(embedding1, embedding2, dim=0).item()

# Find similar words
def find_similar_words(word, vocabulary, top_n=5, similarity_threshold=0.6):
    target_embedding = get_word_embedding(word)
    if target_embedding is None:
        return []

    similarities = {}

    for vocab_word in vocabulary:
        if vocab_word == word:
            continue
        vocab_embedding = get_word_embedding(vocab_word)
        if vocab_embedding is not None:  # Ensure vocab_embedding is not None
            similarity = cosine_similarity(target_embedding, vocab_embedding)
            if similarity >= similarity_threshold: # Apply similarity threshold
                similarities[vocab_word] = similarity

    sorted_similar_words = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
    return [word for word, similarity in sorted_similar_words[:top_n]]

# Text preprocessing
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

def remove_stops(text, stops):
    words = text.split()
    final = [word for word in words if word not in stops]
    final = ' '.join(final)
    final = final.translate(str.maketrans('', '', string.punctuation))  # remove punctuations
    final = ''.join([i for i in final if not i.isdigit()])  # remove digits
    return ' '.join(final.split())  # remove extra spaces

def clean_docs(docs, stops):
    lemmatizer = WordNetLemmatizer()
    return [lemmatize(remove_stops(doc.lower(), stops), lemmatizer) for doc in docs]

my_stops = ['um', 'uh', 'affirmative', 'laugh', 'mmhmm', 'oh', 'hello', 'hi']
stops = list(set(stopwords.words("english") + my_stops))
stops.remove('from')

# Load data (transcripts)
df_long_conversations = df[df['num_of_utterances'] > 10]
long_conversations = df_long_conversations['file_name'].to_list()

project_root = get_project_root()
source_file_path = os.path.join(project_root, 'data', 'raw_files', 'merged_conversations', 'all_conversations_raw_files.json')
with open(source_file_path, 'r') as source_file:
    data = json.load(source_file)

# Create vocabulary (from entire data)
entire_text = []
for file in data:
    if file in long_conversations:
        continue  # Extracts words from long conversations only
    entire_text.extend([utterance['text'] for utterance in data[file]['transcript']])

clean_text = clean_docs(entire_text, stops)
vocabulary = set(' '.join(clean_text).split())

all_similar_words_by_topic = {}

for topic in top_10_words_per_topic:
    topic_similar_words = {}
    top_words = top_10_words_per_topic[topic]

    for word in top_words[:5]:  # Takes only top 3 words for each topic
        if len(word.split()) > 1:
            continue

        similar_words = find_similar_words(word=word, vocabulary=vocabulary, top_n=5)
        topic_similar_words[word] = similar_words

    all_similar_words_by_topic[topic] = topic_similar_words

for topic in all_similar_words_by_topic:
    print(f'{topic}: \n')

    for word in all_similar_words_by_topic[topic]:
        print(f'{word}: {all_similar_words_by_topic[topic][word]}')

    print('\n')

import heapq
import nltk
import numpy as np
import pandas as pd

# Load the text data
text = "Insert your text here."

# Tokenize the text into sentences
sentences = nltk.sent_tokenize(text)

# Calculate the sentence scores based on word frequency
word_frequencies = {}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        if word not in nltk.corpus.stopwords.words('english'):
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

# Calculate the sentence scores based on sentence length
sentence_scores = {}
for sentence in sentences:
    if len(sentence.split(' ')) < 30:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

# Select the top 5 sentences with the highest scores
summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

# Combine the summary sentences into a summary paragraph
summary = ' '.join(summary_sentences)
print(summary)

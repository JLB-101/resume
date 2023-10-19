import heapq
import nltk
import numpy as np
import pandas as pd

# Baixa os recursos necessários
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')

# Recebe o texto de entrada do usuário
print("\n=======================================================================================\n")
text = input("Insira seu texto aqui: ")

# Tokeniza o texto em frases
sentences = nltk.sent_tokenize(text)

# Calcula as pontuações das frases com base na frequência de palavras
word_frequencies = {}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        if word not in nltk.corpus.stopwords.words('portuguese') and word not in nltk.corpus.stopwords.words('english'):
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

# Calcula as pontuações das frases com base no comprimento da frase
sentence_scores = {}
for sentence in sentences:
    if len(sentence.split(' ')) < 30:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

# Seleciona as 5 frases principais com as pontuações mais altas
summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

# Combina as frases principais em um parágrafo de resumo
summary = ' '.join(summary_sentences)

print("\n================================Resumo=================================================\n")
print("\n---------------------------------------------------------------------------------------\n")
print("Resumo: ", summary)
print("\n---------------------------------------------------------------------------------------\n")
print("\n=======================================================================================\n")


# Conta o número de palavras e linhas no texto original e no resumo
original_word_count = len(text.split())
original_line_count = len(text.split('\n'))
summary_word_count = len(summary.split())
summary_line_count = len(summary.count('\n'))

# Imprime as estatísticas
print("Número de palavras no texto original: ", original_word_count)
print("Número de linhas no texto original: ", original_line_count)
print("Número de palavras no resumo: ", summary_word_count)
print("Número de linhas no resumo: ", summary_line_count)

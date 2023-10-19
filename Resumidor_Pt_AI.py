import heapq
import nltk

# Baixa os recursos necessários do NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')

# Recebe o texto de entrada do usuário
text = input("Insira seu texto aqui: ")

# Tokeniza o texto em frases
sentences = nltk.sent_tokenize(text, language='portuguese')

# Calcula as pontuações de cada frase com base na frequência das palavras
word_frequencies = {}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower(), language='portuguese'):
        if word not in nltk.corpus.stopwords.words('portuguese'):
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

# Calcula as pontuações de cada frase com base no comprimento da frase
sentence_scores = {}
for sentence in sentences:
    if len(sentence.split(' ')) < 30:
        for word in nltk.word_tokenize(sentence.lower(), language='portuguese'):
            if word in word_frequencies.keys():
                if sentence not in sentence_scores.keys():
                    sentence_scores[sentence] = word_frequencies[word]
                else:
                    sentence_scores[sentence] += word_frequencies[word]

# Seleciona as 5 frases com as maiores pontuações
summary_sentences = heapq.nlargest(5, sentence_scores, key=sentence_scores.get)

# Combina as frases do resumo em um único parágrafo
summary = ' '.join(summary_sentences)
print('------------------------------------------------------------\n Resumo: \n')
print(summary)

import nltk
nltk.download()
from urllib.request import Request, urlopen

import PyPDF2
#URL do local onde está o livro
ULR_livro = 'Lectura1.pdf'
#lendo o local indicado
book = open(ULR_livro, 'rb')
#Lendo o livro
pdfReader = PyPDF2.PdfFileReader(book)
text = '' #var aonde vai ficar todo o texto do livro
#O conto está apenas entre as paginas 3 e 32
for num in range(3 , 32):
    page = pdfReader.getPage(num)
    text = text + page.extractText()

#Intalação dos dicionários de palavras(corpus)
from collections import defaultdict
corpus = defaultdict(int)


#dividindo o nosso texto em sentenças e depois em palavras
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
sentencas = sent_tokenize(text)
palavras = word_tokenize(text.lower())
#Retirando as stopwords
from nltk.corpus import stopwords
from string import punctuation
stopwords = set(stopwords.words('portuguese') + list(punctuation))
palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]
# criando a distribuição de frequência
from nltk.probability import FreqDist
frequencia = FreqDist(palavras_sem_stopwords)
# Separando as sentenças mais importantes
from collections import defaultdict
sentencas_importantes = defaultdict(int)
#Loop para percorrer todas as sentenças e coletar todas as estatísticas
for i, sentenca in enumerate(sentencas):
    for palavra in word_tokenize(sentenca.lower()):
        if palavra in frequencia:
            sentencas_importantes[i] += frequencia[palavra]
#“n” sentenças mais importantes
from heapq import nlargest
idx_sentencas_importantes = nlargest(4, sentencas_importantes, sentencas_importantes.get)
# Temos o resumo! :)
resumo = ''
for i in sorted(idx_sentencas_importantes):
    resumo = resumo + sentencas[i]



import nltk
nltk.download()

#o import das funções Request e urlopen da biblioteca urllib.request (urllib2 no Python 2).
from urllib.request import Request, urlopen

#2- Agora vamos utilizar essas funções para ler uma notícia do site Último Segundo. As informações retornadas serão armazenadas em uma variável chamada pagina.

#aqui entra a url da blog, site entre outros.
link = Request('https://esporte.ig.com.br/futebol/internacional/2023-03-06/neymar-lesionado-messi-elogia-mbappe-projeta-futuro-psg.html',headers={'User-Agent': 'Mozilla/5.0'})
pagina = urlopen(link).read().decode('utf-8', 'ignore')

#3- Hora de utilizar o BeautifulSoap para garimpar a página e pegar apenas o que nos interessa. 
# Nessa etapa é importante saber que o código depende da estrutura da página que estamos garimpando, ou seja, 
# é preciso modificá-lo para garimpar outras páginas. No 
# site do Último Segundo as notícias ficam dentro de uma DIV com ID=noticia, como vocês podem notar na imagem:
from bs4 import BeautifulSoup
soup = BeautifulSoup(pagina, "lxml")
texto = soup.find(id="noticia").text


#4- Chegou o momento de aplicarmos o processamento sobre linguagens 
# naturais para tratar o texto extraído da notícia do site.
#  Vamos começar importando algumas funcionalidades da biblioteca NLTK:
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

#Agora vamos dividir o nosso texto em sentenças e depois em palavras:
sentencas = sent_tokenize(texto)
palavras = word_tokenize(texto.lower())


#ATENÇÃO: O processo de “tokenização” do NLTK considera
#  as pontuações do texto como tokens também e 
# por isso não podemos deixar de retirá-los também!
#Retirando as stopwords da nossa lista de palavras:

from nltk.corpus import stopwords
from string import punctuation
stopwords = set(stopwords.words('portuguese') + list(punctuation))
palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopwords]

#6- Hora de criar a nossa distribuição de frequência para essa lista de palavras e 
# descobrir quais são as mais importantes.
#  Para isso, vamos utilizar a função FreqDist da biblioteca nltk.probability:

from nltk.probability import FreqDist
frequencia = FreqDist(palavras_sem_stopwords)

#7- Vamos agora separar quais são as sentenças mais importantes do nosso texto.
#  Criaremos um “score” para cada sentença baseado no número de vezes que uma palavra importante se repete dentro dela.
from collections import defaultdict
sentencas_importantes = defaultdict(int)

#Hora de popular o nosso dicionário. 
# Vamos criar um looping para percorrer todas as sentenças e coletar todas as estatísticas:
for i, sentenca in enumerate(sentencas):
    for palavra in word_tokenize(sentenca.lower()):
        if palavra in frequencia:
            sentencas_importantes[i] += frequencia[palavra]


#9- Pronto! De posse dessas informações,
#  podemos selecionar no nosso dicionário as “n” sentenças mais importantes para formar o nosso resumo.
#  Para facilitar a nossa vida, vamos usar a funcionalidade nlargest da biblioteca heapq:

from heapq import nlargest
idx_sentencas_importantes = nlargest(4, sentencas_importantes, sentencas_importantes.get)

#10- Finalmente podemos criar o nosso resumo: de qutrosentecas
for i in sorted(idx_sentencas_importantes):
    print(sentencas[i])

#Librería PDF -> HTML
import fitz
#Librería para Realizar Resumen 
import bs4 as bs  
import urllib.request  
import re
import nltk
import bs4
import urllib.request
import requests
from bs4 import BeautifulSoup
import urllib.request
from inscriptis import get_text
from googletrans import Translator
#Para la version de googletrans es -> pip install googletrans==3.1.0a0
import pdfminer
from pdfminer.high_level import extract_text
from nltk import word_tokenize,sent_tokenize
import heapq  
nltk.download('punkt')
nltk.download('stopwords')
#Librería para la polaridad
from textblob import TextBlob
#Librería para leer txt utf-8
import codecs

def PdfToHTML():
    #Insertamos el PDF(1)
    pdf = "Lectura1.pdf" # ----> Aquí insertas tu PDF (Recuerda que el nombre de tu pdf debe ser igual)
    documento = fitz.open(pdf)
    pagina = documento.loadPage(0)
    doc = fitz.open(pdf)
    salida = open(pdf+".html","wb")
    for pagina in doc:
        texto = pagina.getText("html").encode("utf8")
        salida.write(texto)
        salida.write(b"\n--------------------\n")
    salida.close()
    Resumen()  

def Resumen():
    #Insertamos el PDF(2)
    pdfTohtml = extract_text("Lectura1.pdf") # ----> Aquí insertas tu PDF (Recuerda que el nombre de tu pdf debe ser igual)
    articulo_texto = pdfTohtml
    articulo_texto = articulo_texto.replace("[ edit ]", "")
    print ("#########################")
    print ("##### R E S U M E N #####")
    print ("#########################")

    # Elimina palabras vacías, espacios extras
    articulo_texto = re.sub(r'\[[0-9]*\]', ' ', articulo_texto)  
    articulo_texto = re.sub(r'\s+', ' ', articulo_texto)  

    formatear_articulo = re.sub('[^a-zA-Z]', ' ', articulo_texto )  
    formatear_articulo = re.sub(r'\s+', ' ', formatear_articulo)  
    
    lista_palabras = nltk.sent_tokenize(articulo_texto)  
    stopwords = nltk.corpus.stopwords.words('portuguese')

    frecuencia_palabras = {}  
    for word in nltk.word_tokenize(formatear_articulo):  
        if word not in stopwords:
            if word not in frecuencia_palabras.keys():
                frecuencia_palabras[word] = 1
            else:
                frecuencia_palabras[word] += 1
    max_frecuencia = max(frecuencia_palabras.values())

    for word in frecuencia_palabras.keys():  
        frecuencia_palabras[word] = (frecuencia_palabras[word]/max_frecuencia)

    #Calcula frases repetidas
    max_oracion = {}  
    for sent in lista_palabras:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in frecuencia_palabras.keys():
                if len(sent.split(' ')) < 90: # -----------> Este numero variará de acuerdo a la cantidad de páginas que tengas
                    if sent not in max_oracion.keys():
                        max_oracion[sent] = frecuencia_palabras[word]
                    else:
                        max_oracion[sent] += frecuencia_palabras[word]

    #Resumen
    resumen_oracion = heapq.nlargest(7, max_oracion, key=max_oracion.get)
    resumen = ' '.join(resumen_oracion)  
    print(resumen)  

    #Traducción
    translator = Translator()
    translate = translator.translate(resumen, src="pt", dest="pt")

    #Guardar en .txt
    resumenpdf = open("Resumen.txt","w")
    resumenpdf.write("Resumen del texto:\n" + translate.text)
    resumenpdf.close()
    Polaridad()
    
def Polaridad():
    translator = Translator()
    resumenTxt = codecs.open("Resumen.txt","r")
    lectura=resumenTxt.read()
    translate = translator.translate(lectura, src="pt", dest="en")
    t=TextBlob(translate.text)
    t = t.sentiment
    polaridadLista = list(t)
    polaridad = open ("Polaridad.txt","w")
    if polaridadLista[0]<0:
        polaridad.write("OPINIÓN NEGATIVA\n\n")
        polaridad.write("POLARIDAD:" + str(polaridadLista[0])+"\nSUBJETIVIDAD: " + str(polaridadLista[1])+"\n")
    elif polaridadLista[0]==0:
        polaridad.write("OPINIÓN NEUTRAL\n\n")
        polaridad.write("POLARIDAD:" + str(polaridadLista[0])+"\nSUBJETIVIDAD: " + str(polaridadLista[1])+"\n")
    elif polaridadLista[0]>0 and polaridadLista[0] <=1:
        polaridad.write("OPINIÓN POSITIVA\n\n")
        polaridad.write("POLARIDAD:" + str(polaridadLista[0])+"\nSUBJETIVIDAD: " + str(polaridadLista[1])+"\n")
    polaridad.close()

PdfToHTML()
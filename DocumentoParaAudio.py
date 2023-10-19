import os
import docx
import pyttsx3

# Inicializa o mecanismo de TTS
engine = pyttsx3.init()

# Define a voz e a velocidade
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id) # Seleciona a segunda voz
engine.setProperty('rate', 150) # Define a taxa de fala

# Obtém o diretório atual
current_dir = os.getcwd()

# Constrói o caminho para o documento do Word
document_path = os.path.join(current_dir, 'document.docx')

# Abre o documento do Word
doc = docx.Document(document_path)

# Extrai o texto do documento
text = ''
for paragraph in doc.paragraphs:
    text += paragraph.text

# Converte o texto para áudio
engine.say(text)
engine.runAndWait()

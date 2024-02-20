import os
import langchain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import PyPDFLoader
import gradio as gr
import fitz
from PIL import Image

# Global variables
count = 0
n = 0
chat_history = []
chain = ''

# Function to set the OpenAI API key
def set_api_key(api_key):
    os.environ['OPENAI_API_KEY'] = api_key
    return 'OpenAI API key is set'

# Function to enable the API key input box
def enable_api_box():
    return

# Function to add text to the chat history
def add_text(history, text):
    if not text:
        raise gr.Error('Enter text')
    history.append((text, ''))
    return history

# Function to process the PDF file and create a conversation chain
def process_file(file):
    if 'OPENAI_API_KEY' not in os.environ:
        raise gr.Error('Upload your OpenAI API key')

    loader = PyPDFLoader(file.name)
    documents = loader.load()

    embeddings = OpenAIEmbeddings()

    pdf_search = Chroma.from_documents(documents, embeddings)

    chain = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0.3),
                                                  retriever=pdf_search.as_retriever(search_kwargs={"k": 1}),
                                                  return_source_documents=True)
    return chain

# Function to generate a response based on the chat history and query
def generate_response(history, query, btn):
    global count, n, chat_history, chain

    if not btn:
        raise gr.Error(message='Upload a PDF')
    if count == 0:
        chain = process_file(btn)
        count += 1

    result = chain({"question": query, 'chat_history': chat_history}, return_only_outputs=True)
    chat_history.append((query, result["answer"]))
    n = list(result['source_documents'][0])[1][1]['page']

    for char in result['answer']:
        history[-1][-1] += char
    return history, " "

# Function to render a specific page of a PDF file as an image
def render_file(file):
    global n
    doc = fitz.open(file.name)
    page = doc[n]
    # Render the page as a PNG image with a resolution of 300 DPI
    pix = page.get_pixmap(matrix=fitz.Matrix(300 / 72, 300 / 72))
    image = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    return image
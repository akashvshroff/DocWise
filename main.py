#TODO:
#1. Streamlit - doc input, validation and local storage + styling with lottie
#2. LangChain - doc upload, API calls, similarity search

#general imports
import os
import requests
from constants import *
import time

#streamlit imports
import streamlit as st
from streamlit_lottie import st_lottie
from utils import *

#langchain imports
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents.agent_toolkits import (create_vectorstore_agent, VectorStoreToolkit, VectorStoreInfo)

llm = OpenAI(temperature=0.1, verbose=True, openai_api_key=OpenAI_key)
embeddings = OpenAIEmbeddings(openai_api_key=OpenAI_key)

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_file = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_G6Lxp3nm1p.json")

hide_menu_style = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden; }
</style>
"""
st.set_page_config(page_title="DocWise")
#st.markdown(hide_menu_style, unsafe_allow_html=True)
st_lottie(lottie_file, height=200, key='coding')

st.title("**DocWise: Your AI PDF Analysis Assistant**")
st.write(
    "Upload your **:blue[pdf]** and ask your personal AI assistant any questions about it!")

input_file = st.file_uploader('Choose a file')

if input_file and does_file_have_pdf_extension(input_file):
    path = store_pdf_file(input_file, dir)
    scs = st.success("File successfully uploaded")
    filename = input_file.name
    store, agent_executor = None, None
    with st.spinner("Analyzing document..."):
        loader = PyPDFLoader(path)
        pages = loader.load_and_split()
        store = Chroma.from_documents(pages, embeddings, collection_name="analysis")
        vectorstore_info = VectorStoreInfo(name = filename, description="analyzing pdf", vectorstore=store)
        toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info, openai_api_key=OpenAI_key)
        agent_executor = create_vectorstore_agent(llm=llm, toolkit=toolkit, verbose=True)
    scs.empty()

    prompt = st.text_input("Input your question here")
    if prompt:
        response = agent_executor(prompt)
        st.write(response)

        with st.expander("Similarity Search"):
            search = store.similarity_search_with_score(prompt)
            st.write(search[0][0].page_content)




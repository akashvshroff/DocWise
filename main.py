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

os.environ['OPENAI_API_KEY'] = OpenAI_key
llm = OpenAI(temperature=0.1, verbose=True)
embeddings = OpenAIEmbeddings()

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_file = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_G6Lxp3nm1p.json")

hide_menu_style = """
<style>
footer {visibility: hidden; }
</style>
"""
st.set_page_config(page_title="DocWise")
#st.markdown(hide_menu_style, unsafe_allow_html=True)
st_lottie(lottie_file, height=200, key='coding')

st.title("**DocWise: An AI PDF Analysis Tool**")

if 'uploaded' not in st.session_state:
    st.session_state['uploaded'] = False
    st.session_state['filename'] = None

if 'agent_executor' not in st.session_state:
    st.session_state['agent_executor'] = None
    st.session_state['store'] = None

if not st.session_state['uploaded']:
    st.write(
        "Upload your **:blue[pdf]** and ask your personal AI assistant any questions about it!")
    input_file = st.file_uploader('Choose a file')

    if input_file and does_file_have_pdf_extension(input_file):
        path = store_pdf_file(input_file, dir)
        scs = st.success("File successfully uploaded")
        filename = input_file.name

        with st.spinner("Analyzing document..."):
            loader = PyPDFLoader(path)
            pages = loader.load_and_split()
            store = Chroma.from_documents(pages, embeddings, collection_name="analysis")
            vectorstore_info = VectorStoreInfo(name = filename, description="analyzing pdf", vectorstore=store)
            toolkit = VectorStoreToolkit(vectorstore_info=vectorstore_info)
            agent_executor = create_vectorstore_agent(llm=llm, toolkit=toolkit, verbose=True)
            st.session_state['agent_executor'] = agent_executor
            st.session_state['store'] = store
        scs.empty()

        st.session_state['uploaded'] = True
        st.session_state['filename'] = filename

        st.experimental_rerun()

if st.session_state['uploaded']:
    st.write(f"Enter your questions about the document \'{st.session_state['filename']}\' below:")
    prompt = st.text_input("Type your query")
    if prompt:
        agent_executor = st.session_state['agent_executor']
        store = st.session_state['store']
        with st.spinner("Generating response..."):
            response = agent_executor(prompt)
            st.write(response["output"])
            with st.expander("Similarity Search"):
                search = store.similarity_search_with_score(prompt)
                st.write(search[0][0].page_content)




#TODO:
#1. Streamlit - doc input, validation and local storage + styling with lottie
#2. LangChain - doc upload, API calls, similarity search

#langchain imports


#streamlit imports
import streamlit as st
from streamlit_lottie import st_lottie
from utils import *

#general imports
import os
import requests

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

hide_menu_style = """
<style>
#MainMenu {visibility: hidden; }
footer {visibility: hidden; }
</style>
"""
st.set_page_config(page_title="DocWise")
st.markdown(hide_menu_style, unsafe_allow_html=True)
#st_lottie(lottie_file, height=200, key='coding')

st.title("**DocWise: Analyze Your PDF Documents Using AI**")
st.write(
    "Upload your **:blue[pdf]** and have your own personal AI assistant analyze it for you.")

input_file = st.file_uploader('Choose a file')

if input_file and does_file_have_pdf_extension(input_file):
    print("success")
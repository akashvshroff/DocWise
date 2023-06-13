import streamlit as st
import os

def does_file_have_pdf_extension(file):
    if not (file.name.endswith('.pdf')):
        st.warning('Not a valid PDF file.', icon="⚠️")
        return False
    return True
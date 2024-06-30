import streamlit as st
from PyPDF2 import PdfReader
from llama_index.core import Document

def process_healthcare_document(uploaded_file):
    st.write(f"Processing file: {uploaded_file.name}")
    reader = PdfReader(uploaded_file)
    text_list = []
    for i, page in enumerate(reader.pages):
        text_list.append(page.extract_text())
        st.write(f"Processed page {i+1}")
    
    # Additional processing for healthcare documents could be added here
    # For example, extracting specific sections, metadata, or applying healthcare-specific NLP

    documents = [Document(text=t, metadata={"source": uploaded_file.name, "page": i}) for i, t in enumerate(text_list)]
    st.write(f"Created {len(documents)} document chunks")
    return documents
from PyPDF2 import PdfReader
from llama_index.core import Document

def process_healthcare_document(uploaded_file):
    reader = PdfReader(uploaded_file)
    text_list = []
    for page in reader.pages:
        text_list.append(page.extract_text())
    
    # Additional processing for healthcare documents could be added here
    # For example, extracting specific sections, metadata, or applying healthcare-specific NLP

    documents = [Document(text=t, metadata={"source": uploaded_file.name}) for t in text_list]
    return documents

import streamlit as st
from PyPDF2 import PdfReader
from llama_index.core import Document
import fitz  # PyMuPDF
import io
from PIL import Image
import base64

def process_healthcare_document(uploaded_file, include_vision=True):
    st.write(f"Processing file: {uploaded_file.name}")
    text_list = []
    image_list = []
    
    try:
        # Use PyPDF2 for text extraction
        reader = PdfReader(uploaded_file)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            text_list.append(text)
            st.write(f"Processed page {i+1} (text)")
        
        # Use PyMuPDF for image extraction if include_vision is True
        if include_vision:
            pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            for i, page in enumerate(pdf_document):
                images = extract_images_from_page(page)
                image_list.extend(images)
                st.write(f"Processed page {i+1} (images)")
    except Exception as e:
        st.error(f"Error processing document: {str(e)}")
        return []

    # Create documents with text content
    documents = [Document(text=t, metadata={"source": uploaded_file.name, "page": i}) for i, t in enumerate(text_list) if t.strip()]
    
    # Add image documents if vision is included
    if include_vision:
        for i, img in enumerate(image_list):
            img_doc = Document(
                text=f"Image {i+1} from {uploaded_file.name}",
                metadata={
                    "source": uploaded_file.name,
                    "type": "image",
                    "image": img
                }
            )
            documents.append(img_doc)
    
    st.write(f"Created {len(documents)} document chunks (including {len(image_list)} images)")
    return documents

def extract_images_from_page(page):
    images = []
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = page.parent.extract_image(xref)
        image_bytes = base_image["image"]
        
        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        images.append(img_str)
    return images
"""
Document processing functionality for PDF, DOCX, and TXT files
"""

import PyPDF2
from docx import Document
import io


def process_uploaded_doc(uploaded_file):
    """
    Extract text from uploaded document
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Extracted text or None if error
    """
    try:
        if uploaded_file.type == "application/pdf":
            return extract_pdf_text(uploaded_file)
        
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_docx_text(uploaded_file)
        
        elif uploaded_file.type == "text/plain":
            return uploaded_file.read().decode('utf-8')
        
        else:
            return None
    except Exception as e:
        print(f"Error processing document: {e}")
        return None


def extract_pdf_text(uploaded_file):
    """Extract text from PDF file"""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def extract_docx_text(uploaded_file):
    """Extract text from DOCX file"""
    doc = Document(uploaded_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text
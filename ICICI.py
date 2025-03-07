import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from docx import Document
from io import BytesIO

import pytesseract

# Set the correct path for Tesseract in Streamlit Cloud
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"


# Set Telugu language for OCR
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Adjust path if needed

st.title("Telugu PDF to Word Converter")
st.write("Upload a Telugu PDF, and it will be converted to a Word document with extracted text.")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    st.write("Processing the file...")
    
    # Convert PDF to images
    images = convert_from_bytes(uploaded_file.read())

    # Initialize a Word document
    document = Document()

    # Extract text using OCR for Telugu language
    for img in images:
        text = pytesseract.image_to_string(img, lang="tel")
        document.add_paragraph(text)

    # Save the extracted text to a Word document
    output = BytesIO()
    document.save(output)
    output.seek(0)

    # Provide a download link
    st.download_button(
        label="Download Word File",
        data=output,
        file_name="converted_telugu.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    st.success("Conversion complete! Click the button above to download your Word file.")

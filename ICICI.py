import streamlit as st
from pdf2image import convert_from_bytes
import pytesseract
from docx import Document
from io import BytesIO
import os

import pytesseract

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Set TESSDATA_PREFIX to ensure Telugu language is found
os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/4.00/tessdata/"

# Check available languages
print("Available Tesseract languages:", pytesseract.get_languages(config=''))

# Set up Tesseract path (Modify if needed)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"  # Linux/Mac
# Uncomment for Windows: 
# pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

st.title("📜 Telugu PDF to Word Converter")
st.write("Upload a Telugu PDF, and it will be converted to a Word document with extracted text.")

# File uploader
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file is not None:
    st.write("⏳ Processing the file...")

    # Convert PDF to images (high DPI for better OCR)
    images = convert_from_bytes(uploaded_file.read(), dpi=300)

    # Initialize a Word document
    document = Document()

    # Extract text using OCR for Telugu language
    for img in images:
        text = pytesseract.image_to_string(img, lang="tel", timeout=60)  # Telugu OCR with timeout
        document.add_paragraph(text)

    # Save the extracted text to a Word document
    output = BytesIO()
    document.save(output)
    output.seek(0)

    # Provide a download button for the user
    st.download_button(
        label="📥 Download Word File",
        data=output,
        file_name="converted_telugu.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    st.success("✅ Conversion complete! Click the button above to download your Word file.")

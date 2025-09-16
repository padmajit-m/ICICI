import streamlit as st
from zipfile import ZipFile
from io import BytesIO
import os

# Function to map old file name to new file name based on keywords
def rename_file(file_name, partnercustomerid, partnerloanid):
    name_lower = file_name.lower()
    new_name = None

    if "aadhaar" in name_lower and "coap" in name_lower:
        new_name = f"{partnercustomerid}_{partnerloanid}_Coapplicant1_POA_Aadhaar.jpg"
    elif "voter" in name_lower and "coap" in name_lower:
        new_name = f"{partnercustomerid}_{partnerloanid}_Coapplicant1_POI_Voterid.jpg"
    elif "bank" in name_lower and "stmt" in name_lower:
        new_name = f"{partnercustomerid}_{partnerloanid}_BankStatement.pdf"
    elif "pan" in name_lower and "coap" in name_lower:
        new_name = f"{partnercustomerid}_{partnerloanid}_Coapplicant1_Pan.jpg"
    elif "pan" in name_lower:
        new_name = f"{partnercustomerid}_{partnerloanid}_Pan.jpg"
    elif "voter" in name_lower and "back" in name_lower:
        new_name = f"{partnercustomerid}_{partnerloanid}_POI_Voterid_back.jpg"
    else:
        # If no keyword match, keep original name with prefix
        base, ext = os.path.splitext(file_name)
        new_name = f"{partnercustomerid}_{partnerloanid}_{base}{ext}"

    return new_name

# Streamlit UI
st.title("Document Renaming Tool")

partnercustomerid = st.text_input("Enter Partner Customer ID")
partnerloanid = st.text_input("Enter Partner Loan ID")

uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

if st.button("Rename and Download"):
    if not partnercustomerid or not partnerloanid:
        st.error("Please enter both Partner Customer ID and Partner Loan ID.")
    elif not uploaded_files:
        st.error("Please upload at least one file.")
    else:
        # Create in-memory zip file
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for uploaded_file in uploaded_files:
                original_name = uploaded_file.name
                new_name = rename_file(original_name, partnercustomerid, partnerloanid)
                content = uploaded_file.read()
                zip_file.writestr(new_name, content)

        zip_buffer.seek(0)
        st.download_button(
            label="Download Renamed Files",
            data=zip_buffer,
            file_name=f"{partnercustomerid}_{partnerloanid}_documents.zip",
            mime="application/zip"
        )

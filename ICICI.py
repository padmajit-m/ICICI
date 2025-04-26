# save this as app.py

import streamlit as st
import os
import zipfile
from PIL import Image, ImageDraw
import shutil

# Predefined document list
DOCUMENTS = [
    "POA_Voterid", "POA_Voterid_front", "POA_Voterid_back",
    "POA_Aadhaar", "POA_Aadhaar_front", "POA_Aadhaar_back",
    "POI_Voterid", "POI_Voterid_front", "POI_Voterid_back",
    "POI_Aadhaar", "POI_Aadhaar_front", "POI_Aadhaar_back",
    "Coapplicant1_POA_Voterid", "Coapplicant1_POA_Voterid_front", "Coapplicant1_POA_Voterid_back",
    "Coapplicant1_POA_Aadhaar", "Coapplicant1_POA_Aadhaar_front", "Coapplicant1_POA_Aadhaar_back",
    "Coapplicant1_POI_Voterid", "Coapplicant1_POI_Voterid_front", "Coapplicant1_POI_Voterid_back",
    "Coapplicant1_POI_Aadhaar", "Coapplicant1_POI_Aadhaar_front", "Coapplicant1_POI_Aadhaar_back",
    "Consent_Applicant", "Coapplicant1_Consent",
    "LoanDocuments", "CKYC", "BankPassbook", "BankStatement",
    "Photo", "Coapplicant1_Photo", "OwnershipProof",
    "BusinessPhoto", "ResidencePhoto",
    "SPDC", "DOGH", "UdyamAadhar", "ITR",
    "UDC", "OtherDocuments1", "OtherDocuments2", "OtherDocuments3"
]

def create_dummy_image(text, filename):
    img = Image.new('RGB', (400, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 90), text, fill=(0, 0, 0))
    img.save(filename)

def generate_documents(partner_customer_id, partner_loan_id, output_folder="generated_docs"):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)  # Clean old data
    os.makedirs(output_folder)

    for doc in DOCUMENTS:
        filename = f"{partner_customer_id}_{partner_loan_id}_{doc}.jpg"
        filepath = os.path.join(output_folder, filename)
        create_dummy_image(doc, filepath)

def zip_documents(output_folder="generated_docs", zip_name="documents.zip"):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for root, _, files in os.walk(output_folder):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)

st.title("📄 Dummy Loan Document Generator")

# UI inputs
partner_customer_id = st.text_input("Enter Partner Customer ID")
partner_loan_id = st.text_input("Enter Partner Loan ID")

if st.button("Generate & Download Documents"):
    if partner_customer_id and partner_loan_id:
        generate_documents(partner_customer_id, partner_loan_id)
        zip_documents()

        with open("documents.zip", "rb") as f:
            st.download_button("📥 Download ZIP", f, file_name="documents.zip")

        st.success("✅ Documents generated successfully!")
    else:
        st.warning("⚠️ Please enter both Partner Customer ID and Partner Loan ID.")


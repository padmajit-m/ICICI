import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta

# Function to generate random data
def generate_random_data():
    data = {
        "Bank Account Number": [str(random.randint(1000000000000, 9999999999999))],
        "KYC POI Proof No": [f"AB{random.randint(1000000, 9999999)}"],
        "KYC POA Proof No": [f"XY{random.randint(1000000, 9999999)}"],
        "Partner Application ID": [f"RPSTEST{random.randint(10, 99)}"],
        "Partner Customer ID": [f"CUST{random.randint(1000, 9999)}"],
        "Co-Applicant 1 Mobile Number": [f"9{random.randint(100000000, 999999999)}"],
        "Co-Applicant 1 Alternate contact number": [f"9{random.randint(100000000, 999999999)}"],
        "Mobile No.": [f"8{random.randint(100000000, 999999999)}"],
        "Group ID": [f"C209{random.randint(1000, 9999)}-G1"],
        "Co-Applicant 1 KYC POI Proof No": [f"PQR{random.randint(1000000, 9999999)}"],
        "Co-Applicant 1 First Name": ["John"],
        "Applicant Last Name": ["Doe"],
        "Applicant First Name": ["Jane"]
    }
    return pd.DataFrame(data)

# Function to generate LRR file
def generate_lrr(flat_file):
    application_date = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
    sanctioned_date = datetime.now().strftime('%Y-%m-%d')
    group_id = flat_file["Group ID"][0].split("-")[0]
    
    lrr_data = {
        "NAME_OF_BC": ["MIDLAND MICROFIN LIMITED"],
        "APPLICATION_DATE": [application_date],
        "DAY_OF_MEETING": [datetime.strptime(application_date, '%Y-%m-%d').strftime('%A')],
        "NAME_JLG_CENTRE": [group_id],
        "FIRST_NAME": [flat_file["Applicant First Name"][0]],
        "SANCTIONED_DATE": [sanctioned_date],
        "SANCTIONED_AMT": [60000],
        "URNID": [f"{random.randint(1000000, 9999999)}"],
        "APPLICATION_FORM_NO": [flat_file["Partner Application ID"][0]],
        "MEMBER_CLIENT_ID": [flat_file["Partner Customer ID"][0]]
    }
    return pd.DataFrame(lrr_data)

# Function to generate LBD file
def generate_lbd(lrr_file, flat_file):
    account_number = flat_file["Bank Account Number"][0]
    sanctioned_date = datetime.now().strftime('%Y-%m-%d')
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    lbd_data = {
        "PINSTID": [lrr_file["URNID"][0]],
        "NAME_OF_BC": ["MIDLAND MICROFIN LIMITED"],
        "UNIQUE_REFERENCE_NUMBER": [f"UR{random.randint(1000000, 9999999)}"],
        "APPLICATION_FORM_NO": [flat_file["Partner Application ID"][0]],
        "CUSTOMER_NAME": [flat_file["Applicant First Name"][0]],
        "CUSTOMER_ID": [flat_file["Partner Customer ID"][0]],
        "SANCTION_AMOUNT": [60000],
        "SANCTION_DATE": [sanctioned_date],
        "ACCOUNT_NUMBER": [account_number],
        "ACCOUNT_OPENING_DATE": [current_date_time],
        "EXPIRY_DATE": ["2047-06-05"]
    }
    return pd.DataFrame(lbd_data)

# Function to generate ADR Stage 1 file
def generate_adr_stage1(flat_file):
    installment_start_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    interest_start_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    adr1_data = {
        "Partner Loan ID": [flat_file["Partner Application ID"][0]],
        "Partner Customer ID": [flat_file["Partner Customer ID"][0]],
        "Originator Decision": ["APPROVE"],
        "Installment Start Date": [installment_start_date],
        "Interest Start Date": [interest_start_date]
    }
    return pd.DataFrame(adr1_data)

# Function to generate ADR Stage 2 file
def generate_adr_stage2(flat_file):
    disbursement_date = datetime.now().strftime('%Y-%m-%d')
    
    adr2_data = {
        "Partner Loan ID": [flat_file["Partner Application ID"][0]],
        "Partner Customer ID": [flat_file["Partner Customer ID"][0]],
        "Originator Disbursement Date": [disbursement_date],
        "Originator Disbursement Amount": [60000],
        "Bc Reimbursement Ac No": [flat_file["Bank Account Number"][0]]
    }
    return pd.DataFrame(adr2_data)

# Streamlit UI
st.title("Loan Creation Flow File Generator")

if st.button('Generate Files'):
    # Generate random flat file data
    flat_file = generate_random_data()
    
    # Generate the respective files based on the flat file
    lrr_file = generate_lrr(flat_file)
    lbd_file = generate_lbd(lrr_file, flat_file)
    adr1_file = generate_adr_stage1(flat_file)
    adr2_file = generate_adr_stage2(flat_file)
    
    # Provide download links for the generated files
    st.success('Files generated successfully!')
    
    st.download_button(label="Download Flat File", data=flat_file.to_csv(index=False), file_name='flat_file.csv', mime='text/csv')
    st.download_button(label="Download LRR File", data=lrr_file.to_csv(index=False), file_name='lrr_file.csv', mime='text/csv')
    st.download_button(label="Download LBD File", data=lbd_file.to_csv(index=False), file_name='lbd_file.csv', mime='text/csv')
    st.download_button(label="Download ADR Stage 1 File", data=adr1_file.to_csv(index=False), file_name='adr1_file.csv', mime='text/csv')
    st.download_button(label="Download ADR Stage 2 File", data=adr2_file.to_csv(index=False), file_name='adr2_file.csv', mime='text/csv')

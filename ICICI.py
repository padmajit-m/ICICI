import streamlit as st
import pandas as pd
import random
import io

# Function to generate random data based on format and length
def generate_random_value(format_type, length):
    if format_type == 'alphanumeric':
        return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=length))
    elif format_type == 'numeric':
        return ''.join(random.choices('0123456789', k=length))
    elif format_type == 'date':
        return pd.to_datetime('today').strftime('%d-%m-%Y')
    return None

# Function to generate each file's data
def generate_flat_file():
    data = {
        'Bank Account Number': [generate_random_value('numeric', 12)],
        'KYC POI Proof No': [generate_random_value('alphanumeric', 10)],
        'KYC POA Proof No': [generate_random_value('alphanumeric', 10)],
        'Partner Application ID': [generate_random_value('alphanumeric', 8)],
        'Partner Customer ID': [generate_random_value('alphanumeric', 8)],
        'Co-Applicant 1 Mobile Number': [generate_random_value('numeric', 10)],
        'Co-Applicant 1 Alternate contact number': [generate_random_value('numeric', 10)],
        'Mobile No.': [generate_random_value('numeric', 10)],
        'Group ID': [f'C209{random.randint(1000,9999)}-G{random.randint(1,9)}'],
        'Co-Applicant 1 KYC POI Proof No': [generate_random_value('alphanumeric', 10)],
        'Co-Applicant 1 First Name': ['John'],
        'Applicant Last Name': ['Doe'],
        'Applicant First Name': ['Jane'],
        'Date of Application': [(pd.to_datetime('today') - pd.DateOffset(days=5)).strftime('%d-%m-%Y')],
    }
    df = pd.DataFrame(data)
    return df

# Function to generate LRR File
def generate_lrr_file(flat_file):
    df = pd.DataFrame({
        'NAME_OF_BC': ['MIDLAND MICROFIN LIMITED'],
        'APPLICATION_DATE': [flat_file['Date of Application'].values[0]],
        'DAY_OF_MEETING': [pd.to_datetime(flat_file['Date of Application'].values[0]).strftime('%A')],
        'NAME_JLG_CENTRE': [flat_file['Group ID'].values[0].split('-')[0]],
        'FIRST_NAME': [flat_file['Applicant First Name'].values[0]],
        'SANCTIONED_DATE': [pd.to_datetime('today').strftime('%d-%m-%Y')],
        'SANCTIONED_AMT': [50000],
        'URNID': [generate_random_value('numeric', 8)],
        'APPLICATION_FORM_NO': [flat_file['Partner Application ID'].values[0]],
        'MEMBER_CLIENT_ID': [flat_file['Partner Customer ID'].values[0]]
    })
    return df

# Function to generate LBD File
def generate_lbd_file(lrr_file):
    df = pd.DataFrame({
        'PINSTID': [f'JLG-{generate_random_value("numeric", 6)}-PRO'],
        'NAME_OF_BC': ['MIDLAND'],
        'UNIQUE_REFERENCE_NUMBER': [generate_random_value('alphanumeric', 10)],
        'APPLICATION_FORM_NO': [lrr_file['APPLICATION_FORM_NO'].values[0]],
        'CUSTOMER_NAME': [lrr_file['FIRST_NAME'].values[0]],
        'CUSTOMER_ID': [lrr_file['MEMBER_CLIENT_ID'].values[0]],
        'SANCTION_AMOUNT': [lrr_file['SANCTIONED_AMT'].values[0]],
        'SANCTION_DATE': [lrr_file['SANCTIONED_DATE'].values[0]],
        'ACCOUNT_NUMBER': ['ICICI' + generate_random_value('numeric', 10)],
        'ACCOUNT_OPENING_DATE': [pd.to_datetime('today').strftime('%d-%m-%Y %H:%M:%S')],
        'EXPIRY_DATE': ['2047-06-05']
    })
    return df

# Function to generate ADR Stage 1 File
def generate_adr_stage1_file(flat_file):
    df = pd.DataFrame({
        'Partner Loan ID': [flat_file['Partner Application ID'].values[0]],
        'Partner Customer ID': [flat_file['Partner Customer ID'].values[0]],
        'Originator Decision': ['APPROVE'],
        'Installment Start Date': [(pd.to_datetime('today') + pd.DateOffset(months=1)).strftime('%d-%m-%Y')],
        'Interest Start Date': [(pd.to_datetime('today') + pd.DateOffset(days=1)).strftime('%d-%m-%Y')]
    })
    return df

# Function to generate ADR Stage 2 File
def generate_adr_stage2_file(flat_file):
    df = pd.DataFrame({
        'Partner Loan ID': [flat_file['Partner Application ID'].values[0]],
        'Partner Customer ID': [flat_file['Partner Customer ID'].values[0]],
        'Originator Disbursement Date': [pd.to_datetime('today').strftime('%d-%m-%Y')],
        'Originator Disbursement Amount': [60000],
        'Bc Reimbursement Ac No': [flat_file['Bank Account Number'].values[0]]
    })
    return df

# Streamlit app logic
st.title('Loan File Generator')

if st.button('Generate Files'):
    # Generate all files
    flat_file = generate_flat_file()
    lrr_file = generate_lrr_file(flat_file)
    lbd_file = generate_lbd_file(lrr_file)
    adr_stage1_file = generate_adr_stage1_file(flat_file)
    adr_stage2_file = generate_adr_stage2_file(flat_file)

    # Create buffers for each file
    files = {
        'Flat_File.xlsx': flat_file,
        'LRR_File.xlsx': lrr_file,
        'LBD_File.xlsx': lbd_file,
        'ADR_Stage1_File.xlsx': adr_stage1_file,
        'ADR_Stage2_File.xlsx': adr_stage2_file,
    }
    
    # Generate download buttons without page refresh
    for file_name, df in files.items():
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.close()  # Use close() instead of save()
        st.download_button(
            label=f"Download {file_name}",
            data=output.getvalue(),
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

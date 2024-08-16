import io
import random
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st

# Generate random values based on the required formats
def generate_random_data():
    return {
        'Bank Account Number': f'ICICI{random.randint(1000000000, 9999999999)}',
        'KYC POI Proof No': f'A{random.randint(1000000000, 9999999999)}',
        'KYC POA Proof No': f'B{random.randint(1000000000, 9999999999)}',
        'Partner Application ID': f'RPSTEST{random.randint(1000, 9999)}P',
        'Partner Customer ID': f'RPSTEST{random.randint(1000, 9999)}P',
        'Co-Applicant 1 Mobile Number': f'9{random.randint(1000000000, 9999999999)}',
        'Co-Applicant 1 Alternate contact number': f'9{random.randint(1000000000, 9999999999)}',
        'Mobile No.': f'9{random.randint(1000000000, 9999999999)}',
        'Group ID': f'C{random.randint(2092500, 2092999)}-G1',
        'Co-Applicant 1 KYC POI Proof No': f'C{random.randint(1000000000, 9999999999)}',
        'Co-Applicant 1 First Name': 'Mani',
        'Applicant Last Name': 'Sharma',
        'Applicant First Name': 'Arun'
    }

# Generate the LRR file based on the Flat file data
def generate_lrr(flat_data):
    application_date = (datetime.now() - timedelta(days=5)).strftime('%d/%m/%Y')
    first_name = flat_data['Applicant First Name']
    group_id = flat_data['Group ID'].split('-')[0]
    loan_amount = random.randint(30000, 70000)

    lrr_data = {
        'NAME_OF_BC': 'MIDLAND MICROFIN LIMITED',
        'APPLICATION_DATE': application_date,
        'DAY_OF_MEETING': 'SATURDAY',
        'NAME_JLG_CENTRE': group_id,
        'FIRST_NAME': first_name,
        'SANCTIONED_DATE': datetime.now().strftime('%d-%m-%Y'),
        'SANCTIONED_AMT': loan_amount,
        'URNID': random.randint(10000000, 99999999),
        'APPLICATION_FORM_NO': flat_data['Partner Application ID'],
        'MEMBER_CLIENT_ID': flat_data['Partner Customer ID']
    }
    return pd.DataFrame([lrr_data])

# Generate the LBD file based on the LRR data
def generate_lbd(flat_data, lrr_data):
    lbd_data = {
        'PINSTID': f'JLG-{random.randint(100000, 999999)}-PRO',
        'NAME_OF_BC': lrr_data['NAME_OF_BC'][0],
        'UNIQUE_REFERENCE_NUMBER': f'RPSTEST{random.randint(1000, 9999)}P',
        'CLIENT_ID': flat_data['Partner Customer ID'],
        'APPLICATION_FORM_NO': flat_data['Partner Application ID'],
        'CUSTOMER_NAME': flat_data['Applicant First Name'],
        'CUSTOMER_ID': flat_data['Partner Customer ID'],
        'SANCTION_AMOUNT': lrr_data['SANCTIONED_AMT'][0],
        'SANCTION_DATE': lrr_data['SANCTIONED_DATE'][0],
        'ACCOUNT_NUMBER': flat_data['Bank Account Number'],
        'ACCOUNT_OPENING_DATE': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'EXPIRY_DATE': '2047-06-05'
    }
    return pd.DataFrame([lbd_data])

# Generate the ADR Stage 1 file based on the Flat file data
def generate_adr_stage1(flat_data):
    adr_stage1_data = {
        'Partner Loan ID': flat_data['Partner Application ID'],
        'Partner Customer ID': flat_data['Partner Customer ID'],
        'Originator Decision': 'APPROVE',
        'Installment Start Date': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'Interest Start Date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    }
    return pd.DataFrame([adr_stage1_data])

# Generate the ADR Stage 2 file based on the Flat file data
def generate_adr_stage2(flat_data):
    adr_stage2_data = {
        'Partner Loan ID': flat_data['Partner Application ID'],
        'Partner Customer ID': flat_data['Partner Customer ID'],
        'Originator Disbursement Date': datetime.now().strftime('%Y-%m-%d'),
        'Originator Disbursement Amount': random.randint(30000, 70000),
        'Bc Reimbursement Ac No': flat_data['Bank Account Number']
    }
    return pd.DataFrame([adr_stage2_data])

# Convert dataframes to Excel format
def to_excel(df_dict):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        writer.close()

    return output.getvalue()

# Streamlit app
def main():
    st.title("Loan Creation Flow File Generator")

    if st.button("Generate Files"):
        # Generate the data
        flat_data = generate_random_data()
        lrr_data = generate_lrr(flat_data)
        lbd_data = generate_lbd(flat_data, lrr_data)
        adr_stage1_data = generate_adr_stage1(flat_data)
        adr_stage2_data = generate_adr_stage2(flat_data)

        # Store dataframes in a dictionary
        df_dict = {
            'Flat File': pd.DataFrame([flat_data]),
            'LRR File': lrr_data,
            'LBD File': lbd_data,
            'ADR Stage 1 File': adr_stage1_data,
            'ADR Stage 2 File': adr_stage2_data
        }

        # Convert to Excel
        excel_data = to_excel(df_dict)

        # Download the file
        st.download_button(
            label="Download Excel",
            data=excel_data,
            file_name="loan_files.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()

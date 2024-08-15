import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
from io import BytesIO

# Generate random data based on your requirements
def generate_random_data():
    group_id_series = random.randint(2092527, 3092527)
    current_date = datetime.now()
    date_of_application = current_date - timedelta(days=5)

    flat_data = {
        "Group ID": f"C{group_id_series}-G{random.randint(1, 9)}",
        "Bank Account Number": f"{random.randint(100000000000, 999999999999)}",
        "KYC POI Proof No": f"RPS{random.randint(1000000, 9999999)}",
        "KYC POA Proof No": f"RJ{random.randint(100000000, 999999999)}",
        "Partner Application ID": f"RPSTEST{random.randint(1, 99)}P",
        "Partner Customer ID": f"RPSTEST{random.randint(1, 99)}P",
        "Mobile No.": f"{random.randint(9000000000, 9999999999)}",
        "Co-Applicant 1 Mobile Number": f"{random.randint(9000000000, 9999999999)}",
        "Co-Applicant 1 Alternate contact number": f"{random.randint(9000000000, 9999999999)}",
        "Applicant First Name": "Mani",
        "Applicant Last Name": "Shree",
        "Date of Application": date_of_application.strftime("%d/%m/%Y"),
        "Loan Amount": 60000
    }
    
    lrr_data = {
        "NAME_OF_BC": "MIDLAND MICROFIN LIMITED",
        "APPLICATION_DATE": flat_data["Date of Application"],
        "DAY_OF_MEETING": date_of_application.strftime("%A").upper(),
        "NAME_JLG_CENTRE": flat_data["Group ID"].split("-")[0],
        "FIRST_NAME": flat_data["Applicant First Name"],
        "SANCTIONED_DATE": current_date.strftime("%d-%m-%Y"),
        "SANCTIONED_AMT": flat_data["Loan Amount"],
        "URNID": random.randint(10000000, 99999999),
        "APPLICATION_FORM_NO": flat_data["Partner Application ID"],
        "MEMBER_CLIENT_ID": flat_data["Partner Customer ID"]
    }
    
    lbd_data = {
        "PINSTID": lrr_data["URNID"],
        "NAME_OF_BC": lrr_data["NAME_OF_BC"],
        "UNIQUE_REFERENCE_NUMBER": random.randint(1000000, 9999999),
        "CLIENT_ID": lrr_data["MEMBER_CLIENT_ID"],
        "APPLICATION_FORM_NO": lrr_data["APPLICATION_FORM_NO"],
        "CUSTOMER_NAME": lrr_data["FIRST_NAME"],
        "CUSTOMER_ID": lrr_data["MEMBER_CLIENT_ID"],
        "SANCTION_AMOUNT": lrr_data["SANCTIONED_AMT"],
        "SANCTION_DATE": lrr_data["SANCTIONED_DATE"],
        "ACCOUNT_NUMBER": flat_data["Bank Account Number"],
        "ACCOUNT_OPENING_DATE": current_date.strftime("%Y-%m-%d %H:%M:%S"),
        "EXPIRY_DATE": (current_date + timedelta(days=30)).strftime("%d-%m-%Y")
    }
    
    adr_stage1_data = {
        "Partner Loan ID": flat_data["Partner Application ID"],
        "Partner Customer ID": flat_data["Partner Customer ID"],
        "Originator Decision": "APPROVE",
        "Installment Start Date": (current_date + timedelta(days=30)).strftime("%d-%m-%Y"),
        "Interest Start Date": (current_date + timedelta(days=1)).strftime("%d-%m-%Y")
    }
    
    adr_stage2_data = {
        "Partner Loan ID": flat_data["Partner Application ID"],
        "Partner Customer ID": flat_data["Partner Customer ID"],
        "Originator Disbursement Date": current_date.strftime("%d-%m-%Y"),
        "Originator Disbursement Amount": flat_data["Loan Amount"],
        "Bc Reimbursement Ac No": flat_data["Bank Account Number"]
    }

    return flat_data, lrr_data, lbd_data, adr_stage1_data, adr_stage2_data

# Convert DataFrame to Excel in memory
def to_excel(df_dict):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    
    for sheet_name, df in df_dict.items():
        df.to_excel(writer, index=False, sheet_name=sheet_name)
    
    writer.save()
    processed_data = output.getvalue()
    return processed_data

# Initialize session state
if 'generated_files' not in st.session_state:
    st.session_state['generated_files'] = {}

# Main Streamlit app
st.title("Loan File Generator")

if st.button("Generate Loan Files"):
    flat_data, lrr_data, lbd_data, adr_stage1_data, adr_stage2_data = generate_random_data()
    
    # Create DataFrames
    df_flat = pd.DataFrame([flat_data])
    df_lrr = pd.DataFrame([lrr_data])
    df_lbd = pd.DataFrame([lbd_data])
    df_adr_stage1 = pd.DataFrame([adr_stage1_data])
    df_adr_stage2 = pd.DataFrame([adr_stage2_data])

    # Store the Excel files in session state
    st.session_state['generated_files'] = {
        'Flat File.xlsx': to_excel({"Flat File": df_flat}),
        'LRR File.xlsx': to_excel({"LRR File": df_lrr}),
        'LBD File.xlsx': to_excel({"LBD File": df_lbd}),
        'ADR Stage 1 File.xlsx': to_excel({"ADR Stage 1": df_adr_stage1}),
        'ADR Stage 2 File.xlsx': to_excel({"ADR Stage 2": df_adr_stage2})
    }

if st.session_state['generated_files']:
    st.download_button("Download Flat File", data=st.session_state['generated_files']['Flat File.xlsx'], file_name='Flat File.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    st.download_button("Download LRR File", data=st.session_state['generated_files']['LRR File.xlsx'], file_name='LRR File.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    st.download_button("Download LBD File", data=st.session_state['generated_files']['LBD File.xlsx'], file_name='LBD File.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    st.download_button("Download ADR Stage 1 File", data=st.session_state['generated_files']['ADR Stage 1 File.xlsx'], file_name='ADR Stage 1 File.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    st.download_button("Download ADR Stage 2 File", data=st.session_state['generated_files']['ADR Stage 2 File.xlsx'], file_name='ADR Stage 2 File.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

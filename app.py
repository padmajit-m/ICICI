import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Total EMI Calculator 📊")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        if 'AccountId/ Partner Loan ID' not in df.columns or 'EMI' not in df.columns:
            st.error("File must contain 'AccountId/ Partner Loan ID' and 'EMI' columns.")
        else:
            result_df = df.groupby('AccountId/ Partner Loan ID')['EMI'].sum().reset_index()
            result_df.columns = ['AccountId/ Partner Loan ID', 'Total EMI Amount']
            st.success("✅ Total EMI calculated!")

            st.dataframe(result_df)

            # Convert to Excel
            output = BytesIO()

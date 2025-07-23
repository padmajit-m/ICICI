import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Total EMI Calculator 📊")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        if 'AccountId/ Partner Loan ID' not in df.columns or 'EMI' not in df.columns:
            st.error("❌ Columns 'AccountId/ Partner Loan ID' and 'EMI' are required.")
        else:
            result_df = df.groupby('AccountId/ Partner Loan ID')['EMI'].sum().reset_index()
            result_df.columns = ['AccountId/ Partner Loan ID', 'Total EMI Amount']

            st.success("✅ Total EMI calculated!")
            st.dataframe(result_df)

            # Output Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                result_df.to_excel(writer, index=False)
            output.seek(0)

            st.download_button(
                label="📥 Download Result as Excel",
                data=output,
                file_name='total_emi_result.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    except Exception as e:
        st.error(f"❌ Failed to process file: {e}")

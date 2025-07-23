import streamlit as st
import pandas as pd
from io import BytesIO

st.title("🧮 Total EMI & Principal Calculator")

uploaded_file = st.file_uploader("📤 Upload Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Check if required columns exist
        required_columns = ['AccountId/ Partner Loan ID', 'EMI', 'Principal']
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ Required columns missing: {required_columns}")
        else:
            # Group and calculate both EMI and Principal
            result_df = df.groupby('AccountId/ Partner Loan ID')[['EMI', 'Principal']].sum().reset_index()
            result_df.columns = ['AccountId/ Partner Loan ID', 'Total EMI Amount', 'Total Principal']

            st.success("✅ Calculation complete!")
            st.dataframe(result_df)

            # Prepare downloadable Excel
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                result_df.to_excel(writer, index=False)
            output.seek(0)

            st.download_button(
                label="📥 Download Result as Excel",
                data=output,
                file_name='emi_principal_summary.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

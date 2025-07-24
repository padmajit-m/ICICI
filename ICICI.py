import streamlit as st
import pandas as pd
from io import BytesIO

st.title("📊 EMI & Principal Calculator with Adjusted EMI Dates")

uploaded_file = st.file_uploader("📤 Upload Excel file", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Ensure required columns are present
        required_columns = ['AccountId/ Partner Loan ID', 'EMI', 'Principal', 'EMI date']
        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ Required columns missing: {required_columns}")
        else:
            # Ensure 'EMI date' is datetime
            df['EMI date'] = pd.to_datetime(df['EMI date'])

            updated_records = []

            for acc_id, group in df.groupby('AccountId/ Partner Loan ID'):
                group = group.sort_values('EMI date').reset_index(drop=True)

                # Drop last EMI record
                group = group.iloc[:-1].copy()

                # Insert new EMI at top
                new_row = group.iloc[0].copy()
                new_row['EMI date'] = pd.to_datetime("2025-06-30")
                group = pd.concat([pd.DataFrame([new_row]), group], ignore_index=True)

                updated_records.append(group)

            updated_df = pd.concat(updated_records, ignore_index=True)

            # Create summary table
            summary_df = updated_df.groupby('AccountId/ Partner Loan ID').agg(
                Total_EMI_Amount=('EMI', 'sum'),
                Total_Principal=('Principal', 'sum'),
                Total_EMI_Count=('EMI', 'count')
            ).reset_index()

            st.success("✅ EMI dates adjusted and totals calculated!")

            st.subheader("🔁 Adjusted EMI Schedule")
            st.dataframe(updated_df)

            st.subheader("📋 Summary")
            st.dataframe(summary_df)

            # Prepare Excel file with 2 sheets
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                updated_df.to_excel(writer, sheet_name='Adjusted EMI Schedule', index=False)
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
            output.seek(0)

            st.download_button(
                label="📥 Download Adjusted EMI Excel",
                data=output,
                file_name='adjusted_emi_with_summary.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

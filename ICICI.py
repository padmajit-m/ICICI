import streamlit as st
from zipfile import ZipFile
from io import BytesIO
import os

# Function to map old file name to new file name based on keywords
def rename_file(file_name, partnercustomerid, partnerloanid):
    name_lower = file_name.lower()
    base, ext = os.path.splitext(file_name)

    if "aadhaar" in name_lower and "coap" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_POA_Aadhaar{ext}"
    elif "voter" in name_lower and "coap" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_POI_Voterid{ext}"
    elif "bank" in name_lower and "stmt" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_BankStatement{ext}"
    elif "pan" in name_lower and "coap" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_Pan{ext}"
    elif "pan" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Pan{ext}"
    elif "voter" in name_lower and "back" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_POI_Voterid_back{ext}"
    else:
        # Return None if file doesn't match any known pattern
        return None

# Streamlit UI
st.title("Document Renaming Tool with Exception Folder")

partnercustomerid = st.text_input("Enter Partner Customer ID")
partnerloanid = st.text_input("Enter Partner Loan ID")

uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)

if st.button("Rename and Download"):
    if not partnercustomerid or not partnerloanid:
        st.error("Please enter both Partner Customer ID and Partner Loan ID.")
    elif not uploaded_files:
        st.error("Please upload at least one file.")
    else:
        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            renamed_count = 0
            exception_count = 0

            for uploaded_file in uploaded_files:
                original_name = uploaded_file.name
                new_name = rename_file(original_name, partnercustomerid, partnerloanid)
                content = uploaded_file.read()

                if new_name:
                    zip_file.writestr(new_name, content)
                    renamed_count += 1
                else:
                    # Put unmatched files into Exception folder
                    zip_file.writestr(f"Exception/{original_name}", content)
                    exception_count += 1

        zip_buffer.seek(0)

        if renamed_count > 0 or exception_count > 0:
            st.download_button(
                label="Download Zip File",
                data=zip_buffer,
                file_name=f"{partnercustomerid}_{partnerloanid}_documents.zip",
                mime="application/zip"
            )
            st.success(f"Renamed {renamed_count} file(s), {exception_count} file(s) placed in Exception folder.")
        else:
            st.error("No files uploaded.")

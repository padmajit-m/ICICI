import streamlit as st
from zipfile import ZipFile
from io import BytesIO

# Function to map old file name to new file name based on keywords
def rename_file(file_name, partnercustomerid, partnerloanid):
    name_lower = file_name.lower()
    
    if "aadhaar" in name_lower and "coap" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_POA_Aadhaar.jpg"
    elif "voter" in name_lower and "coap" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_POI_Voterid.jpg"
    elif "bank" in name_lower and "stmt" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_BankStatement.jpg"
    elif "pan" in name_lower and "coap" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_Pan.jpg"
    elif "pan" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Pan.jpg"
    elif "voter" in name_lower and "back" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_POI_Voterid_back.jpg"
    else:
        # Return None if file doesn't match any known pattern
        return None

# Streamlit UI
st.title("Document Renaming Tool")

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
            added_files = 0
            for uploaded_file in uploaded_files:
                original_name = uploaded_file.name
                new_name = rename_file(original_name, partnercustomerid, partnerloanid)
                
                if new_name:
                    content = uploaded_file.read()
                    zip_file.writestr(new_name, content)
                    added_files += 1

        zip_buffer.seek(0)

        if added_files > 0:
            st.download_button(
                label="Download Renamed Files",
                data=zip_buffer,
                file_name=f"{partnercustomerid}_{partnerloanid}_documents.zip",
                mime="application/zip"
            )
        else:
            st.error("No files matched the required naming patterns.")

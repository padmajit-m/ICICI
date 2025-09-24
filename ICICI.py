import streamlit as st
from zipfile import ZipFile
from io import BytesIO
import os

# Function to map old file name to new file name based on keywords
def rename_file(file_name, partnercustomerid, partnerloanid):
    name_lower = file_name.lower()
    base, ext = os.path.splitext(file_name)

    # Maintain original extension as uploaded
    if "aadhaar" in name_lower and "coap" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_POA_Aadhaar{ext}"

    elif "voter" in name_lower and "coap" in name_lower and "back" not in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_POI_Voterid{ext}"

    elif "voter" in name_lower and "back" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_POI_Voterid_back{ext}"

    elif "bank" in name_lower and ("stmt" in name_lower or "statement" in name_lower):
        return f"{partnercustomerid}_{partnerloanid}_BankStatement{ext}"

    elif "bankpassbook" in name_lower or "passbook" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_BankStatement{ext}"

    elif "pan" in name_lower and "coap" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_Pan{ext}"

    elif "pan" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Pan{ext}"

    elif "photo" in name_lower and "coap" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Coapplicant1_Photo{ext}"

    elif "photo" in name_lower and "business" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_BusinessPhoto{ext}"

    elif "photo" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Photo{ext}"

    elif "loan" in name_lower and "document" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_LoanDocuments{ext}"

    elif "enach" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Enach{ext}"

    elif "pdc" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_Pdc{ext}"

    elif "dpn" in name_lower:
        return f"{partnercustomerid}_{partnerloanid}_DPN{ext}"

    elif "otherdocuments" in name_lower:
        # Map OtherDocuments (you can refine by number if specific mapping needed)
        return f"{partnercustomerid}_{partnerloanid}_OtherDocuments{ext}"

    else:
        return None  # send to Exception folder


# ---------------- Streamlit UI ----------------
st.title("📂 System File Renaming Tool (ZIP → ZIP)")

partnercustomerid = st.text_input("Enter Partner Customer ID")
partnerloanid = st.text_input("Enter Partner Loan ID")

uploaded_zip = st.file_uploader("Upload System 1 ZIP file", type=["zip"])

if st.button("Process and Download"):
    if not partnercustomerid or not partnerloanid:
        st.error("⚠️ Please enter both Partner Customer ID and Partner Loan ID.")
    elif not uploaded_zip:
        st.error("⚠️ Please upload the System 1 ZIP file.")
    else:
        # Create new ZIP buffer
        output_buffer = BytesIO()
        with ZipFile(uploaded_zip, "r") as input_zip, ZipFile(output_buffer, "w") as output_zip:
            renamed_count = 0
            exception_count = 0

            for file_name in input_zip.namelist():
                if file_name.endswith("/"):  # skip directories
                    continue

                content = input_zip.read(file_name)
                new_name = rename_file(file_name, partnercustomerid, partnerloanid)

                if new_name:
                    output_zip.writestr(new_name, content)
                    renamed_count += 1
                else:
                    # Put unmatched files in "Exception/" folder
                    output_zip.writestr(f"Exception/{os.path.basename(file_name)}", content)
                    exception_count += 1

        output_buffer.seek(0)
        st.download_button(
            label="⬇️ Download Processed ZIP",
            data=output_buffer,
            file_name=f"{partnercustomerid}_{partnerloanid}_documents.zip",
            mime="application/zip"
        )
        st.success(f"✅ Renamed {renamed_count} file(s), ⚠️ {exception_count} file(s) moved to Exception folder.")

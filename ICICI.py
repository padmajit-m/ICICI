import os
import shutil

# 📌 Update this to your extracted folder path
INPUT_FOLDER = r"C:\path\to\your\files"
EXCEPTION_FOLDER = os.path.join(INPUT_FOLDER, "exceptions")

# Create exceptions folder if not exists
os.makedirs(EXCEPTION_FOLDER, exist_ok=True)

# Mapping rules (assumed from your requirement)
NAME_MAP = {
    "PAN": "Pan",
    "Coapplicant1_PAN": "Coapplicant1_Pan",
    "Coapplicant1_Photo": "Coapplicant1_Photo",
    "Coapplicant1_POI_VoterId": "Coapplicant1_POI_Voterid",
    "POI_VoterId": "POI_Voterid",
    "BankPassbook": "BankStatement",
    "BusinessPhoto": "BusinessPhoto",
    "OtherDocuments4": "Photo",
    "OtherDocuments5": "Enach",
    "Enach": "Enach",
    "Photo": "Photo",
    "LoanDocuments": "LoanDocuments",
    "DPN_1": "DPN",
    "Pdc": "Pdc"
}

def normalize_filename(filename):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()  # keep extension lowercase

    for key, new_val in NAME_MAP.items():
        if key in name:
            # replace only the matched part
            new_name = name.replace(key, new_val)
            return new_name + ext
    return None  # mark as exception if no match

def rename_files():
    for file in os.listdir(INPUT_FOLDER):
        if os.path.isdir(os.path.join(INPUT_FOLDER, file)):
            continue

        new_name = normalize_filename(file)
        src = os.path.join(INPUT_FOLDER, file)

        if new_name:
            # Remove duplicate extensions like ".jpeg.jpeg"
            if new_name.count('.') > 1:
                parts = new_name.split('.')
                new_name = parts[0] + '.' + parts[-1]

            dst = os.path.join(INPUT_FOLDER, new_name)
            os.rename(src, dst)
            print(f"✅ Renamed: {file} -> {new_name}")
        else:
            # Move to exceptions folder
            dst = os.path.join(EXCEPTION_FOLDER, file)
            shutil.move(src, dst)
            print(f"⚠️ Moved to exceptions: {file}")

if __name__ == "__main__":
    rename_files()

import pandas as pd
import os
from datetime import datetime

# === CONFIGURATION ===
SITE_ID = "CRT_FL"  # <-- CHANGE this to your assigned SiteID
INPUT_FOLDER = "files"
SURVEY_INPUT = os.path.join(INPUT_FOLDER, "redcap_survey_data.csv")
CONTEXT_INPUT = os.path.join(INPUT_FOLDER, "contextual_file.csv")

# === TIMESTAMP ===
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")

SURVEY_OUTPUT = os.path.join(INPUT_FOLDER, f"CS4_{SITE_ID}_Survey_Data_{timestamp}.csv")
CONTEXT_OUTPUT = os.path.join(INPUT_FOLDER, f"CS4_{SITE_ID}_Contextual_{timestamp}.csv")

# === CONFIGURATION FOR SPECIAL FIELDS ===
MULTICODE_COLUMNS = {"c5_2", "c5_5"}  # Contextual columns that need e.g., "01" → "0,1"


# === VALUE CLEANERS ===
def clean_value(val, colname=None):
    if pd.isna(val):
        return ""

    try:
        val_str = str(val).strip()

        # Match exact column name for admin_5
        if colname == "admin_5":
            try:
                parsed = pd.to_datetime(val_str)
                return parsed.strftime("%m/%d/%Y")
            except:
                pass

        # Convert float (or stringified float) with no decimal part to int
        if isinstance(val, float) and val.is_integer():
            return str(int(val))

        if "." in val_str:
            val_float = float(val_str)
            if val_float.is_integer():
                return str(int(val_float))

    except:
        pass

    return val_str.replace('|', '').replace('\n', ' ').replace('\r', ' ')

def clean_contextual_value(val, colname=None):
    val = clean_value(val, colname)
    if colname in MULTICODE_COLUMNS and val.isdigit() and len(val) > 1:
        val = ",".join(val)  # e.g., "01" → "0,1"
    return val

# === FILE PROCESSOR ===
def clean_and_export(input_path, output_path, is_contextual=False):
    print(f"Loading {input_path}...")
    df = pd.read_csv(input_path, dtype=str)

    if is_contextual:
        df = df.apply(lambda col: col.map(lambda val: clean_contextual_value(val, col.name)), axis=0)
    else:
        df = df.apply(lambda col: col.map(lambda val: clean_value(val, col.name)), axis=0)

    print(f"Saving cleaned data to {output_path} (pipe-delimited)...")
    df.to_csv(
        output_path,
        sep='|',
        index=False,
        encoding='utf-8',
        lineterminator='\n',
        quoting=0  # Avoid unnecessary quoting
    )
    print(f"✅ Finished writing: {output_path}")

# === RUN PROCESS ===
clean_and_export(SURVEY_INPUT, SURVEY_OUTPUT, is_contextual=False)
clean_and_export(CONTEXT_INPUT, CONTEXT_OUTPUT, is_contextual=True)
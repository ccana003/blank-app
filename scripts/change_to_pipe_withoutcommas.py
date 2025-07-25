import pandas as pd
import os
from datetime import datetime

# === CONFIGURATION ===
SITE_ID = "101"  # <-- change this to your actual SiteID
INPUT_FOLDER = "files"
SURVEY_INPUT = os.path.join(INPUT_FOLDER, "redcap_survey_data.csv")
CONTEXT_INPUT = os.path.join(INPUT_FOLDER, "contextual_file.csv")

# === TIMESTAMP ===
now = datetime.now()
timestamp = now.strftime("%Y%m%d_%H%M%S")

SURVEY_OUTPUT = os.path.join(INPUT_FOLDER, f"CS4_{SITE_ID}_Survey_Data_{timestamp}.csv")
CONTEXT_OUTPUT = os.path.join(INPUT_FOLDER, f"CS4_{SITE_ID}_Contextual_{timestamp}.csv")

# === CLEAN FUNCTION ===
def clean_value(val):
    if pd.isna(val):
        return ""
    val = str(val)
    val = val.replace('|', '')  # remove pipe characters
    val = val.replace('\n', ' ').replace('\r', ' ')  # remove newlines
    return val.strip()

def clean_and_export(input_path, output_path):
    print(f"Loading {input_path}...")
    df = pd.read_csv(input_path, dtype=str)
    df = df.map(clean_value)

    print(f"Saving cleaned data to {output_path} (pipe-delimited)...")
    df.to_csv(output_path, sep='|', index=False, encoding='utf-8', lineterminator='\n')
    print(f"✅ Finished writing: {output_path}")

# === RUN FOR BOTH FILES ===
clean_and_export(SURVEY_INPUT, SURVEY_OUTPUT)
clean_and_export(CONTEXT_INPUT, CONTEXT_OUTPUT)

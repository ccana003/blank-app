# scripts/extract_redcap_data.py
import requests
import pandas as pd
import os

# === CONFIGURATION ===
API_URL = "https://redcap.miami.edu/api/"
API_TOKEN = "4F0DC05CFA1450BB02E390B00135B7A0"
EXCLUDED_IDS = ["6996-1", "6996-3", "6996-4"]

# === FUNCTION TO EXPORT FILTERED DATA ===
def pull_data() -> pd.DataFrame:
    payload = {
        'token': API_TOKEN,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'true',
        'returnFormat': 'json'
    }

    print("🔄 Requesting ALL data from REDCap...")
    response = requests.post(API_URL, data=payload)
    response.raise_for_status()

    df = pd.DataFrame.from_records(response.json())
    print(f"📦 Retrieved {len(df)} rows from REDCap.")

    # Identify enrolled IDs only from the intake event
    enrolled_ids = df[
        (df["redcap_event_name"] == "intake_survey_arm_1") &
        (df["ptp_enrolled"] == "Enrolled")
    ]["record_id"].unique().tolist()

    print(f"✅ Found {len(enrolled_ids)} enrolled participants.")

    # Filter and exclude known bad records
    df = df[df["record_id"].isin(enrolled_ids)]
    df = df[~df["record_id"].isin(EXCLUDED_IDS)]

    return df.reset_index(drop=True)

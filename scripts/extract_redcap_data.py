# scripts/extract_redcap_data.py
import pandas as pd
import requests
import io

API_TOKEN = "2E5ADE0C72485930E7C9F11325638F74"  # Your REDCap API token
API_URL = "https://redcap.miami.edu/api/"

def pull_data() -> pd.DataFrame:
    print("🔄 Pulling data from REDCap...")

    payload = {
        "token": API_TOKEN,
        "content": "record",
        "format": "csv",
        "type": "flat",
        "rawOrLabel": "raw",
        "rawOrLabelHeaders": "raw",
        "exportCheckboxLabel": "false",
        "exportSurveyFields": "true",
        "exportDataAccessGroups": "false",
        "returnFormat": "json"
    }

    response = requests.post(API_URL, data=payload)
    if response.status_code != 200:
        raise Exception(f"REDCap API request failed: {response.status_code} - {response.text}")

    df = pd.read_csv(io.StringIO(response.text), dtype=str)
    print("🔍 REDCap columns:", df.columns.tolist())
    return df
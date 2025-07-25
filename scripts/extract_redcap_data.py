import requests
import pandas as pd
import os

# === CONFIGURATION ===
API_URL = "https://redcap.miami.edu/api/"
API_TOKEN = "4F0DC05CFA1450BB02E390B00135B7A0"
EXPORT_FILE_NAME = "redcap_export.csv"
OUTPUT_FOLDER = "files"

# === FUNCTION TO EXPORT FULL DATA ===
def export_redcap_data(api_url, token):
    payload = {
        'token': token,
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'returnFormat': 'json'
    }

    print("\nRequesting ALL data from REDCap...")
    response = requests.post(api_url, data=payload)
    response.raise_for_status()

    records = response.json()
    df = pd.DataFrame.from_records(records)
    print(f"Retrieved {len(df)} rows from REDCap.")
    return df

# === MAIN ===
def main():
    try:
        df = export_redcap_data(API_URL, API_TOKEN)

        # Identify enrolled record_ids from intake event only
        enrolled_ids = df[
            (df["redcap_event_name"] == "intake_survey_arm_1") &
            (df["ptp_enrolled"] == "Enrolled")
        ]["record_id"].unique().tolist()

        print(f"Found {len(enrolled_ids)} enrolled participants.")

        # Filter full dataset by those record_ids
        filtered_df = df[df["record_id"].isin(enrolled_ids)]

        # Exclude specific mis-enrolled records
        excluded_ids = ["6996-1", "6996-3", "6996-4"]
        filtered_df = filtered_df[~filtered_df["record_id"].isin(excluded_ids)]

        # Save filtered output
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        output_path = os.path.join(OUTPUT_FOLDER, EXPORT_FILE_NAME)
        filtered_df.to_csv(output_path, index=False)
        print(f"\n✅ Filtered enrolled data saved to: {output_path}")

    except requests.RequestException as e:
        print(f"❌ Failed to connect to REDCap: {e}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# === ENTRY POINT ===
if __name__ == "__main__":
    main()

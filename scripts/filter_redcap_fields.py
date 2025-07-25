# scripts/filter_redcap_fields.py
import pandas as pd
import os

INPUT_FILE = "files/redcap_survey_data.csv"  # This is your original raw export
OUTPUT_FILE = "files/redcap_filtered.csv"    # Your cleaned output to be used by the next script

def apply_filter(df: pd.DataFrame) -> pd.DataFrame:
    # Example: keep only participants where ptp_enrolled = 'Enrolled'
    if 'ptp_enrolled' in df.columns:
        df = df[df['ptp_enrolled'] == 'Enrolled']
    return df.reset_index(drop=True)

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"❌ File not found: {INPUT_FILE}")
        exit(1)

    print(f"📂 Loading data from: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, dtype=str)
    df_filtered = apply_filter(df)

    print(f"💾 Saving filtered data to: {OUTPUT_FILE}")
    df_filtered.to_csv(OUTPUT_FILE, index=False)

import pandas as pd
import os

INPUT_FILE = "files/redcap_survey_data.csv"
OUTPUT_FILE = "files/redcap_survey_data.csv"  # overwrite the same file

def get_valid_date(prompt_text):
    while True:
        user_input = input(prompt_text).strip()
        if not user_input:
            return None
        try:
            return pd.to_datetime(user_input, format="%Y-%m-%d")
        except ValueError:
            print("❌ Invalid format. Use YYYY-MM-DD.")

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ File not found: {INPUT_FILE}")
        return

    print("Enter optional start and end date to filter records by admin_5 (ICF date).")
    print("Press Enter to skip either or both.")

    start_date = get_valid_date("Start date (YYYY-MM-DD): ")
    end_date = get_valid_date("End date (YYYY-MM-DD): ")
    
    # === After user inputs are collected ===
    with open("files/contextual_dates.txt", "w") as f:
        f.write(f"{start_date},{end_date}")

    
    if not start_date and not end_date:
        print("No filtering applied. Keeping all records.")
        return

    df = pd.read_csv(INPUT_FILE, dtype=str)

    if "admin_5" not in df.columns:
        print("❌ Column 'admin_5' not found.")
        return

    df["admin_5_parsed"] = pd.to_datetime(df["admin_5"], errors="coerce")

    if start_date:
        df = df[df["admin_5_parsed"] >= start_date]
    if end_date:
        df = df[df["admin_5_parsed"] <= end_date]

    df = df.drop(columns=["admin_5_parsed"])
    print(f"✅ Remaining rows after filtering: {len(df)}")

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Filtered dataset saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

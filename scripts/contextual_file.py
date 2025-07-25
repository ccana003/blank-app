import pandas as pd
import os
from datetime import datetime

# === Load dynamic date range from filter_by_admin5_date.py ===
try:
    with open("files/contextual_dates.txt") as f:
        date_line = f.read().strip()
        start_raw, end_raw = date_line.split(",")

        # Format as M/D/YYYY (e.g., 3/31/2025)
        START_DATE = datetime.strptime(start_raw, "%Y-%m-%d").strftime("%-m/%-d/%Y")
        END_DATE = datetime.strptime(end_raw, "%Y-%m-%d").strftime("%-m/%-d/%Y")
except Exception:
    START_DATE = "3/31/2025"
    END_DATE = "6/30/2025"


# === File paths ===
INPUT_FILE = "files/redcap_survey_data.csv"
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_FILE = f"files/contextual_file.csv"


# === Ensure output folder exists ===
os.makedirs("files", exist_ok=True)

# === Load REDCap export ===
df = pd.read_csv(INPUT_FILE, dtype=str)
print("✅ Loaded data:", df.shape)

df["admin_2"] = df["admin_2"].str.extract(r'(\d+)').astype(str)
df["admin_4"] = df["admin_4"].astype(str)


# === Helper function to build contextual row ===
def build_row(admin_2_value, wave_value):
    subset = df[(df["admin_2"] == admin_2_value) & (df["admin_4"] == wave_value)]
    count = len(subset)

    method_code = 1 if admin_2_value == "11" else 1 if admin_2_value == "12" else -9

    return {
        "admin_1": "CRT_FL",
        "admin_2": admin_2_value,
        "admin_4": wave_value,
        "c1": 3,
        "c1_os": -1,
        "c2": 2,
        "c3": 0,
        "c4": count,
        "c5_1": 0,
        "c5_2": method_code,
        "c5_3": 0,
        "c5_4": 0,
        "c5_5": method_code,
        "c5_6": 0,
        "c5_6_os": -1,
        "c6": 1,
        "c7_1": 0,
        "c7_2": 1,
        "c7_3": 0,
        "c7_4": 0,
        "c7_4_os": -1,
        "c8": 30,
        "c9": 30,
        "c10": START_DATE,
        "c11": END_DATE,
        "c12": 2
    }

# === Build contextual summary for all (cohort, wave) combinations ===
rows = []
for cohort in ["11", "12"]:
    for wave in ["1", "2"]:
        rows.append(build_row(cohort, wave))


# === Column order for export ===
columns = [
    "admin_1", "admin_2", "admin_4", "c1", "c1_os", "c2", "c3", "c4",
    "c5_1", "c5_2", "c5_3", "c5_4", "c5_5", "c5_6", "c5_6_os", "c6",
    "c7_1", "c7_2", "c7_3", "c7_4", "c7_4_os", "c8", "c9", "c10", "c11", "c12"
]

# === Save output ===
df_out = pd.DataFrame(rows, columns=columns)
df_out.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Contextual summary saved to {OUTPUT_FILE}")

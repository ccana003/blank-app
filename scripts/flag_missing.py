import pandas as pd
import os

# === CONFIGURATION ===
INPUT_FILE = "files/redcap_merged_baseline_only.csv"
OUTPUT_FILE = "files/redcap_survey_data.csv"

# Columns to check
question_cols = [
    "q1a", "q1b", "q1c", "q1d", "q1e", "q1f", "q2",
    "q3a", "q3b", "q3c", "q3d", "q3e", "q3f", "q3g", "q3h", "q3i", "q3j", "q3k",
    "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14a",
    "q15", "q16", "q17", "q18", "q19", "q20",
    "q21_1", "q21_2", "q21_3", "q21_4", "q21_5", "q21_6", "q21_7", "q21_8",
    "q23", "q24a", "q24b", "q24c", "q25a", "q25b", "age_dv", "q26", "q26a", "q26b",
    "q27",
    "q29_1", "q29_2", "q29_3", "q29_4", "q29_5", "q29_6", "q29_7", "q29_8",
    "q30_1", "q30_2", "q30_3", "q30_4", "q30_5", "q30_6", "q30_6_os",
    "q31_1", "q31_2", "q31_3", "q31_4", "q31_5", "q31_6", "q31_7", "q31_8", "q31_9",
    "q31_10", "q31_11", "q31_12", "q31_13", "q31_14", "q31_15", "q31_16", "q31_17",
    "q31_18", "q31_19", "q31_20", "q31_21", "q31_22", "q31_22_os",
    "q32_1", "q32_2", "q32_3", "q32_4", "q32_5", "q32_6", "q32_7", "q32_8",
    "q32_9", "q32_10", "q32_11", "q32_12", "q32_13", "q32_13_os",
    "q33_1", "q33_2", "q33_3", "q33_4", "q33_5", "q33_6", "q33_7", "q33_8",
    "q33_9", "q33_10", "q33_10_os",
    "q34_1", "q34_2", "q34_3", "q34_4", "q34_5", "q34_6", "q34_7", "q34_7_os",
    "q35_1", "q35_2", "q35_3", "q35_4", "q35_5", "q35_6", "q35_7", "q35_8",
    "q35_9", "q35_10", "q35_11", "q35_12", "q35_13", "q35_13_os",
    "q36_1", "q36_2", "q36_3", "q36_4", "q36_5", "q36_6", "q36_7", "q36_7_os",
    "q37", "q38a", "q38b", "q39", "q40", "q41", "q42"
]


# === LOAD DATA ===
print("Loading file...")
df = pd.read_csv(INPUT_FILE)

# === APPLY RULE ===
for col in question_cols:
    if col in df.columns:
        df[col] = df.apply(
            lambda row: -9 if pd.notna(row["admin_5"]) and pd.isna(row[col]) else
                        -2 if pd.isna(row["admin_5"]) and pd.isna(row[col]) else
                        row[col],
            axis=1
        )
        
        
# === Unified Rule: q19_os and q23_os handling ===

# --- Handle q19_os ---
if "q19" in df.columns and "q19_os" in df.columns:
    df["q19_os"] = df.apply(
        lambda row: "-9" if row["q19"] == 3 and (pd.isna(row["q19_os"]) or str(row["q19_os"]).strip() == "")
        else "-1" if row["q19"] != 3
        else row["q19_os"],
        axis=1
    )

# --- Handle q23_os ---
if "q23" in df.columns and "q23_os" in df.columns:
    df["q23_os"] = df.apply(
        lambda row: "-9" if row["q23"] == 10 and (pd.isna(row["q23_os"]) or str(row["q23_os"]).strip() == "")
        else "-1" if row["q23"] != 10
        else row["q23_os"],
        axis=1
    )

# === RULE: Set q24b_os based on q24b ===
if "q24b" in df.columns and "q24b_os" in df.columns:
    df["q24b_os"] = df.apply(
        lambda row: "-9" if row["q24b"] == 99999 and (pd.isna(row["q24b_os"]) or str(row["q24b_os"]).strip() == "")
        else "-1" if row["q24b"] != 99999
        else row["q24b_os"],
        axis=1
    )

# === RULE: Set q26a based on q26 ===
if "q26" in df.columns and "q26a" in df.columns:
    df["q26a"] = df.apply(
        lambda row: "-9" if row["q26"] == 1 and (pd.isna(row["q26a"]) or str(row["q26a"]).strip() == "")
        else "-1" if row["q26"] != 1
        else row["q26a"],
        axis=1
    )

# === RULE: Set q26b and q26b_os based on q26 and q26b ===
if "q26" in df.columns and "q26b" in df.columns:
    # Fill q26b if missing and q26 == 3
    df["q26b"] = df.apply(
        lambda row: "-9" if row["q26"] == 3 and (pd.isna(row["q26b"]) or str(row["q26b"]).strip() == "")
        else row["q26b"],
        axis=1
    )

if "q26b" in df.columns and "q26b_os" in df.columns:
    df["q26b_os"] = df.apply(
        lambda row: "-9" if row["q26"] == 3 and str(row["q26b"]).strip() == "999" and (pd.isna(row["q26b_os"]) or str(row["q26b_os"]).strip() == "")
        else "-1" if pd.notna(row["q26b"]) and (pd.isna(row["q26b_os"]) or str(row["q26b_os"]).strip() == "")
        else row["q26b_os"],
        axis=1
    )

# === RULE: Set q26b and q26b_os based on q26 ===
if "q26" in df.columns and "q26b" in df.columns:
    df["q26b"] = df.apply(
        lambda row: "-9" if row["q26"] == 3 and (pd.isna(row["q26b"]) or str(row["q26b"]).strip() == "")
        else "-1" if row["q26"] == 1 and str(row["q26"]).strip() not in ["-1", "-2", "-9"]
        else row["q26b"],
        axis=1
    )

if "q26b" in df.columns and "q26b_os" in df.columns:
    df["q26b_os"] = df.apply(
        lambda row: "-9" if row["q26"] == 3 and str(row["q26b"]).strip() == "999" and (pd.isna(row["q26b_os"]) or str(row["q26b_os"]).strip() == "")
        else "-1" if (
            (row["q26"] == 1 and str(row["q26"]).strip() not in ["-1", "-2", "-9"]) or
            (pd.notna(row["q26b"]) and (pd.isna(row["q26b_os"]) or str(row["q26b_os"]).strip() == ""))
        )
        else row["q26b_os"],
        axis=1
    )

# === RULE: Set q39_sp based on q39 ===
if "q39" in df.columns and "q39_sp" in df.columns:
    df["q39_sp"] = df.apply(
        lambda row: "-9" if row["q39"] == 1 and (pd.isna(row["q39_sp"]) or str(row["q39_sp"]).strip() == "")
        else "-1" if row["q39"] != 1 and (pd.isna(row["q39_sp"]) or str(row["q39_sp"]).strip() == "")
        else row["q39_sp"],
        axis=1
    )


# === SAVE RESULT ===
os.makedirs("files", exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Missing values flagged and saved to: {OUTPUT_FILE}")

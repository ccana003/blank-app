import pandas as pd
import os

# === CONFIGURATION ===
INPUT_FILE = "files/redcap_filtered.csv"
OUTPUT_FILE = "files/redcap_transformed.csv"

# === LOAD DATA ===
print("Loading filtered REDCap data...")
df = pd.read_csv(INPUT_FILE)

def handle_multiselect_with_os(df, base_q, os_index):
    raw_prefix = f"{base_q}___"
    clean_prefix = f"{base_q}_"
    os_field = f"{base_q}_{os_index}"
    os_text_field = f"{os_field}_os"

    # Rename columns: qXX___N → qXX_N
    df.rename(columns={col: col.replace(raw_prefix, clean_prefix)
                       for col in df.columns if col.startswith(raw_prefix)}, inplace=True)

    # Apply OS logic if applicable
    if os_field in df.columns and os_text_field in df.columns:
        df.loc[df[os_field] == 0, os_text_field] = -1
        df.loc[(df[os_field] == 1) & (
            df[os_text_field].isna() |
            (df[os_text_field].astype(str).str.strip() == "")
        ), os_text_field] = -9

    return df


# === RULE 1: Add cs4_siteID column as second column ===
df.insert(loc=1, column="admin_1", value="CRT_FL")

# === RULE 2: Add cs4_cohortID column based on randomization field ===
def build_cohort_id(randomization_value):
    if str(randomization_value).strip().upper() == "A":
        return "11"
    elif str(randomization_value).strip().upper() == "B":
        return "12"
    else:
        return pd.NA

df.insert(loc=2, column="admin_2", value=df["randomization"].apply(build_cohort_id))

# === RULE 3: Rename record_id to cs4_subjectID ===
if "record_id" in df.columns:
    df.rename(columns={"record_id": "admin_3"}, inplace=True)

# === RULE 4: Rename and recode redcap_event_name to cs4_wave_num, placed as 4th column ===
def map_wave(event_name):
    val = str(event_name).strip().lower()
    if val in ["screening_survey_arm_1", "intake_survey_arm_1"]:
        return 1
    elif val == "exit_survey_arm_1":
        return 2
    return pd.NA

if "redcap_event_name" in df.columns:
    wave_values = df["redcap_event_name"].apply(map_wave)
    df.drop(columns=["redcap_event_name"], inplace=True)
    df.insert(loc=3, column="admin_4", value=wave_values)

# === RULE 4.5: Rename icf_date to admin_5 and place as 5th column ===
if "icf_date" in df.columns:
    icf_values = df["icf_date"]
    df.drop(columns=["icf_date"], inplace=True)
    df.insert(loc=4, column="admin_5", value=icf_values)


# === RULE 5: Recode ptp_language to cs4_survey_lang and insert as 5th column ===
def recode_language(val):
    if pd.isna(val):
        return pd.NA
    if val == 1:
        return "4"
    elif val == 2:
        return "7"
    return pd.NA

if "ptp_language" in df.columns:
    lang_values = df["ptp_language"].apply(recode_language)
    df.drop(columns=["ptp_language"], inplace=True)
    df.insert(loc=4, column="admin_6", value=lang_values)

# === RULE 6: Add cs4_Survey_Lang_Oth_Specify as 6th column filled with -1 ===
df.insert(loc=5, column="admin_6_os", value=-1)

# === RULE 7: Drop randomization column ===
if "randomization" in df.columns:
    df.drop(columns=["randomization"], inplace=True)
    
# === RULE XX: Set values in q5 based on q4 logic ===
if "q4" in df.columns and "q5" in df.columns:
    # Normalize q4 to numeric, just in case it's read as string
    df["q4"] = pd.to_numeric(df["q4"], errors="coerce")

    # Identify rows where q5 is blank
    q5_blank = df["q5"].isna() | (df["q5"].astype(str).str.strip() == "")

    # Apply rule: q4 = 1 or 2 → q5 = -9
    df.loc[q5_blank & df["q4"].isin([1, 2]), "q5"] = -9

    # Apply rule: q4 = 3 → q5 = -1
    df.loc[q5_blank & (df["q4"] == 3), "q5"] = -1

# === RULE XX: Set values in q7 based on q6 logic ===
if "q6" in df.columns and "q7" in df.columns:
    df["q6"] = pd.to_numeric(df["q6"], errors="coerce")
    
    q7_blank = df["q7"].isna() | (df["q7"].astype(str).str.strip() == "")

    # Apply both in a single .loc to avoid overwrite
    df.loc[q7_blank, "q7"] = df.loc[q7_blank, "q6"].map({
        0: -1,
        1: -9, 2: -9, 3: -9, 4: -9, 5: -9, 6: -9, 7: -9
    }).fillna(df.loc[q7_blank, "q7"])  # Leave q7 unchanged for all other q6 values





# === RULE 8: Rename q14b___X to q14b_X for all such columns ===
df.rename(columns={col: col.replace("q14b___", "q14b_") for col in df.columns if col.startswith("q14b___")}, inplace=True)

# === RULE XX: Recode q14b_X = 0 to -1 when q14a is 1 or 2 ===
q14b_fields = [f"q14b_{i}" for i in range(1, 7)]

if "q14a" in df.columns and all(col in df.columns for col in q14b_fields):
    df["q14a"] = pd.to_numeric(df["q14a"], errors="coerce")

    condition = df["q14a"].isin([1, 2])

    for col in q14b_fields:
        mask = condition & (df[col] == 0)
        df.loc[mask, col] = -1



# === RULE 9: Set values in q14b_6_os based on q14b_6 conditions ===
if "q14b_6" in df.columns and "q14b_6_os" in df.columns:
    # Ensure q14b_6 is numeric just in case
    df["q14b_6"] = pd.to_numeric(df["q14b_6"], errors="coerce")

    # If q14b_6 == 0 → q14b_6_os = -1
    df.loc[df["q14b_6"] == 0, "q14b_6_os"] = -1

    # If q14b_6 == 1 and q14b_6_os is blank → q14b_6_os = -9
    df.loc[(df["q14b_6"] == 1) & (df["q14b_6_os"].isna() | df["q14b_6_os"].astype(str).str.strip() == ""), "q14b_6_os"] = -9

    # If q14b_6 == -1 → q14b_6_os = -1
    df.loc[df["q14b_6"] == -1, "q14b_6_os"] = -1

# === RULE 10: Merge q17 and q17_uf into one column called q17 ===
if "q17" in df.columns and "q17_uf" in df.columns:
    df["q17"] = df["q17"].combine_first(df["q17_uf"])
    df.drop(columns=["q17_uf"], inplace=True)

# === RULE 11: Rename q21___X to q21_X for all such columns ===
df.rename(columns={col: col.replace("q21___", "q21_") for col in df.columns if col.startswith("q21___")}, inplace=True)

# === RULE 12: Merge q22 and q22_fiu into one column called q22 ===
if "q22" in df.columns and "q22_fiu" in df.columns:
    df["q22"] = df["q22"].combine_first(df["q22_fiu"])
    df.drop(columns=["q22_fiu"], inplace=True)

# === RULE: Handle multiselect renaming and _os logic in bulk ===
for q_base, os_idx in [
    ("q29", 8),
    ("q30", 6),
    ("q31", 22),
    ("q32", 13),
    ("q33", 10),
    ("q34", 7),
    ("q35", 13),
    ("q36", 7),
]:
    df = handle_multiselect_with_os(df, q_base, os_idx)

# === RULE 18: Format admin_3 to be 8 digits total: '12' + 6-digit padded ID ===
if "admin_3" in df.columns:
    df["admin_3"] = (
        df["admin_3"]
        .astype(str)
        .str.replace("-", "", regex=False)
        .str.zfill(6)  # pad to 6 digits
        .apply(lambda x: f"12{x}")  # prepend '12'
    )
    
# === RULE XX: Set values in q28_os based on q28 logic ===
if "q28" in df.columns and "q28_os" in df.columns:
    df.loc[df["q28"].isin([1, 2, 3, 4]), "q28_os"] = -1
    df.loc[(df["q28"] == 5) & (df["q28_os"].isna() | (df["q28_os"].astype(str).str.strip() == "")), "q28_os"] = -9


# === RULE XX: Set values in q30_* based on q29_1 ===
q30_fields = [f"q30_{i}" for i in range(1, 7)] + ["q30_6_os"]

if "q29_1" in df.columns and all(col in df.columns for col in q30_fields):
    df["q29_1"] = pd.to_numeric(df["q29_1"], errors="coerce")

    for col in q30_fields:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

            # First, fill -1 where value is 0 (but not blank)
            mask_zero = (df["q29_1"] == 1) & (df[col] == 0)
            df.loc[mask_zero, col] = -1

            # Then, fill -9 only where value is truly blank (NaN or empty string)
            mask_blank = (df["q29_1"] == 1) & (df[col].isna() | df[col].astype(str).str.strip() == "")
            df.loc[mask_blank, col] = -9



# === FINAL COLUMN ORDER ADJUSTMENT: Move admin_* columns to front in proper order ===
admin_columns = ["admin_1", "admin_2", "admin_3", "admin_4", "admin_5", "admin_6", "admin_6_os"]
remaining_columns = [col for col in df.columns if col not in admin_columns]
df = df[admin_columns + remaining_columns]



# === SAVE TRANSFORMED FILE ===
df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Transformed data saved to: {OUTPUT_FILE}")

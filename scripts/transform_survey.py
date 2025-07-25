# scripts/transform_survey.py
import pandas as pd

OUTPUT_FILE = "files/redcap_transformed.csv"

def handle_multiselect_with_os(df, base_q, os_index):
    raw_prefix = f"{base_q}___"
    clean_prefix = f"{base_q}_"
    os_field = f"{base_q}_{os_index}"
    os_text_field = f"{os_field}_os"

    df.rename(columns={col: col.replace(raw_prefix, clean_prefix)
                       for col in df.columns if col.startswith(raw_prefix)}, inplace=True)

    if os_field in df.columns and os_text_field in df.columns:
        df.loc[df[os_field] == 0, os_text_field] = -1
        df.loc[(df[os_field] == 1) & (
            df[os_text_field].isna() |
            (df[os_text_field].astype(str).str.strip() == "")
        ), os_text_field] = -9

    return df

def apply(df: pd.DataFrame) -> pd.DataFrame:
    df.insert(loc=1, column="admin_1", value="CRT_FL")

    def build_cohort_id(val):
        val = str(val).strip().upper()
        return "11" if val == "A" else "12" if val == "B" else pd.NA

    df.insert(loc=2, column="admin_2", value=df["randomization"].apply(build_cohort_id))

    if "record_id" in df.columns:
        df.rename(columns={"record_id": "admin_3"}, inplace=True)

    def map_wave(val):
        val = str(val).strip().lower()
        return 1 if val in ["screening_survey_arm_1", "intake_survey_arm_1"] else 2 if val == "exit_survey_arm_1" else pd.NA

    if "redcap_event_name" in df.columns:
        df.insert(loc=3, column="admin_4", value=df["redcap_event_name"].apply(map_wave))
        df.drop(columns=["redcap_event_name"], inplace=True)

    if "icf_date" in df.columns:
        df.insert(loc=4, column="admin_5", value=df["icf_date"])
        df.drop(columns=["icf_date"], inplace=True)

    def recode_language(val):
        if pd.isna(val): return pd.NA
        return "4" if val == 1 else "7" if val == 2 else pd.NA

    if "ptp_language" in df.columns:
        df.insert(loc=4, column="admin_6", value=df["ptp_language"].apply(recode_language))
        df.drop(columns=["ptp_language"], inplace=True)

    df.insert(loc=5, column="admin_6_os", value=-1)

    if "randomization" in df.columns:
        df.drop(columns=["randomization"], inplace=True)

    if "q4" in df.columns and "q5" in df.columns:
        df["q4"] = pd.to_numeric(df["q4"], errors="coerce")
        q5_blank = df["q5"].isna() | (df["q5"].astype(str).str.strip() == "")
        df.loc[q5_blank & df["q4"].isin([1, 2]), "q5"] = -9
        df.loc[q5_blank & (df["q4"] == 3), "q5"] = -1

    if "q6" in df.columns and "q7" in df.columns:
        df["q6"] = pd.to_numeric(df["q6"], errors="coerce")
        q7_blank = df["q7"].isna() | (df["q7"].astype(str).str.strip() == "")
        df.loc[q7_blank, "q7"] = df.loc[q7_blank, "q6"].map({0: -1, 1: -9, 2: -9, 3: -9, 4: -9, 5: -9, 6: -9, 7: -9})

    df.rename(columns={col: col.replace("q14b___", "q14b_") for col in df.columns if col.startswith("q14b___")}, inplace=True)
    q14b_fields = [f"q14b_{i}" for i in range(1, 7)]

    if "q14a" in df.columns and all(col in df.columns for col in q14b_fields):
        df["q14a"] = pd.to_numeric(df["q14a"], errors="coerce")
        for col in q14b_fields:
            df.loc[(df["q14a"] == 2) & (df[col] == 0), col] = -1

    if "q14b_6" in df.columns and "q14b_6_os" in df.columns:
        df["q14b_6"] = pd.to_numeric(df["q14b_6"], errors="coerce")
        df.loc[df["q14b_6"] == 0, "q14b_6_os"] = -1
        df.loc[(df["q14b_6"] == 1) & (df["q14b_6_os"].isna() | (df["q14b_6_os"].astype(str).str.strip() == "")), "q14b_6_os"] = -9
        df.loc[df["q14b_6"] == -1, "q14b_6_os"] = -1

    if "q17" in df.columns and "q17_uf" in df.columns:
        df["q17"] = df["q17"].combine_first(df["q17_uf"])
        df.drop(columns=["q17_uf"], inplace=True)

    df.rename(columns={col: col.replace("q21___", "q21_") for col in df.columns if col.startswith("q21___")}, inplace=True)

    if "q22" in df.columns and "q22_fiu" in df.columns:
        df["q22"] = df["q22"].combine_first(df["q22_fiu"])
        df.drop(columns=["q22_fiu"], inplace=True)

    for q_base, os_idx in [
        ("q29", 8), ("q30", 6), ("q31", 22), ("q32", 13), ("q33", 10), ("q34", 7), ("q35", 13), ("q36", 7)
    ]:
        df = handle_multiselect_with_os(df, q_base, os_idx)

    if "admin_3" in df.columns:
        df["admin_3"] = df["admin_3"].astype(str).str.replace("-", "", regex=False).str.zfill(6).apply(lambda x: f"12{x}")

    if "q28" in df.columns and "q28_os" in df.columns:
        df.loc[df["q28"].isin([1, 2, 3, 4]), "q28_os"] = -1
        df.loc[(df["q28"] == 5) & (df["q28_os"].isna() | (df["q28_os"].astype(str).str.strip() == "")), "q28_os"] = -9

    def apply_exclusive_logic(df, control_col, target_cols):
        if control_col in df.columns and all(col in df.columns for col in target_cols):
            df[control_col] = pd.to_numeric(df[control_col], errors="coerce")
            df.loc[df[control_col] == 0, target_cols] = -1
            none_selected = (df[target_cols] == 1).any(axis=1) == False
            df.loc[(df[control_col] == 1) & none_selected, target_cols] = -9
        return df

    control_target_pairs = {
        "q29_1": [f"q30_{i}" for i in range(1, 7)],
        "q29_2": [f"q31_{i}" for i in range(1, 23)],
        "q29_3": [f"q32_{i}" for i in range(1, 14)],
        "q29_4": [f"q33_{i}" for i in range(1, 11)],
        "q29_5": [f"q34_{i}" for i in range(1, 8)],
        "q29_6": [f"q35_{i}" for i in range(1, 14)],
        "q29_7": [f"q36_{i}" for i in range(1, 8)],
    }

    for control_col, target_cols in control_target_pairs.items():
        df = apply_exclusive_logic(df, control_col, target_cols)

    admin_cols = [f"admin_{i}" for i in range(1, 7)] + ["admin_6_os"]
    other_cols = [col for col in df.columns if col not in admin_cols]
    df = df[admin_cols + other_cols]

    return df.reset_index(drop=True)

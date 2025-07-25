# scripts/select_variables.py
import pandas as pd

# === REQUIRED FIELDS ===
required_fields = [
    "record_id", "redcap_event_name", "randomization", "icf_date", "ptp_language",
    "q1a", "q1b", "q1c", "q1d", "q1e", "q1f", "q2",
    "q3a", "q3b", "q3c", "q3d", "q3e", "q3f", "q3g", "q3h", "q3i", "q3j", "q3k",
    "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14a",
    "q14b___1", "q14b___2", "q14b___3", "q14b___4", "q14b___5", "q14b___6", "q14b_6_os",
    "q15", "q16", "q17", "q17_uf", "q18", "q19", "q19_os", "q20",
    "q21___1", "q21___2", "q21___3", "q21___4", "q21___5", "q21___6", "q21___7", "q21___8",
    "q22", "q22_fiu", "q23", "q23_os", "q24a", "q24b", "q24b_os", "q24c",
    "q25a", "q25b", "age_dv", "q26", "q26a", "q26b", "q26b_os", "q27", 
    "q29___1", "q29___2", "q29___3", "q29___4", "q29___5", "q29___6", "q29___7", "q29___8", "q29_8_os", 
    "q30___1", "q30___2", "q30___3", "q30___4", "q30___5", "q30___6", "q30_6_os",
    "q31___1", "q31___2", "q31___3", "q31___4", "q31___5", "q31___6", "q31___7", "q31___8", "q31___9",
    "q31___10", "q31___11", "q31___12", "q31___13", "q31___14", "q31___15", "q31___16", "q31___17",
    "q31___18", "q31___19", "q31___20", "q31___21", "q31___22", "q31_22_os",
    "q32___1", "q32___2", "q32___3", "q32___4", "q32___5", "q32___6", "q32___7", "q32___8", "q32___9",
    "q32___10", "q32___11", "q32___12", "q32___13", "q32_13_os",
    "q33___1", "q33___2", "q33___3", "q33___4", "q33___5", "q33___6", "q33___7", "q33___8", "q33___9",
    "q33___10", "q33_10_os",
    "q34___1", "q34___2", "q34___3", "q34___4", "q34___5", "q34___6", "q34___7", "q34_7_os",
    "q35___1", "q35___2", "q35___3", "q35___4", "q35___5", "q35___6", "q35___7", "q35___8", "q35___9",
    "q35___10", "q35___11", "q35___12", "q35___13", "q35_13_os",
    "q36___1", "q36___2", "q36___3", "q36___4", "q36___5", "q36___6", "q36___7", "q36_7_os",
    "q37", "q38a", "q38b", "q39", "q39_sp", "q40", "q41", "q42"
]

def apply(df: pd.DataFrame) -> pd.DataFrame:
    print("🔎 Filtering REDCap data to required fields...")
    existing_fields = [col for col in required_fields if col in df.columns]
    missing_fields = [col for col in required_fields if col not in df.columns]

    if missing_fields:
        print("⚠️ WARNING: The following expected fields were not found in the data and will be skipped:")
        for field in missing_fields:
            print(f"  - {field}")

    filtered_df = df[existing_fields]
    print(f"✅ Columns retained: {len(existing_fields)}")
    print(f"❌ Columns dropped: {len(df.columns) - len(existing_fields)}")
    return filtered_df.reset_index(drop=True)

if __name__ == "__main__":
    from scripts.filter_redcap_fields import apply  # or just `import select_variables` if needed
    INPUT_FILE = "files/redcap_enrolled.csv"
    OUTPUT_FILE = "files/redcap_selected.csv"

    df = pd.read_csv(INPUT_FILE, dtype=str)
    df = apply(df)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Selected variables saved to: {OUTPUT_FILE}")

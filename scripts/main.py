# scripts/main.py
import subprocess

steps = [
    "extract_redcap_data.py",        # outputs: redcap_survey_data.csv
    "filter_redcap_fields.py",       # inputs: redcap_survey_data.csv → outputs: redcap_filtered.csv
    "apply_special_rules.py",        # inputs: redcap_filtered.csv → outputs: redcap_transformed.csv
    "merge_baseline.py",             # inputs: redcap_transformed.csv → outputs: redcap_merged_baseline_only.csv
    "flag_missing.py",               # inputs: redcap_merged_baseline_only.csv → outputs: redcap_survey_data.csv
    "filter_by_admin5_date.py",      # filters: redcap_survey_data.csv (same file)
    "contextual_file.py",            # uses: redcap_survey_data.csv → outputs: contextual_file.csv
    "change_to_pipe.py",             # uses: redcap_survey_data.csv + contextual_file.csv → outputs: final pipe-delimited files
    "zip_output.py"                  # zips them
]

print("🚀 Running pipeline...")

for script in steps:
    print(f"\n▶️ Running: {script}")
    subprocess.run(["python", f"scripts/{script}"], check=True)

print("\n✅ Pipeline completed.")

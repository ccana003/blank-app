# scripts/main.py
import subprocess

steps = [
    "extract_redcap_data.py",
    "filter_enrolled.py",
    "select_variables.py",
    "transform_survey.py",
    "merge_baseline.py",
    "flag_missing.py",
    "filter_by_admin5_date.py",
    "contextual_file.py",
    "change_to_pipe.py",
    "zip_output.py"
]

print("🚀 Running pipeline...")

for script in steps:
    print(f"\n▶️ Running: {script}")
    subprocess.run(["python", f"scripts/{script}"], check=True)

print("\n✅ Pipeline completed.")

if __name__ == "__main__":
    import os

    INPUT_FILE = "files/redcap_merged_baseline_only.csv"
    OUTPUT_FILE = "files/redcap_survey_data.csv"

    df = pd.read_csv(INPUT_FILE, dtype=str)
    df = apply(df)
    os.makedirs("files", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Cleaned file saved to: {OUTPUT_FILE}")

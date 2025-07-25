# scripts/main.py
import subprocess

steps = [
    "extract_redcap_data.py",
    "filter_redcap_fields.py",
    "apply_special_rules.py",
    "merge_baseline.py",
    "flag_missing.py",
    "filter_by_admin5_date.py",
    "contextual_file.py",
    "change_to_pipe.py"
]

print("🚀 Running pipeline...")

for script in steps:
    print(f"\n▶️ Running: {script}")
    subprocess.run(["python", f"scripts/{script}"], check=True)

print("\n✅ Pipeline completed.")

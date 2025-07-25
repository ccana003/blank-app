# scripts/main.py
import subprocess

steps = [
    "extract_redcap_data.py",
    "filter_redcap_fields.py",       # ✅ Matches uploaded file
    "apply_special_rules.py",        # ✅ Matches uploaded file
    "merge_baseline.py",             # ✅ Matches uploaded file
    "flag_missing.py",               # ✅ Matches uploaded file
    "filter_by_admin5_date.py",      # ✅ Matches uploaded file
    "contextual_file.py",            # ✅ Matches uploaded file
    "change_to_pipe.py"              # ✅ Matches uploaded file
    # "zip_output.py" — Not included because you didn’t upload it
]

print("🚀 Running pipeline...")

for script in steps:
    print(f"\n▶️ Running: {script}")
    subprocess.run(["python", f"scripts/{script}"], check=True)

print("\n✅ Pipeline completed.")

import pandas as pd
import numpy as np
import os

# === CONFIGURATION ===
INPUT_FILE = "files/redcap_transformed.csv"
OUTPUT_FILE = "files/redcap_merged_baseline_only.csv"

# === LOAD TRANSFORMED DATA ===
print("Loading transformed REDCap data...")
df = pd.read_csv(INPUT_FILE)

# === SPLIT ===
# Keep all follow-up rows (admin_4 == 2, etc.)
non_baseline = df[df["admin_4"] != 1]

# Keep all baseline rows
baseline_rows = df[df["admin_4"] == 1]

# Merge baseline rows by admin_3 only if duplicates exist
def smart_merge(group):
    return group.ffill().bfill().iloc[0]

# Check for duplicated admin_3 values in baseline
duplicates = baseline_rows["admin_3"][baseline_rows["admin_3"].duplicated()].unique()
merged_baseline = (
    baseline_rows.groupby("admin_3", as_index=False)
    .apply(lambda g: smart_merge(g) if g["admin_3"].iloc[0] in duplicates else g.iloc[0])
)

# Flatten index if groupby-apply created a MultiIndex
if isinstance(merged_baseline.index, pd.MultiIndex):
    merged_baseline.reset_index(drop=True, inplace=True)

# Combine everything
df_final = pd.concat([non_baseline, merged_baseline], ignore_index=True)

# === SAVE RESULT ===
os.makedirs("files", exist_ok=True)
df_final.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Merged baseline rows saved to: {OUTPUT_FILE}")

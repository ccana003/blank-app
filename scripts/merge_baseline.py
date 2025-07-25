import pandas as pd
import numpy as np
import os

# === PANDAS FUTURE BEHAVIOR SETTING ===
pd.set_option("future.no_silent_downcasting", True)

# === CONFIGURATION ===
INPUT_FILE = "files/redcap_transformed.csv"
OUTPUT_FILE = "files/redcap_merged_baseline_only.csv"
LOG_FILE = "files/merged_duplicates_log.txt"

# === LOAD TRANSFORMED DATA ===
print("Loading transformed REDCap data...")
df = pd.read_csv(INPUT_FILE)

# === SPLIT DATA BY WAVE ===
non_baseline = df[df["admin_4"] != 1]
baseline_rows = df[df["admin_4"] == 1]

# === SMART MERGE FOR DUPLICATE BASELINE ROWS ===
def smart_merge(group):
    return group.ffill().bfill().infer_objects(copy=False).iloc[0]

# === IDENTIFY DUPLICATES ===
duplicates = baseline_rows["admin_3"][baseline_rows["admin_3"].duplicated()].unique()
duplicates = sorted(duplicates)  # Sorted for readability

# === WRITE LOG FILE ===
os.makedirs("files", exist_ok=True)
with open(LOG_FILE, "w") as log:
    log.write(f"Total duplicated admin_3 IDs found: {len(duplicates)}\n")
    if duplicates:
        log.write("Duplicated admin_3 values:\n")
        for val in duplicates:
            count = (baseline_rows["admin_3"] == val).sum()
            log.write(f"  {val} -> {count} rows\n")
    else:
        log.write("No duplicated admin_3 values found.\n")
print(f"📝 Duplicate merge log saved to: {LOG_FILE}")

# === MERGE DUPLICATES (EXCLUDING GROUPING COLUMN FROM DATA) ===
merged_baseline = (
    baseline_rows.drop(columns=["admin_3"])
    .groupby(baseline_rows["admin_3"], group_keys=False)
    .apply(lambda g: smart_merge(g) if g.name in duplicates else g.iloc[0])
    .reset_index()
)

print(f"📦 Merged {merged_baseline.shape[0]} baseline records (duplicates resolved and singletons preserved).")

# === COMBINE BASELINE AND NON-BASELINE ROWS ===
df_final = pd.concat([non_baseline, merged_baseline], ignore_index=True)

# === SAVE TO FILE ===
df_final.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Merged baseline rows saved to: {OUTPUT_FILE}")

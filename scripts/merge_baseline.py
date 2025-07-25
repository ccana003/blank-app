# scripts/merge_baseline.py
import pandas as pd

LOG_FILE = "files/merged_duplicates_log.txt"

pd.set_option("future.no_silent_downcasting", True)

def smart_merge(group):
    return group.ffill().bfill().infer_objects(copy=False).iloc[0]

def apply(df: pd.DataFrame) -> pd.DataFrame:
    non_baseline = df[df["admin_4"] != 1]
    baseline_rows = df[df["admin_4"] == 1]

    duplicates = baseline_rows["admin_3"][baseline_rows["admin_3"].duplicated()].unique()
    duplicates = sorted(duplicates)

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

    merged_baseline = (
        baseline_rows.drop(columns=["admin_3"])
        .groupby(baseline_rows["admin_3"], group_keys=False)
        .apply(lambda g: smart_merge(g) if g.name in duplicates else g.iloc[0])
        .reset_index()
    )

    print(f"📦 Merged {merged_baseline.shape[0]} baseline records (duplicates resolved and singletons preserved).")

    return pd.concat([non_baseline, merged_baseline], ignore_index=True)

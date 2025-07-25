import pandas as pd

def build(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    print("🧱 Building contextual file...")
    counts = df["randomization"].map({"A": "11", "B": "12"}).value_counts().to_dict()
    rows = []

    for cohort_id, count in counts.items():
        rows.append({
            "admin_1": "CRT_FL",
            "admin_2": cohort_id,
            "admin_3": count,
            "admin_4": f"{start}|{end}",
            "admin_5": start,
            "admin_6": "Mixed",
            "admin_6_os": "",
        })

    return pd.DataFrame(rows)

import pandas as pd

def apply(df: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    print(f"📅 Filtering by ICF date between {start} and {end}...")
    df["admin_5"] = pd.to_datetime(df["admin_5"])
    return df[(df["admin_5"] >= start) & (df["admin_5"] <= end)].reset_index(drop=True)

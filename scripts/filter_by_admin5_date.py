
# scripts/filter_by_admin5_date.py
import pandas as pd

def apply(df: pd.DataFrame, start_date=None, end_date=None) -> pd.DataFrame:
    if "admin_5" not in df.columns:
        raise KeyError("admin_5 column not found in data")

    df["admin_5_parsed"] = pd.to_datetime(df["admin_5"], errors="coerce")

    if start_date:
        df = df[df["admin_5_parsed"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["admin_5_parsed"] <= pd.to_datetime(end_date)]

    return df.drop(columns=["admin_5_parsed"]).reset_index(drop=True)

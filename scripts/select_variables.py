import pandas as pd

def apply(df: pd.DataFrame) -> pd.DataFrame:
    print("🔎 Selecting only relevant fields...")
    needed_cols = ["record_id", "randomization", "admin_5", "q1a"]
    return df[needed_cols]

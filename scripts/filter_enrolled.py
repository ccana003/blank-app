import pandas as pd

def apply(df: pd.DataFrame) -> pd.DataFrame:
    print("✅ Filtering to enrolled participants...")
    return df[df["ptp_enrolled"] == "Enrolled"].reset_index(drop=True)

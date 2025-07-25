import pandas as pd

def apply(df: pd.DataFrame) -> pd.DataFrame:
    print("🔄 Transforming survey data...")
    df = df.copy()

    def convert_record_id(row):
        prefix = "11" if row["randomization"] == "A" else "12"
        return f"{prefix}{row['record_id']}"

    df["record_id"] = df.apply(convert_record_id, axis=1)
    return df.rename(columns={"q1a": "CS4_Sat_Standard_of_Living"})

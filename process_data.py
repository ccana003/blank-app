import pandas as pd

def process_csv(df: pd.DataFrame, selected_date) -> pd.DataFrame:
    # Sample logic: add date column and sum of numeric columns
    df["RunDate"] = selected_date
    df["Sum"] = df.select_dtypes(include="number").sum(axis=1)
    return df

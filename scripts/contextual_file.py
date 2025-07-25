# scripts/contextual_file.py
import pandas as pd
import os
from datetime import datetime

# === Load dynamic date range from filter_by_admin5_date.py ===
def load_contextual_dates(default_start="3/31/2025", default_end="6/30/2025"):
    try:
        with open("files/contextual_dates.txt") as f:
            date_line = f.read().strip()
            start_raw, end_raw = date_line.split(",")
            start_date = datetime.strptime(start_raw, "%Y-%m-%d").strftime("%-m/%-d/%Y")
            end_date = datetime.strptime(end_raw, "%Y-%m-%d").strftime("%-m/%-d/%Y")
            return start_date, end_date
    except Exception:
        return default_start, default_end


def build_contextual_summary(df: pd.DataFrame) -> pd.DataFrame:
    START_DATE, END_DATE = load_contextual_dates()
    df["admin_2"] = df["admin_2"].str.extract(r'(\d+)').astype(str)
    df["admin_4"] = df["admin_4"].astype(str)

    def build_row(admin_2_value, wave_value):
        subset = df[(df["admin_2"] == admin_2_value) & (df["admin_4"] == wave_value)]
        count = len(subset)
        method_code = 1 if admin_2_value in ["11", "12"] else -9

        return {
            "admin_1": "CRT_FL",
            "admin_2": admin_2_value,
            "admin_4": wave_value,
            "c1": 3,
            "c1_os": -1,
            "c2": 2,
            "c3": 0,
            "c4": count,
            "c5_1": 0,
            "c5_2": method_code,
            "c5_3": 0,
            "c5_4": 0,
            "c5_5": method_code,
            "c5_6": 0,
            "c5_6_os": -1,
            "c6": 1,
            "c7_1": 0,
            "c7_2": 1,
            "c7_3": 0,
            "c7_4": 0,
            "c7_4_os": -1,
            "c8": 30,
            "c9": 30,
            "c10": START_DATE,
            "c11": END_DATE,
            "c12": 2
        }

    rows = [build_row(cohort, wave) for cohort in ["11", "12"] for wave in ["1", "2"]]

    columns = [
        "admin_1", "admin_2", "admin_4", "c1", "c1_os", "c2", "c3", "c4",
        "c5_1", "c5_2", "c5_3", "c5_4", "c5_5", "c5_6", "c5_6_os", "c6",
        "c7_1", "c7_2", "c7_3", "c7_4", "c7_4_os", "c8", "c9", "c10", "c11", "c12"
    ]

    return pd.DataFrame(rows, columns=columns)

# scripts/change_to_pipe.py
import pandas as pd
from datetime import datetime

SITE_ID = "CRT_FL"
INPUT_FOLDER = "files"
SURVEY_INPUT = f"{INPUT_FOLDER}/redcap_survey_data.csv"
CONTEXT_INPUT = f"{INPUT_FOLDER}/contextual_file.csv"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
SURVEY_OUTPUT = f"{INPUT_FOLDER}/CS4_{SITE_ID}_Survey_Data_{timestamp}.csv"
CONTEXT_OUTPUT = f"{INPUT_FOLDER}/CS4_{SITE_ID}_Contextual_{timestamp}.csv"

MULTICODE_COLUMNS = {"c5_2", "c5_5"}

def clean_value(val, colname=None):
    if pd.isna(val):
        return ""
    try:
        val_str = str(val).strip()
        if colname == "admin_5":
            try:
                parsed = pd.to_datetime(val_str)
                return parsed.strftime("%m/%d/%Y")
            except:
                pass
        if isinstance(val, float) and val.is_integer():
            return str(int(val))
        if "." in val_str:
            val_float = float(val_str)
            if val_float.is_integer():
                return str(int(val_float))
    except:
        pass
    return val_str.replace('|', '').replace('\n', ' ').replace('\r', ' ')

def clean_contextual_value(val, colname=None):
    val = clean_value(val, colname)
    if colname in MULTICODE_COLUMNS and val.isdigit() and len(val) > 1:
        val = ",".join(val)
    return val

def clean_dataframe(df: pd.DataFrame, is_contextual=False) -> pd.DataFrame:
    if is_contextual:
        return df.apply(lambda col: col.map(lambda val: clean_contextual_value(val, col.name)), axis=0)
    else:
        return df.apply(lambda col: col.map(lambda val: clean_value(val, col.name)), axis=0)

def export_pipe_delimited(df: pd.DataFrame, output_path: str):
    df.to_csv(
        output_path,
        sep='|',
        index=False,
        encoding='utf-8',
        lineterminator='\n',
        quoting=0
    )
    print(f"✅ Saved: {output_path}")

def run_conversion():
    print(f"📂 Reading: {SURVEY_INPUT}")
    survey_df = pd.read_csv(SURVEY_INPUT, dtype=str)
    cleaned_survey_df = clean_dataframe(survey_df, is_contextual=False)
    export_pipe_delimited(cleaned_survey_df, SURVEY_OUTPUT)

    print(f"📂 Reading: {CONTEXT_INPUT}")
    context_df = pd.read_csv(CONTEXT_INPUT, dtype=str)
    cleaned_context_df = clean_dataframe(context_df, is_contextual=True)
    export_pipe_delimited(cleaned_context_df, CONTEXT_OUTPUT)

if __name__ == "__main__":
    run_conversion()

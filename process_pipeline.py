# process_pipeline.py
import os
import pandas as pd
from scripts import (
    extract_redcap,
    filter_enrolled,
    transform_contextual,
    transform_survey_data,
    generate_zip_output
)

def run_pipeline(uploaded_csv_path: str, start_date: str, end_date: str) -> str:
    """
    Main pipeline to process CS4 REDCap data and generate ZIP output.
    Args:
        uploaded_csv_path: Path to raw REDCap data (CSV).
        start_date: Start of data collection window (YYYY-MM-DD).
        end_date: End of data collection window (YYYY-MM-DD).
    Returns:
        Path to generated ZIP file ready for submission.
    """
    # === Load Raw Data ===
    df_raw = pd.read_csv(uploaded_csv_path)

    # === Step 1: Filter enrolled participants ===
    df_enrolled = filter_enrolled.apply_filter(df_raw)

    # === Step 2: Generate contextual file ===
    contextual_df = transform_contextual.build_contextual(df_enrolled, start_date, end_date)

    # === Step 3: Generate cleaned survey data file ===
    survey_df = transform_survey_data.clean_survey_data(df_enrolled)

    # === Step 4: Save both files ===
    os.makedirs("files", exist_ok=True)
    contextual_path = os.path.join("files", "CS4_Site01_Contextual_20250725_120000.csv")
    survey_path = os.path.join("files", "CS4_Site01_Survey_Data_20250725_120000.csv")

    contextual_df.to_csv(contextual_path, sep="|", index=False, encoding="utf-8")
    survey_df.to_csv(survey_path, sep="|", index=False, encoding="utf-8")

    # === Step 5: Zip both files for submission ===
    zip_path = generate_zip_output.create_zip(
    ["files/contextual.csv", "files/survey_data.csv"],
    "files"
)


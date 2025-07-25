import os
from scripts import (
    apply_special_rules,
    extract_redcap_data,
    filter_by_admin5_date,
    filter_enrolled,
    filter_redcap_fields,
    contextual_file,
    zip_output
)

def run_pipeline(start_date: str, end_date: str) -> str:
    df = extract_redcap_data.pull_data()
    df = filter_enrolled.apply(df)
    df = filter_by_admin5_date.apply(df, start_date, end_date)
    df = filter_redcap_fields.apply(df)

    contextual_df = contextual_file.build(df, start_date, end_date)
    survey_df = apply_special_rules.apply(df)

    os.makedirs("files", exist_ok=True)
    contextual_path = "files/contextual.csv"
    survey_path = "files/survey_data.csv"

    contextual_df.to_csv(contextual_path, sep="|", index=False)
    survey_df.to_csv(survey_path, sep="|", index=False)

    return zip_output.create_zip([contextual_path, survey_path], "files")

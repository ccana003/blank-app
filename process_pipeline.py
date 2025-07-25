import os
from scripts import (
    extract_redcap_data,
    filter_enrolled,
    filter_by_date,
    select_variables,
    contextual_file,
    transform_survey,
    zip_output
)

def run_pipeline(start_date: str, end_date: str) -> str:
    df = extract_redcap_data.pull_data()
    df = filter_enrolled.apply(df)
    df = filter_by_date.apply(df, start_date, end_date)
    df = select_variables.apply(df)

    contextual_df = contextual_file.build(df, start_date, end_date)
    survey_df = transform_survey.apply(df)

    os.makedirs("files", exist_ok=True)
    contextual_path = "files/contextual.csv"
    survey_path = "files/survey_data.csv"

    contextual_df.to_csv(contextual_path, sep="|", index=False)
    survey_df.to_csv(survey_path, sep="|", index=False)

    return zip_output.create_zip([contextual_path, survey_path], "files")

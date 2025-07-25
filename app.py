import streamlit as st
import datetime
from process_pipeline import run_pipeline

st.title("CEAL CS4 Submission Builder")

start_date = st.date_input("Start Date", value=datetime.date(2025, 4, 1))
end_date = st.date_input("End Date", value=datetime.date.today())

if st.button("Run Submission Process"):
    with st.spinner("Processing..."):
        zip_path = run_pipeline(start_date.isoformat(), end_date.isoformat())

    st.success("Done!")
    with open(zip_path, "rb") as f:
        st.download_button("Download ZIP", f, file_name="CS4_submission.zip")

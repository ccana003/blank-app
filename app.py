import tempfile
import streamlit as st
import datetime
from process_pipeline import run_pipeline

st.title("CEAL CS4 Data Processor")

uploaded_file = st.file_uploader("Upload REDCap CSV", type="csv")
start_date = st.date_input("Start Date", value=datetime.date(2025, 4, 1))
end_date = st.date_input("End Date")

if uploaded_file and st.button("Process and Generate Zip"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

    with st.spinner("Processing..."):
        zip_path = run_pipeline(tmp_path, start_date.isoformat(), end_date.isoformat())

    st.success("Done!")
    with open(zip_path, "rb") as f:
        st.download_button("Download ZIP", f, file_name="CS4_submission.zip")

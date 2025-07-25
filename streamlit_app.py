import streamlit as st
import pandas as pd
import os
from datetime import date
from process_data import process_csv  # We'll create this file next

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

st.title("📅 CSV Processor Demo")

# --- User Inputs ---
selected_date = st.date_input("Select a date", value=date.today())
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

# --- Action ---
if st.button("Run Script"):
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("✅ Uploaded Data Preview:", df.head())

        # Process CSV
        output_df = process_csv(df, selected_date)

        # Save output
        output_path = f"output/processed_{selected_date}.csv"
        output_df.to_csv(output_path, index=False)

        st.success(f"Done! File saved to `{output_path}`")
        st.dataframe(output_df)
    else:
        st.warning("Please upload a CSV file first.")

import streamlit as st
import pandas as pd

import upload_data_page          # <-- your upload page
import scrap_analysis_page
import quality_reports_page

st.set_page_config(page_title="Digital Scrap & Quality Tracker", layout="wide")

# ---- Navigation ----
page = st.sidebar.radio(
    "Navigate",
    ["Upload Data", "Scrap Analysis", "Quality Reports"]
)

# ---- Page selection ----
if page == "Upload Data":
    upload_data_page.show_upload_data_page()

elif page == "Scrap Analysis":
    scrap_analysis_page.show_scrap_analysis_page()

elif page == "Quality Reports":
    quality_reports_page.show_quality_reports_page()

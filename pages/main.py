import streamlit as st
import scrap_analysis_page, quality_reports_page
import pandas as pd

st.set_page_config(page_title="Digital Scrap & Quality Tracker", layout="wide")

# --- File upload (shared for all pages) ---
if "df" not in st.session_state:
    st.session_state.df = None

uploaded_file = st.sidebar.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    st.session_state.df = pd.read_csv(uploaded_file)
    st.sidebar.success("File uploaded!")

# --- Navigation ---
page = st.sidebar.radio("Navigate", ["Scrap Analysis", "Quality Reports"])

# --- Run selected page ---
if page == "Scrap Analysis":
    scrap_analysis_page.show_scrap_analysis_page()
elif page == "Quality Reports":
    quality_reports_page.show_quality_reports_page()

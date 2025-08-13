import streamlit as st
from pages import upload_data, scrap_analysis, quality_reports

st.set_page_config(page_title="Digital Scrap & Quality Tracker", layout="wide")

# Sidebar navigation
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Upload Data", "Scrap Analysis", "Quality Reports"])

# Home page
if page == "Home":
    st.title("🧵 Digital Scrap & Quality Tracker")
    st.markdown(
        """
        Welcome! Use the sidebar to navigate between pages:
        - **Upload Data**: Upload your scrap CSV file
        - **Scrap Analysis**: Explore scrap trends and defects
        - **Quality Reports**: Analyze scrap cost, machines, and defects
        """
    )

# Upload Data page
elif page == "Upload Data":
    upload_data.show_upload_page()

# Scrap Analysis page
elif page == "Scrap Analysis":
    scrap_analysis.show_scrap_analysis_page()

# Quality Reports page
elif page == "Quality Reports":
    quality_reports.show_quality_reports_page()

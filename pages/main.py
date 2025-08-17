import streamlit as st
import pandas as pd

import upload_data_page          # <-- your upload page
import scrap_analysis_page
import quality_reports_page
import home_page

st.set_page_config(page_title="Digital Scrap & Quality Tracker", layout="wide")

# ---- Navigation ----
page = st.sidebar.radio(
    "Navigate",
    ["Home","Upload Data", "Scrap Analysis", "Quality Reports"]
)

if page =="Home":
    st.title("🧵 Digital Scrap & Quality Tracker")
    st.markdown(
    """
Welcome to the **Digital Scrap & Quality Tracker** prototype for Lear Corporation —  
an internal dashboard designed to help you understand and reduce textile scrap.

Use the navigation menu on the left to explore the app:

- 📂 **Upload Data** – upload your production / scrap CSV file.
- 📊 **Scrap Analysis** – analyse scrap quantity, trends, top contributors, and machines.
- 🧵 **Quality Reports** – explore defect types and shift-related scrap issues.

---

### 🔧 How to Get Started

1. Go to **Upload Data** and upload your dataset (CSV format)  
2. Choose the **columns you want to include** (optional)  
3. Navigate to **Scrap Analysis** or **Quality Reports** to explore the insights

---

### 📌 Tip

Use the filters (Date, Machine, Defect Type, Fabric, Shift) in each page  
to focus on a specific time period or contributor group.

---


"""
)

# ---- Page selection ----
if page == "Upload Data":
    upload_data_page.show_upload_data_page()

elif page == "Scrap Analysis":
    scrap_analysis_page.show_scrap_analysis_page()

elif page == "Quality Reports":
    quality_reports_page.show_quality_reports_page()

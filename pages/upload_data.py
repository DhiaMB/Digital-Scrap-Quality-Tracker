import streamlit as st
import pandas as pd

def show_upload_page():
    st.title("📂 Upload Data")

    uploaded_file = st.file_uploader("Upload scrap data CSV", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df  # persist data across pages
        st.success("✅ Data uploaded successfully!")
        st.dataframe(df.head(10))
    elif "df" in st.session_state:
        st.info("Data already uploaded. Go to another page to analyze.")

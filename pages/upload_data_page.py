import streamlit as st
import pandas as pd
import os

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def show_upload_data_page():
    st.title("📂 Upload Data")

    # --- File uploader ---
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    file_to_load = None

    if uploaded_file:
        # Save the uploaded file locally
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File saved locally: {uploaded_file.name}")
        file_to_load = file_path

    # --- Previously uploaded files ---
    st.sidebar.subheader("📄 Previously Uploaded Files")
    uploaded_files = os.listdir(UPLOAD_DIR)
    if uploaded_files:
        selected_file = st.sidebar.selectbox("Select a file to load", uploaded_files)
        if selected_file:
            file_to_load = os.path.join(UPLOAD_DIR, selected_file)

    # --- Load and display only once ---
    if file_to_load:
        st.session_state.df = pd.read_csv(file_to_load)
        st.subheader(f"📊 Loaded Data: {os.path.basename(file_to_load)}")
        st.dataframe(st.session_state.df)
    else:
        st.info("Upload a CSV file to get started.")

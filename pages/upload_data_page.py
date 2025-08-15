import streamlit as st
import pandas as pd

def show_upload_data_page():
    st.title("📂 Upload Data & Select Columns")

    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df.copy()  # Save in session state to use in other pages

        st.success("File uploaded successfully!")

        # --- Column Selection ---
        st.subheader("Select Columns to Display")
        if "selected_columns" not in st.session_state:
            # Default: all columns selected
            st.session_state.selected_columns = df.columns.tolist()

        selected_columns = st.multiselect(
            "Choose columns to display",
            options=df.columns.tolist(),
            default=st.session_state.selected_columns
        )
        st.session_state.selected_columns = selected_columns  # Save choice

        # Show filtered DataFrame
        st.subheader(f"Preview of Selected Columns ({len(df)} rows)")
        st.dataframe(df[selected_columns])
    else:
        st.info("Please upload a CSV file to get started.")

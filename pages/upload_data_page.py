import streamlit as st
import pandas as pd

def main():
    st.title("📂 Upload Data")

    uploaded_file = st.file_uploader("Upload your CSV file", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df  # store in session state
        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())

if __name__ == "__main__":
    main()

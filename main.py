import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Digital Scrap & Quality Tracker", layout="wide")

st.title("🧵 Digital Scrap & Quality Tracker (Textile Industry)")

# File uploader
uploaded_file = st.file_uploader("Upload scrap data CSV", type="csv")

# Load data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Display raw data
    st.subheader("📄 Raw Data")
    st.dataframe(df)

    # KPIs
    total_scrap = df["Quantity_Scrapped_meters"].sum()
    total_cost = df["Scrap_Cost"].sum()
    top_defect = df["Defect_Type"].mode()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scrap (m)", f"{total_scrap}")
    col2.metric("Total Scrap Cost", f"${total_cost:,.2f}")
    col3.metric("Most Common Defect", top_defect)

    # Scrap trend over time
    df["Date"] = pd.to_datetime(df["Date"])
    scrap_trend = df.groupby("Date")["Quantity_Scrapped_meters"].sum().reset_index()
    fig1 = px.line(scrap_trend, x="Date", y="Quantity_Scrapped_meters", title="Scrap Trend Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    # Scrap by defect type
    defect_chart = df.groupby("Defect_Type")["Quantity_Scrapped_meters"].sum().reset_index()
    fig2 = px.bar(defect_chart, x="Defect_Type", y="Quantity_Scrapped_meters", title="Scrap by Defect Type")
    st.plotly_chart(fig2, use_container_width=True)

    # Scrap cost by fabric type
    fabric_chart = df.groupby("Fabric_Type")["Scrap_Cost"].sum().reset_index()
    fig3 = px.bar(fabric_chart, x="Fabric_Type", y="Scrap_Cost", title="Scrap Cost by Fabric", color="Fabric_Type")
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Please upload your textile scrap dataset to get started.")

st.markdown("---")
st.caption("Prototype version 1.0 | © 2025 Digital Scrap & Quality Tracker")

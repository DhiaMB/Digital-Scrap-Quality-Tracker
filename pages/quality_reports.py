import streamlit as st
import pandas as pd
import plotly.express as px

def show_quality_reports_page():
    st.title("📋 Quality Reports")
    
    if "df" not in st.session_state or st.session_state.df is None:
        st.info("📂 Please upload a file first on the Upload Data page.")
        return
    
    df = st.session_state.df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    st.sidebar.header("🔧 Filters")

    if "qr_selected_date" not in st.session_state:
        st.session_state.qr_selected_date = (df["Date"].min(), df["Date"].max())
    if "qr_selected_machines" not in st.session_state:
        st.session_state.qr_selected_machines = df["Machine_ID"].unique().tolist()
    if "qr_selected_defects" not in st.session_state:
        st.session_state.qr_selected_defects = df["Defect_Type"].unique().tolist()
    if "qr_selected_fabric" not in st.session_state:
        st.session_state.qr_selected_fabric = df["Fabric_Type"].unique().tolist()

    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.qr_selected_date = (df["Date"].min(), df["Date"].max())
        st.session_state.qr_selected_machines = df["Machine_ID"].unique().tolist()
        st.session_state.qr_selected_defects = df["Defect_Type"].unique().tolist()
        st.session_state.qr_selected_fabric = df["Fabric_Type"].unique().tolist()

    selected_date = st.sidebar.date_input("Select Date Range", key="qr_selected_date")
    selected_machines = st.sidebar.multiselect("Select Machines", df["Machine_ID"].unique(), key="qr_selected_machines")
    selected_defects = st.sidebar.multiselect("Select Defect Types", df["Defect_Type"].unique(), key="qr_selected_defects")
    selected_fabric = st.sidebar.multiselect("Select Fabric Types", df["Fabric_Type"].unique(), key="qr_selected_fabric")

    df_filtered = df[
        (df["Date"] >= pd.to_datetime(selected_date[0])) &
        (df["Date"] <= pd.to_datetime(selected_date[1])) &
        (df["Machine_ID"].isin(selected_machines)) &
        (df["Defect_Type"].isin(selected_defects)) &
        (df["Fabric_Type"].isin(selected_fabric))
    ]

    st.subheader(f"Filtered Data ({len(df_filtered)} rows)")
    st.dataframe(df_filtered)

    # Charts
    fabric_fig = px.bar(
        df_filtered.groupby("Fabric_Type", as_index=False)["Scrap_Cost"].sum(),
        x="Fabric_Type", y="Scrap_Cost", color="Fabric_Type", text="Scrap_Cost"
    )
    st.plotly_chart(fabric_fig, use_container_width=True)

    machine_fig = px.bar(
        df_filtered.groupby("Machine_ID", as_index=False)["Quantity_Scrapped_meters"].sum(),
        x="Machine_ID", y="Quantity_Scrapped_meters", color="Machine_ID", text="Quantity_Scrapped_meters"
    )
    st.plotly_chart(machine_fig, use_container_width=True)

    top_defects = df_filtered["Defect_Type"].value_counts().reset_index()
    top_defects.columns = ["Defect_Type", "Count"]
    defect_fig = px.bar(top_defects, x="Defect_Type", y="Count", color="Defect_Type", text="Count")
    st.plotly_chart(defect_fig, use_container_width=True)

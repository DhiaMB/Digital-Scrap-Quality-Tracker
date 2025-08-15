import streamlit as st
import pandas as pd

def sidebar_filters(df):
    # --- Sidebar Filters ---
    st.sidebar.header("🔧 Filters")

    # Initialize session state only if keys do not exist
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = (df["Date"].min(), df["Date"].max())
    if "selected_machines" not in st.session_state:
        st.session_state.selected_machines = df["Machine_ID"].unique().tolist()
    if "selected_defects" not in st.session_state:
        st.session_state.selected_defects = df["Defect_Type"].unique().tolist()
    if "selected_fabric" not in st.session_state:
        st.session_state.selected_fabric = df["Fabric_Type"].unique().tolist()

    # Reset button
    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.selected_date = (df["Date"].min(), df["Date"].max())
        st.session_state.selected_machines = df["Machine_ID"].unique().tolist()
        st.session_state.selected_defects = df["Defect_Type"].unique().tolist()
        st.session_state.selected_fabric = df["Fabric_Type"].unique().tolist()

    # Widgets synced with session state
    selected_date = st.sidebar.date_input(
        "Select Date Range",
        value=st.session_state.selected_date,
        key="selected_date"
    )
    selected_machines = st.sidebar.multiselect(
        "Select Machines",
        options=df["Machine_ID"].unique(),
        default=st.session_state.selected_machines,
        key="selected_machines"
    )
    selected_defects = st.sidebar.multiselect(
        "Select Defect Types",
        options=df["Defect_Type"].unique(),
        default=st.session_state.selected_defects,
        key="selected_defects"
    )
    selected_fabric = st.sidebar.multiselect(
        "Select Fabric Types",
        options=df["Fabric_Type"].unique(),
        default=st.session_state.selected_fabric,
        key="selected_fabric"
    )

    # Filter the dataframe
    df_filtered = df[
        (df["Date"] >= pd.to_datetime(selected_date[0])) &
        (df["Date"] <= pd.to_datetime(selected_date[1])) &
        (df["Machine_ID"].isin(selected_machines)) &
        (df["Defect_Type"].isin(selected_defects)) &
        (df["Fabric_Type"].isin(selected_fabric))
    ]
    return selected_date, selected_machines, selected_defects, selected_fabric
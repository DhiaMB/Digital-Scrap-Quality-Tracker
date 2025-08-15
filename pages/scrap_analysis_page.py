import streamlit as st
import pandas as pd
import plotly.express as px

def show_scrap_analysis_page():
    st.title("📊 Scrap Analysis")

    # Use the shared uploaded file
    if "df" not in st.session_state or st.session_state.df is None:
        st.info("📂 Please upload a file first in the sidebar.")
        return

    df = st.session_state.df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Filters
    st.sidebar.header("🔧 Filters")
    if "sa_selected_date" not in st.session_state:
        st.session_state.sa_selected_date = (df["Date"].min(), df["Date"].max())
    if "sa_selected_machines" not in st.session_state:
        st.session_state.sa_selected_machines = df["Machine_ID"].unique().tolist()
    if "sa_selected_defects" not in st.session_state:
        st.session_state.sa_selected_defects = df["Defect_Type"].unique().tolist()

    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.sa_selected_date = (df["Date"].min(), df["Date"].max())
        st.session_state.sa_selected_machines = df["Machine_ID"].unique().tolist()
        st.session_state.sa_selected_defects = df["Defect_Type"].unique().tolist()

    selected_date = st.sidebar.date_input("Select Date Range", key="sa_selected_date")
    selected_machines = st.sidebar.multiselect(
        "Select Machines", df["Machine_ID"].unique(), key="sa_selected_machines"
    )
    selected_defects = st.sidebar.multiselect(
        "Select Defect Types", df["Defect_Type"].unique(), key="sa_selected_defects"
    )

    # Filter dataframe
    df_filtered = df[
        (df["Date"] >= pd.to_datetime(selected_date[0])) &
        (df["Date"] <= pd.to_datetime(selected_date[1])) &
        (df["Machine_ID"].isin(selected_machines)) &
        (df["Defect_Type"].isin(selected_defects))
    ]

    # --- KPIs and Charts (same as your current layout) ---
    total_scrap = df_filtered["Quantity_Scrapped_meters"].sum()
    top_defect = df_filtered["Defect_Type"].mode()[0] if not df_filtered.empty else "-"
    machines = df_filtered["Machine_ID"].nunique()

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Scrap (m)", total_scrap)
    c2.metric("Most Frequent Defect", top_defect)
    c3.metric("Machines Involved", machines)

    st.subheader("Scrap Trend Over Time")
    trend_fig = px.line(
        df_filtered.groupby("Date", as_index=False)["Quantity_Scrapped_meters"].sum(),
        x="Date",
        y="Quantity_Scrapped_meters",
        markers=True
    )
    st.plotly_chart(trend_fig, use_container_width=True)

    st.subheader("Scrap by Defect Type")
    defect_fig = px.bar(
        df_filtered.groupby("Defect_Type", as_index=False)["Quantity_Scrapped_meters"].sum(),
        x="Defect_Type", y="Quantity_Scrapped_meters", color="Defect_Type", text="Quantity_Scrapped_meters"
    )
    st.plotly_chart(defect_fig, use_container_width=True)

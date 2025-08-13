import streamlit as st
import pandas as pd
import plotly.express as px

def show_scrap_analysis_page():
    st.title("📊 Scrap Analysis")
    
    if "df" not in st.session_state or st.session_state.df is None:
        st.info("📂 Please upload a file first on the Upload Data page.")
        return
    
    df = st.session_state.df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        # KPIs
    total_scrap = df["Quantity_Scrapped_meters"].sum()
    total_cost = df["Scrap_Cost"].sum()
    top_defect = df["Defect_Type"].mode()[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scrap (m)", f"{total_scrap}")
    col2.metric("Total Scrap Cost", f"${total_cost:,.2f}")
    col3.metric("Most Common Defect", top_defect)

    # Sidebar filters and session_state handling (same as before)
    st.sidebar.header("🔧 Filters")
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = (df["Date"].min(), df["Date"].max())
    if "selected_machines" not in st.session_state:
        st.session_state.selected_machines = df["Machine_ID"].unique().tolist()
    if "selected_defects" not in st.session_state:
        st.session_state.selected_defects = df["Defect_Type"].unique().tolist()

    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.selected_date = (df["Date"].min(), df["Date"].max())
        st.session_state.selected_machines = df["Machine_ID"].unique().tolist()
        st.session_state.selected_defects = df["Defect_Type"].unique().tolist()

    selected_date = st.sidebar.date_input("Select Date Range", key="selected_date")
    selected_machines = st.sidebar.multiselect("Select Machines", df["Machine_ID"].unique(), key="selected_machines")
    selected_defects = st.sidebar.multiselect("Select Defect Types", df["Defect_Type"].unique(), key="selected_defects")

    df_filtered = df[
        (df["Date"] >= pd.to_datetime(selected_date[0])) &
        (df["Date"] <= pd.to_datetime(selected_date[1])) &
        (df["Machine_ID"].isin(selected_machines)) &
        (df["Defect_Type"].isin(selected_defects))
    ]

    st.subheader(f"Filtered Data ({len(df_filtered)} rows)")
    st.dataframe(df_filtered)

    # Charts
    defect_fig = px.bar(
        df_filtered.groupby("Defect_Type", as_index=False)["Quantity_Scrapped_meters"].sum(),
        x="Defect_Type", y="Quantity_Scrapped_meters", color="Defect_Type", text="Quantity_Scrapped_meters"
    )
    st.plotly_chart(defect_fig, use_container_width=True)

    trend_fig = px.line(
        df_filtered.groupby("Date", as_index=False)["Quantity_Scrapped_meters"].sum(),
        x="Date", y="Quantity_Scrapped_meters", markers=True
    )
    st.plotly_chart(trend_fig, use_container_width=True)

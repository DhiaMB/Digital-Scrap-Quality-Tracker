import streamlit as st
import pandas as pd
import plotly.express as px
import io

def show_quality_reports_page():
    st.title("📋 Quality Reports")

    if "df" not in st.session_state or st.session_state.df is None:
        st.info("📂 Please upload a file first in the sidebar.")
        return

    df = st.session_state.df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Filters
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
    selected_defects  = st.sidebar.multiselect("Select Defect Types", df["Defect_Type"].unique(), key="qr_selected_defects")
    selected_fabric   = st.sidebar.multiselect("Select Fabric Types", df["Fabric_Type"].unique(), key="qr_selected_fabric")

    df_filtered = df[
        (df["Date"] >= pd.to_datetime(selected_date[0])) &
        (df["Date"] <= pd.to_datetime(selected_date[1])) &
        (df["Machine_ID"].isin(selected_machines)) &
        (df["Defect_Type"].isin(selected_defects)) &
        (df["Fabric_Type"].isin(selected_fabric))
    ]

    # Tabs and Charts (keep your layout)
    tab_kpi, tab_trend, tab_breakdown = st.tabs(["📊 KPIs", "📈 Trend/Cost", "🧵 Breakdown"])

    with tab_kpi:
        st.subheader("Key Performance Indicators")
        total_scrap = df_filtered["Quantity_Scrapped_meters"].sum()
        total_cost  = df_filtered["Scrap_Cost"].sum()
        top_defect  = df_filtered["Defect_Type"].mode()[0] if not df_filtered.empty else "-"
        machine_count = df_filtered["Machine_ID"].nunique()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Scrap (m)", total_scrap)
        c2.metric("Total Scrap Cost", f"${total_cost:,.2f}")
        c3.metric("Most Frequent Defect", top_defect)

    with tab_trend:
        st.subheader("Scrap Trend Over Time")
        trend_fig = px.line(
            df_filtered.groupby("Date", as_index=False)["Quantity_Scrapped_meters"].sum(),
            x="Date", y="Quantity_Scrapped_meters", markers=True
        )
        st.plotly_chart(trend_fig, use_container_width=True)

        st.subheader("Scrap Cost by Fabric")
        cost_fig = px.bar(
            df_filtered.groupby("Fabric_Type", as_index=False)["Scrap_Cost"].sum(),
            x="Fabric_Type", y="Scrap_Cost", color="Fabric_Type"
        )
        st.plotly_chart(cost_fig, use_container_width=True)

    with tab_breakdown:
        st.subheader("Scrap by Machine")
        machine_fig = px.bar(
            df_filtered.groupby("Machine_ID", as_index=False)["Quantity_Scrapped_meters"].sum(),
            x="Machine_ID", y="Quantity_Scrapped_meters", color="Machine_ID"
        )
        st.plotly_chart(machine_fig, use_container_width=True)

        st.subheader("Defect Type Distribution")
        defect_fig = px.pie(
            df_filtered.groupby("Defect_Type", as_index=False)["Quantity_Scrapped_meters"].sum(),
            names="Defect_Type", values="Quantity_Scrapped_meters"
        )
        st.plotly_chart(defect_fig, use_container_width=True)

        # Export filtered data
        st.subheader("💾 Export Filtered Data")
        st.download_button(
            "Download CSV",
            data=df_filtered.to_csv(index=False).encode("utf-8"),
            file_name="filtered_quality_report.csv",
            mime="text/csv"
        )

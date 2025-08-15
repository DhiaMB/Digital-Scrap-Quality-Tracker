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

    # --- Sidebar Filters ---
    st.sidebar.header("🔧 Filters")
    if "qr_selected_date" not in st.session_state:
        st.session_state.qr_selected_date = (df["Date"].min(), df["Date"].max())
    if "qr_selected_machines" not in st.session_state:
        st.session_state.qr_selected_machines = df["Machine_ID"].unique().tolist()
    if "qr_selected_defects" not in st.session_state:
        st.session_state.qr_selected_defects = df["Defect_Type"].unique().tolist()
    if "qr_selected_shift" not in st.session_state:
        st.session_state.qr_selected_shift = df["Shift"].unique().tolist()

    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.qr_selected_date = (df["Date"].min(), df["Date"].max())
        st.session_state.qr_selected_machines = df["Machine_ID"].unique().tolist()
        st.session_state.qr_selected_defects = df["Defect_Type"].unique().tolist()
        st.session_state.qr_selected_shift = df["Shift"].unique().tolist()

    selected_date = st.sidebar.date_input("Select Date Range", key="qr_selected_date")
    selected_machines = st.sidebar.multiselect("Select Machines", df["Machine_ID"].unique(), key="qr_selected_machines")
    selected_defects  = st.sidebar.multiselect("Select Defect Types", df["Defect_Type"].unique(), key="qr_selected_defects")
    selected_shift    = st.sidebar.multiselect("Select Shifts", df["Shift"].unique(), key="qr_selected_shift")

    # --- Filter DataFrame ---
    df_filtered = df[
        (df["Date"] >= pd.to_datetime(selected_date[0])) &
        (df["Date"] <= pd.to_datetime(selected_date[1])) &
        (df["Machine_ID"].isin(selected_machines)) &
        (df["Defect_Type"].isin(selected_defects)) &
        (df["Shift"].isin(selected_shift))
    ]

    # --- Tabs ---
    tab_kpi, tab_trend, tab_breakdown = st.tabs(["📊 KPIs", "📈 Trend", "🧵 Breakdown"])

    # ---- KPI TAB ----
    with tab_kpi:
        st.subheader("Key Metrics")
        total_scrap = df_filtered["Quantity_Scrapped_meters"].sum()
        top_defect = df_filtered["Defect_Type"].mode()[0] if not df_filtered.empty else "-"
        shift_count = df_filtered["Shift"].nunique()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Scrap (m)", total_scrap)
        c2.metric("Most Frequent Defect", top_defect)
        c3.metric("Shifts Involved", shift_count)

    # ---- Trend TAB ----
    with tab_trend:
        st.subheader("Scrap Quantity Over Time")
        trend_fig = px.line(
            df_filtered.groupby("Date", as_index=False)["Quantity_Scrapped_meters"].sum(),
            x="Date", y="Quantity_Scrapped_meters", markers=True
        )
        st.plotly_chart(trend_fig, use_container_width=True)

    # ---- Breakdown TAB ----
    with tab_breakdown:
        st.subheader("🏆 Top Contributors")

        # Top 5 Machines
        top_machines = (
            df_filtered.groupby("Machine_ID")["Quantity_Scrapped_meters"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        st.markdown("**Top 5 Machines with Most Scrap**")
        fig_top_machines = px.bar(
            top_machines,
            x="Quantity_Scrapped_meters",
            y="Machine_ID",
            orientation='h',
            color="Machine_ID",
            text="Quantity_Scrapped_meters",
        )
        st.plotly_chart(fig_top_machines, use_container_width=True)

        # Top 5 Defect Types
        #top_defects = (
            #df_filtered.groupby("Defect_Type")["Quantity_Scrapped_meters"]
            #.sum()
            #.sort_values(ascending=False)
            #.head(5)
            #.reset_index()
        #)
        #st.markdown("**Top 5 Defect Types**")
        #fig_top_defects = px.bar(
            #top_defects,
            #x="Quantity_Scrapped_meters",
            #y="Defect_Type",
            #orientation='h',
            #color="Defect_Type",
            #text="Quantity_Scrapped_meters",
        #)
        #st.plotly_chart(fig_top_defects, use_container_width=True)

        # Top 5 Shifts
        top_shifts = (
            df_filtered.groupby("Shift")["Quantity_Scrapped_meters"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        st.markdown("**Top Shifts with Most Scrap**")
        fig_top_shifts = px.bar(
            top_shifts,
            x="Quantity_Scrapped_meters",
            y="Shift",
            orientation='h',
            color="Shift",
            text="Quantity_Scrapped_meters",
        )
        st.plotly_chart(fig_top_shifts, use_container_width=True)



        # Scrap by Defect Type
        st.subheader("Scrap by Defect Type")
        defect_fig = px.pie(
            df_filtered.groupby("Defect_Type", as_index=False)["Quantity_Scrapped_meters"].sum(),
            names="Defect_Type", values="Quantity_Scrapped_meters"
        )
        st.plotly_chart(defect_fig, use_container_width=True)


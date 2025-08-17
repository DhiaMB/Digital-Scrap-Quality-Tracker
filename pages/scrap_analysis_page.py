import streamlit as st
import pandas as pd
import plotly.express as px

def show_scrap_analysis_page():
    st.title("📊 Scrap Analysis")

    # Check if data is uploaded
    if "df" not in st.session_state or st.session_state.df is None:
        st.info("📂 Please upload a file first on the Upload Data page.")
        return

    df = st.session_state.df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # --- Sidebar Filters ---
    st.sidebar.header("🔧 Filters")
    if "sa_selected_date" not in st.session_state:
        st.session_state.sa_selected_date = (df["Date"].min(), df["Date"].max())
    if "sa_selected_machines" not in st.session_state:
        st.session_state.sa_selected_machines = df["Machine_ID"].unique().tolist()
    if "sa_selected_defects" not in st.session_state:
        st.session_state.sa_selected_defects = df["Defect_Type"].unique().tolist()
    if "sa_selected_fabric" not in st.session_state:
        st.session_state.sa_selected_fabric = df["Fabric_Type"].unique().tolist()

    if st.sidebar.button("🔄 Reset Filters"):
        st.session_state.sa_selected_date = (df["Date"].min(), df["Date"].max())
        st.session_state.sa_selected_machines = df["Machine_ID"].unique().tolist()
        st.session_state.sa_selected_defects = df["Defect_Type"].unique().tolist()
        st.session_state.sa_selected_fabric = df["Fabric_Type"].unique().tolist()

    selected_date = st.sidebar.date_input("Select Date Range", key="sa_selected_date")
    selected_machines = st.sidebar.multiselect("Select Machines", df["Machine_ID"].unique(), key="sa_selected_machines")
    selected_defects = st.sidebar.multiselect("Select Defect Types", df["Defect_Type"].unique(), key="sa_selected_defects")
    selected_fabric = st.sidebar.multiselect("Select Fabric Types", df["Fabric_Type"].unique(), key="sa_selected_fabric")

    time_granularity = st.sidebar.radio("Time Granularity", ["Day", "Week", "Month"])

    # --- Filter the DataFrame ---
    df_filtered = df[
        (df["Date"] >= pd.to_datetime(selected_date[0])) &
        (df["Date"] <= pd.to_datetime(selected_date[1])) &
        (df["Machine_ID"].isin(selected_machines)) &
        (df["Defect_Type"].isin(selected_defects)) &
        (df["Fabric_Type"].isin(selected_fabric))
    ]
        # --- Resample according to time granularity ---
    if not df_filtered.empty:
        df_filtered["Date_Resampled"] = df_filtered["Date"]
        if time_granularity == "Week":
            df_filtered["Date_Resampled"] = df_filtered["Date"].dt.to_period("W").apply(lambda r: r.start_time)
        elif time_granularity == "Month":
            df_filtered["Date_Resampled"] = df_filtered["Date"].dt.to_period("M").apply(lambda r: r.start_time)


    # --- Tabs ---
    tab_kpi, tab_trend, tab_breakdown , tab_cost, tab_insights = st.tabs(["📊 KPIs", "📈 Trend & Cost", "🧵 Breakdown","💰 Cost Contributors","💡 Insights"])

    # ---- KPI TAB ----
    with tab_kpi:
        st.subheader("Key Performance Indicators")
        st.write("Overall scrap KPIs for the selected date range and filters.")
        total_scrap = df_filtered["Quantity_Scrapped_meters"].sum()
        total_cost = df_filtered["Scrap_Cost"].sum()
        top_defect = df_filtered["Defect_Type"].mode()[0] if not df_filtered.empty else "-"
        machine_count = df_filtered["Machine_ID"].nunique()

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Scrap (m)", total_scrap)
        c2.metric("Total Scrap Cost", f"${total_cost:,.2f}")
        c3.metric("Most Frequent Defect", top_defect)

    # ---- Trend & Cost TAB ----
    with tab_trend:
        st.subheader("Scrap Trend Over Time({time_granularity})")
        st.write("Explore how scrap quantity evolves over time and across machines/defects.")

        trend_fig = px.line(
            df_filtered.groupby("Date", as_index=False)["Quantity_Scrapped_meters"].sum(),
            x="Date", y="Quantity_Scrapped_meters", markers=True
        )
        st.plotly_chart(trend_fig, use_container_width=True)

        st.subheader("Scrap Trend per Machine")
        machine_trend = df_filtered.groupby(["Date", "Machine_ID"], as_index=False)["Quantity_Scrapped_meters"].sum()
        fig_machine_trend = px.line(machine_trend, x="Date", y="Quantity_Scrapped_meters", color="Machine_ID", markers=True)
        st.plotly_chart(fig_machine_trend, use_container_width=True)

        st.subheader("Scrap per Defect Type Over Time")
        defect_trend = df_filtered.groupby(["Date", "Defect_Type"], as_index=False)["Quantity_Scrapped_meters"].sum()
        fig_defect_trend = px.area(defect_trend, x="Date", y="Quantity_Scrapped_meters", color="Defect_Type")
        st.plotly_chart(fig_defect_trend, use_container_width=True)



    # ---- Breakdown TAB ----
    with tab_breakdown:
        st.subheader("Top 5 Machines with Most Scrap")
        st.write("Identify the major contributors to scrap quantity.")

        top_machines = (
            df_filtered.groupby("Machine_ID")["Quantity_Scrapped_meters"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        fig_top_machines = px.bar(
            top_machines, x="Quantity_Scrapped_meters", y="Machine_ID",
            orientation='h', color="Machine_ID", title="Top 5 Machines by Scrap"
        )
        st.plotly_chart(fig_top_machines, use_container_width=True)

        # Cumulative scrap per machine
        st.subheader("Cumulative Scrap per Machine Over Time")
        machine_trend = (
            df_filtered.groupby(["Date", "Machine_ID"], as_index=False)["Quantity_Scrapped_meters"]
            .sum()
            .sort_values(["Machine_ID", "Date"])
        )
        machine_trend["Cumulative_Scrap"] = machine_trend.groupby("Machine_ID")["Quantity_Scrapped_meters"].cumsum()
        fig_machine_cum = px.line(
            machine_trend, x="Date", y="Cumulative_Scrap", color="Machine_ID",
            title="Cumulative Scrap per Machine"
        )
        st.plotly_chart(fig_machine_cum, use_container_width=True)

        # Cumulative scrap per defect type
        st.subheader("Cumulative Scrap per Defect Type Over Time")
        defect_trend = (
            df_filtered.groupby(["Date", "Defect_Type"], as_index=False)["Quantity_Scrapped_meters"]
            .sum()
            .sort_values(["Defect_Type", "Date"])
        )
        defect_trend["Cumulative_Scrap"] = defect_trend.groupby("Defect_Type")["Quantity_Scrapped_meters"].cumsum()
        fig_defect_cum = px.line(
            defect_trend, x="Date", y="Cumulative_Scrap", color="Defect_Type",
            title="Cumulative Scrap per Defect Type"
        )
        st.plotly_chart(fig_defect_cum, use_container_width=True)

        st.subheader("Defect Type Distribution")
        defect_fig = px.pie(
            df_filtered.groupby("Defect_Type", as_index=False)["Quantity_Scrapped_meters"].sum(),
            names="Defect_Type", values="Quantity_Scrapped_meters",
            title="Defect Type Share"
        )
        st.plotly_chart(defect_fig, use_container_width=True)


# ---- COST Contributors TAB ----
    with tab_cost:
        st.subheader("Treemap: Scrap Cost by Machine")
        treemap_machine = px.treemap(
            df_filtered.groupby("Machine_ID", as_index=False)[["Scrap_Cost", "Quantity_Scrapped_meters"]].sum(),
            path=["Machine_ID"],
            values="Scrap_Cost",
            color="Scrap_Cost",
            hover_data=["Quantity_Scrapped_meters"],
            color_continuous_scale="Reds",
            title="Scrap Cost Contribution per Machine"
        )
        st.plotly_chart(treemap_machine, use_container_width=True)

        st.subheader("Treemap: Scrap Cost by Fabric Type")
        treemap_fabric = px.treemap(
            df_filtered.groupby("Fabric_Type", as_index=False)[["Scrap_Cost", "Quantity_Scrapped_meters"]].sum(),
            path=["Fabric_Type"],
            values="Scrap_Cost",
            color="Scrap_Cost",
            hover_data=["Quantity_Scrapped_meters"],
            color_continuous_scale="Blues",
            title="Scrap Cost Contribution per Fabric Type"
        )
        st.plotly_chart(treemap_fabric, use_container_width=True)

        st.subheader("Treemap: Scrap Cost by Defect Type")
        treemap_defect = px.treemap(
            df_filtered.groupby("Defect_Type", as_index=False)[["Scrap_Cost", "Quantity_Scrapped_meters"]].sum(),
            path=["Defect_Type"],
            values="Scrap_Cost",
            color="Scrap_Cost",
            hover_data=["Quantity_Scrapped_meters"],
            color_continuous_scale="Greens",
            title="Scrap Cost Contribution per Defect Type"
        )
        st.plotly_chart(treemap_defect, use_container_width=True)
        # ---- New Tab: Cost & Quantity Insights ----
    with tab_insights:
        st.subheader("Machines: Scrap Quantity vs Cost")
        machine_stats = df_filtered.groupby("Machine_ID", as_index=False).agg({
            "Quantity_Scrapped_meters": "sum",
            "Scrap_Cost": "sum"
        })
        fig_machine_stats = px.scatter(
            machine_stats,
            x="Quantity_Scrapped_meters",
            y="Scrap_Cost",
            size="Scrap_Cost",
            color="Machine_ID",
            hover_data=["Quantity_Scrapped_meters", "Scrap_Cost"],
            title="Machine Scrap Quantity vs Cost"
        )
        st.plotly_chart(fig_machine_stats, use_container_width=True, key="insights_machine")

        st.subheader("Fabrics: Scrap Quantity vs Cost")
        fabric_stats = df_filtered.groupby("Fabric_Type", as_index=False).agg({
            "Quantity_Scrapped_meters": "sum",
            "Scrap_Cost": "sum"
        })
        fig_fabric_stats = px.scatter(
            fabric_stats,
            x="Quantity_Scrapped_meters",
            y="Scrap_Cost",
            size="Scrap_Cost",
            color="Fabric_Type",
            hover_data=["Quantity_Scrapped_meters", "Scrap_Cost"],
            title="Fabric Scrap Quantity vs Cost"
        )
        st.plotly_chart(fig_fabric_stats, use_container_width=True, key="insights_fabric")

        st.subheader("Defects: Scrap Quantity vs Cost")
        defect_stats = df_filtered.groupby("Defect_Type", as_index=False).agg({
            "Quantity_Scrapped_meters": "sum",
            "Scrap_Cost": "sum"
        })
        fig_defect_stats = px.scatter(
            defect_stats,
            x="Quantity_Scrapped_meters",
            y="Scrap_Cost",
            size="Scrap_Cost",
            color="Defect_Type",
            hover_data=["Quantity_Scrapped_meters", "Scrap_Cost"],
            title="Defect Scrap Quantity vs Cost"
        )
        st.plotly_chart(fig_defect_stats, use_container_width=True, key="insights_defect")

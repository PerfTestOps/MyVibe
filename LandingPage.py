import streamlit as st
import pandas as pd
import altair as alt
import plotly.graph_objects as go

import AddingUser
import AddProject
import ActualsVsForecast
import UpdatingActualsWithFilter
import UpdateForecast
import ActualsByMonth
import ActualsByYear

def show_page():
    st.set_page_config(page_title="Revenue Dashboard", layout="wide")
    st.sidebar.title("📁 Navigation")

    # Check authentication
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.error("🚫 You must be logged in to view this page.")
        st.stop()

    # Get role
    role = st.session_state.get("role", "Unknown")

    # Role-based menu
    if role == "Admin":
        page_options = [
            "Home",
            "Add User",
            "Add Project",
            "Actuals Vs Forecast",
            "Update Actuals",
            "Update Forecast",
            "Actuals By Month",
            "Actuals By Year",
            "Settings"
        ]
    elif role == "Contributor":
        page_options = [
            "Home",
            "Actuals Vs Forecast",
            "Update Actuals",
            "Update Forecast",
            "Actuals By Month",
            "Actuals By Year",
            "Settings"
        ]
    elif role == "Viewer":
        page_options = [
            "Home",
            "Actuals Vs Forecast",
            "Actuals By Month",
            "Actuals By Year",
            "Settings"
        ]
    else:
        page_options = ["Home"]

    st.sidebar.caption(f"👤 Logged in as: {role}")
    page = st.sidebar.radio("Go to", page_options)

    if page == "Home":
        st.title("🏠 Welcome to the Dashboard")
        st.markdown("---")

        excel_file = "BaseDatasheet.xlsx"
        df = pd.read_excel(excel_file, sheet_name="Sheet1")
        df = df[df["Active"].astype(str).str.lower() == "yes"]

        actual_cols = [col for col in df.columns if "Actuals" in col]
        df[actual_cols] = df[actual_cols].fillna(0)
        df["Actuals_YTD"] = df[actual_cols].sum(axis=1)
        total_revenue = df["Actuals_YTD"].sum()

        st.markdown(
            f"<h3 style='color:#1f77b4; font-weight:bold; text-align:center;'>Total YTD Revenue: <b>${total_revenue:,.0f}</b></h3>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        summary_df = df.groupby("ServiceLine", as_index=False)["Actuals_YTD"].sum()
        summary_df["RevenueLabel"] = summary_df["Actuals_YTD"].apply(lambda x: f"${x:,.0f}")

        bar_base_1 = alt.Chart(summary_df).encode(
            y=alt.Y("ServiceLine:N", sort="-x"),
            x=alt.X("Actuals_YTD:Q", axis=alt.Axis(format="$,.0f"))
        )
        bars_1 = bar_base_1.mark_bar(size=25).encode(
            color=alt.Color("ServiceLine:N", scale=alt.Scale(scheme="pastel1"), legend=None)
        )
        labels_1 = bar_base_1.mark_text(align="left", baseline="middle", dx=5, fontSize=13, color="white").encode(
            text="RevenueLabel:N"
        )
        with col1:
            st.altair_chart(
                (bars_1 + labels_1).properties(title="💰 YTD Revenue by Service Line", height=280).configure_title(
                    fontSize=20, fontWeight="bold", color="#1f77b4"
                ).configure_view(stroke=None),
                use_container_width=True
            )

        with st.expander("📄 View Service Line Table"):
            st.dataframe(summary_df.sort_values("Actuals_YTD", ascending=False), use_container_width=True)

        region_df = df.groupby("Region", as_index=False)["Actuals_YTD"].sum()
        region_df["RevenueLabel"] = region_df["Actuals_YTD"].apply(lambda x: f"${x:,.0f}")

        bar_base_2 = alt.Chart(region_df).encode(
            y=alt.Y("Region:N", sort="-x"),
            x=alt.X("Actuals_YTD:Q", axis=alt.Axis(format="$,.0f"))
        )
        bars_2 = bar_base_2.mark_bar(size=25).encode(
            color=alt.Color("Region:N", scale=alt.Scale(scheme="pastel2"), legend=None)
        )
        labels_2 = bar_base_2.mark_text(align="left", baseline="middle", dx=5, fontSize=13, color="white").encode(
            text="RevenueLabel:N"
        )
        with col2:
            st.altair_chart(
                (bars_2 + labels_2).properties(title="🌐 YTD Revenue by Region", height=280).configure_title(
                    fontSize=20, fontWeight="bold", color="#1f77b4"
                ).configure_view(stroke=None),
                use_container_width=True
            )

        with st.expander("📄 View Region Table"):
            st.dataframe(region_df.sort_values("Actuals_YTD", ascending=False), use_container_width=True)

        st.markdown("---")
        pie_col1, pie_col2 = st.columns(2)

        with pie_col1:
            st.markdown("### 🥧 Revenue Contribution by Service Line")
            fig1 = go.Figure(data=[go.Pie(
                labels=summary_df["ServiceLine"],
                values=summary_df["Actuals_YTD"],
                textinfo="percent",
                textposition="outside",
                hole=0.3
            )])
            fig1.update_traces(marker=dict(line=dict(color="#000000", width=1)))
            fig1.update_layout(title_text="Service Line Contribution", title_font_size=16)
            st.plotly_chart(fig1, use_container_width=True)

        with pie_col2:
            st.markdown("### 🥧 Revenue Contribution by Region")
            fig2 = go.Figure(data=[go.Pie(
                labels=region_df["Region"],
                values=region_df["Actuals_YTD"],
                textinfo="percent",
                textposition="outside",
                hole=0.3
            )])
            fig2.update_traces(marker=dict(line=dict(color="#000000", width=1)))
            fig2.update_layout(title_text="Region Contribution", title_font_size=16)
            st.plotly_chart(fig2, use_container_width=True)

    elif page == "Add User":
        AddingUser.show_page()
    elif page == "Add Project":
        AddProject.show_page()
    elif page == "Actuals Vs Forecast":
        ActualsVsForecast.show_page()
    elif page == "Update Actuals":
        UpdatingActualsWithFilter.show_page()
    elif page == "Update Forecast":
        UpdateForecast.show_page()
    elif page == "Actuals By Month":
        ActualsByMonth.show_page()
    elif page == "Actuals By Year":
        ActualsByYear.show_page()
    elif page == "Settings":
        st.title("⚙️ Settings")
        st.write("Control app preferences, theme options, or configuration.")

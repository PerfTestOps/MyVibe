import pandas as pd
import streamlit as st
import altair as alt
from datetime import datetime


def show_page():
    # --- Load Data ---
    df = pd.read_excel("BaseDatasheet.xlsx", sheet_name="MonthByYear", index_col=0)
    df = df.T.reset_index()
    df[['Vertical', 'Year']] = df['index'].str.split('-', expand=True)
    df.drop('index', axis=1, inplace=True)

    # --- Sidebar Filters ---
    st.sidebar.title("📂 Filter Revenue Data")

    # Define current and previous year
    current_year = str(datetime.now().year)
    previous_year = str(datetime.now().year - 1)
    available_years = sorted(df["Year"].unique())
    default_years = [y for y in [current_year, previous_year] if y in available_years]

    selected_years = st.sidebar.multiselect("Choose Years", available_years, default=default_years)

    # Horizontal checkboxes for Verticals with BFS preselected
    st.sidebar.markdown("### Choose Verticals")
    verticals = sorted(df["Vertical"].unique())
    num_cols = 3
    cols = st.sidebar.columns(num_cols)
    selected_verticals = []

    for idx, vertical in enumerate(verticals):
        col = cols[idx % num_cols]
        default_check = True if vertical == "BFS" else False
        if col.checkbox(vertical, value=default_check):
            selected_verticals.append(vertical)

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    month_map = {month: i+1 for i, month in enumerate(month_order)}

    month_columns = [col for col in df.columns if col not in ["Vertical", "Year"]]
    default_months = [m for m in month_order if m in month_columns]
    selected_months = st.sidebar.multiselect("Choose Months", default_months, default=default_months)

    # --- Filter & Melt Data ---
    filtered_df = df[(df["Vertical"].isin(selected_verticals)) & (df["Year"].isin(selected_years))]
    melted = filtered_df.melt(id_vars=["Vertical", "Year"], value_vars=selected_months,
                              var_name="Month", value_name="Revenue")

    melted["Month_Num"] = melted["Month"].map(month_map)
    melted = melted.sort_values("Month_Num")
    melted["Month"] = pd.Categorical(melted["Month"], categories=month_order, ordered=True)
    melted["Legend_Key"] = melted["Vertical"] + " - " + melted["Year"]

    # --- Main Title ---
    st.title("📊 Revenue Trending Year on Year")

    # --- Altair Charts ---
    base_chart = alt.Chart(melted).mark_line(point=True).encode(
        x=alt.X("Month:N", sort=month_order),
        y=alt.Y("Revenue:Q", title="Revenue ($)"),
        color=alt.Color("Legend_Key:N", legend=alt.Legend(title="Vertical-Year")),
        tooltip=["Vertical", "Year", "Month", "Revenue"]
    ).properties(width=850, height=450)

    trend_lines = alt.Chart(melted).transform_regression(
        "Month_Num", "Revenue", groupby=["Legend_Key"]
    ).mark_line(strokeDash=[4, 2], color="gray").encode(
        x=alt.X("Month_Num:Q", axis=alt.Axis(
            title="Month",
            values=list(range(1, 13)),
            labelExpr='["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][datum.value - 1]'
        )),
        y="Revenue:Q",
        detail="Legend_Key:N"
    )

    # --- Combine & Display ---
    st.altair_chart(base_chart + trend_lines, use_container_width=True)

    # --- Summary Stats ---
    with st.expander("📈 Summary Statistics"):
        summary = melted.groupby(["Vertical", "Year"])["Revenue"].sum().reset_index()
        st.dataframe(summary.style.format({"Revenue": "{:,.0f}"}))


show_page()
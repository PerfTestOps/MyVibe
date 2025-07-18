import streamlit as st
import pandas as pd
import altair as alt


def show_page():

    # Load the Excel file
    excel_file = "BaseDatasheet.xlsx"
    sheet_name = "Sheet1"

    # Read the data
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    st.title("📁 Forecast vs Actuals by Project")

    # Extract month options
    month_options = []
    for col in df.columns:
        if "Actuals" in col:
            month = col.split()[0]
            forecast_col = f"{month} Forecast"
            if forecast_col in df.columns:
                month_options.append(month)

    # Month selector
    selected_month = st.selectbox("Select a month", month_options)

    # Project selector
    project_names = df["Project Name"].dropna().unique()
    selected_project = st.selectbox("Select a project", project_names)

    # Filter data for selected project
    project_data = df[df["Project Name"] == selected_project]

    # Get relevant columns
    actual_col = f"{selected_month} Actuals"
    forecast_col = f"{selected_month} Forecast"

    # Display comparison
    st.subheader(f"📊 {selected_month} Forecast vs Actuals for Project: {selected_project}")
    if not project_data.empty:
        actual = project_data[actual_col].sum() if actual_col in project_data else 0
        forecast = project_data[forecast_col].sum() if forecast_col in project_data else 0

        # Create a DataFrame for chart
        chart_df = pd.DataFrame({
            "Metric": ["Forecast", "Actual"],
            "Value": [forecast, actual],
            "Color": ["#1f77b4", "#ff7f0e"]  # Blue for Forecast, Orange for Actual
        })

        # Show metrics
        st.metric(label="Total Forecast", value=forecast)
        st.metric(label="Total Actual", value=actual)
        st.metric(label="Difference", value=actual - forecast)

        # Draw colored bar chart using Altair
        chart = alt.Chart(chart_df).mark_bar().encode(
            x=alt.X("Metric", title="Revenue Projected Vs Revenue Actual"),
            y=alt.Y("Value", title="Dollars"),
            color=alt.Color("Color", scale=None),  # Use custom colors
            tooltip=["Metric", "Value"]
        ).properties(width=400)

        st.altair_chart(chart, use_container_width=True)
    else:
        st.warning("No data found for the selected project.")

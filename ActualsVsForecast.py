import streamlit as st
import pandas as pd
import altair as alt

def show_page():
# Load Excel
    excel_file = "BaseDatasheet.xlsx"
    sheet_name = "Sheet1"
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    st.title("📁 Forecast vs Actuals by Project")

    # Extract valid months
    month_options = []
    for col in df.columns:
        if "Actuals" in col:
            m = col.split()[0]
            if f"{m} Forecast" in df.columns:
                month_options.append(m)

    # Select project
    project_names = df["Project Name"].dropna().unique()
    selected_project = st.selectbox("Select a project", project_names)
    project_data = df[df["Project Name"] == selected_project]

    # Select months
    st.markdown("### 🗓️ Select Months for Comparison")
    selected_months = []
    cols = st.columns(4)
    for i, m in enumerate(month_options):
        with cols[i % 4]:
            if st.checkbox(m, key=f"month_{m}"):
                selected_months.append(m)

    # Show chart
    if selected_months and not project_data.empty:
        st.subheader(f"📊 Actuals & Forecast per Month for {selected_project}")

        chart_rows = []
        label_order = []

        for m in selected_months:
            actual_col = f"{m} Actuals"
            forecast_col = f"{m} Forecast"
            actual = project_data[actual_col].sum() if actual_col in project_data else 0
            forecast = project_data[forecast_col].sum() if forecast_col in project_data else 0

            chart_rows.append({
                "Month": m,
                "Label": f"{m} - Actual",
                "Metric": "Actual",
                "Value": actual,
                "ValueLabel": f"${actual:,.0f}"
            })
            chart_rows.append({
                "Month": m,
                "Label": f"{m} - Forecast",
                "Metric": "Forecast",
                "Value": forecast,
                "ValueLabel": f"${forecast:,.0f}"
            })
            label_order.extend([f"{m} - Actual", f"{m} - Forecast"])

        df_chart = pd.DataFrame(chart_rows)

        # Bar chart layer
        bars = alt.Chart(df_chart).mark_bar(size=20).encode(
            y=alt.Y("Label:N", title="Month - Metric", sort=label_order),
            x=alt.X("Value:Q", title="Amount"),
            color=alt.Color("Metric:N", title="Type", scale=alt.Scale(
                domain=["Forecast", "Actual"],
                range=["#1f77b4", "#ff7f0e"]
            )),
            tooltip=["Month", "Metric", "ValueLabel"]
        )

        # Text layer inside the bars
        labels = alt.Chart(df_chart).mark_text(
            align='left',
            baseline='middle',
            dx=5,  # slight shift to the right for visibility
            color='white'  # text inside the bar
        ).encode(
            y=alt.Y("Label:N", sort=label_order),
            x=alt.X("Value:Q"),
            text=alt.Text("ValueLabel:N")
        )

        chart = (bars + labels).properties(height=50 * len(label_order))
        st.altair_chart(chart, use_container_width=True)

    elif not selected_months:
        st.info("☝️ Please select one or more months.")
    else:
        st.warning("⚠️ No data found for the selected project.")

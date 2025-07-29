import streamlit as st
import pandas as pd
import altair as alt


def show_page():
# Load Excel file
    excel_file = "BaseDatasheet.xlsx"
    sheet_name = "Sheet1"
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    st.title("📅 Monthly Actuals Revenue Comparison")

    # Define calendar month order
    month_order = [
        "Jan", "Feb", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Identify Actuals columns
    actuals_cols = [col for col in df.columns if "Actuals" in col]

    # 🎯 Multi-select for projects
    st.markdown("### 🎯 Filter by Project(s)")
    projects = df["Project Name"].unique().tolist()
    projects.insert(0, "All Projects")
    selected_projects = st.multiselect("Choose one or more projects", options=projects, default="All Projects")

    # ✅ Select months to compare
    st.markdown("### ✅ Select Months to Compare")
    selected_months = []
    cols = st.columns(4)
    for i, col in enumerate(actuals_cols):
        month = col.replace(" Actuals", "")
        with cols[i % 4]:
            if st.checkbox(month, key=col):
                selected_months.append(col)

    # Filter data based on selected projects
    if "All Projects" in selected_projects or not selected_projects:
        filtered_df = df.copy()
    else:
        filtered_df = df[df["Project Name"].isin(selected_projects)]

    # Show charts if months are selected
    if selected_months:
        # 🔹 Total actuals chart
        totals = filtered_df[selected_months].sum().reset_index()
        totals.columns = ["Month", "Total Actuals"]
        totals["Month"] = totals["Month"].str.replace(" Actuals", "", regex=False)
        totals["Month"] = pd.Categorical(totals["Month"], categories=month_order, ordered=True)
        totals = totals.sort_values("Month")

        st.markdown("### 📊 Total Actuals by Month")
        bar = alt.Chart(totals).mark_bar().encode(
            x=alt.X("Month", title="Month", sort=month_order),
            y=alt.Y("Total Actuals", title="Revenue"),
            color=alt.Color("Month", legend=None),
            tooltip=["Month", "Total Actuals"]
        )
        text = alt.Chart(totals).mark_text(
            align="center",
            baseline="middle",
            dy=10,
            color="white"
        ).encode(
            x=alt.X("Month", sort=month_order),
            y="Total Actuals",
            text=alt.Text("Total Actuals", format=".0f")
        )
        st.altair_chart(bar + text, use_container_width=True)

        # 📈 Trend line chart by project
        st.markdown("### 📈 Actuals Trend Line by Project")
        line_data = filtered_df[["Project Name"] + selected_months].melt(
            id_vars="Project Name",
            var_name="Month",
            value_name="Actuals"
        )
        line_data["Month"] = line_data["Month"].str.replace(" Actuals", "", regex=False)
        line_data["Month"] = pd.Categorical(line_data["Month"], categories=month_order, ordered=True)

        line_chart = alt.Chart(line_data).mark_line(point=True).encode(
            x=alt.X("Month:N", title="Month", sort=month_order),
            y=alt.Y("Actuals:Q", title="Actuals"),
            color=alt.Color("Project Name:N", title="Project"),
            tooltip=["Project Name", "Month", "Actuals"]
        ).properties(height=400)

        st.altair_chart(line_chart, use_container_width=True)

    else:
        st.info("☝️ Please select one or more months to display the chart.")
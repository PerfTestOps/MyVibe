import streamlit as st
import pandas as pd
import altair as alt

# Load Excel file
excel_file = "BaseDatasheet.xlsx"
sheet_name = "Sheet1"
df = pd.read_excel(excel_file, sheet_name=sheet_name)

st.title("📅 Monthly Actuals Revenue Comparison")

# Define calendar month order (all 12 months)
month_order = [
    "Jan", "Feb", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Identify Actuals columns
actuals_cols = [col for col in df.columns if "Actuals" in col]

# 🎯 Multi-select for projects
st.markdown("### 🎯 Filter by Project(s)")
projects = df["Project Name"].unique().tolist()
projects.insert(0, "All Projects")  # Add 'All Projects' option

selected_projects = st.multiselect("Choose one or more projects", options=projects, default="All Projects")

# Create side-by-side checkboxes
st.markdown("### ✅ Select Months to Compare")
selected_months = []
cols = st.columns(4)
for i, col in enumerate(actuals_cols):
    month = col.replace(" Actuals", "")
    with cols[i % 4]:
        if st.checkbox(month, key=col):
            selected_months.append(col)

# Filter by selected projects
if "All Projects" in selected_projects or not selected_projects:
    filtered_df = df.copy()
else:
    filtered_df = df[df["Project Name"].isin(selected_projects)]

# If months are selected, calculate totals and show chart
if selected_months:
    totals = filtered_df[selected_months].sum().reset_index()
    totals.columns = ["Month", "Total Actuals"]
    totals["Month"] = totals["Month"].str.replace(" Actuals", "", regex=False)

    # Sort by calendar month order
    totals["Month"] = pd.Categorical(totals["Month"], categories=month_order, ordered=True)
    totals = totals.sort_values("Month")

    # Bar chart
    bar = alt.Chart(totals).mark_bar().encode(
        x=alt.X("Month", title="Month"),
        y=alt.Y("Total Actuals", title="Revenue"),
        color=alt.Color("Month", legend=None),
        tooltip=["Month", "Total Actuals"]
    )

    # Text labels inside bars
    text = alt.Chart(totals).mark_text(
        align="center",
        baseline="middle",
        dy=10,
        color="white"
    ).encode(
        x="Month",
        y="Total Actuals",
        text=alt.Text("Total Actuals", format=".0f")
    )

    st.altair_chart(bar + text, use_container_width=True)
else:
    st.info("☝️ Please select one or more months to display the chart.")

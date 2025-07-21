import streamlit as st
import pandas as pd
import altair as alt

def show_page():
    st.title("🧮 Monthly Billing Calculator")
    st.write("Calculate associate-wise billing based on attendance and rate.")

    # Load Sheet2 from Excel
    excel_file = "BaseDatasheet.xlsx"
    sheet_name = "Sheet2"
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Dropdown to select associate
    associates = df["AssociateName"].dropna().unique().tolist()
    selected = st.selectbox("Choose Associate", associates)

    filtered_df = df[df["AssociateName"] == selected].copy()

    if filtered_df.empty:
        st.warning("No data found for selected associate.")
        return

    # Define months and calculate billing
    months = ["Jan", "Feb", "March", "April", "May", "June"]
    billing_rate = filtered_df["BillingRateByMonth"].values[0]
    results = []

    for month in months:
        avail = filtered_df[f"{month}-Available Days"].values[0]
        leave = filtered_df[f"{month}-Leave Days"].values[0]
        extra = filtered_df[f"{month}-Extra Working Days"].values[0]

        billable_days = avail + extra - leave
        billing_amount = billable_days * billing_rate

        results.append({
            "Month": month,
            "Available": avail,
            "Leave": leave,
            "Extra": extra,
            "Billable Days": billable_days,
            "Billing Amount": billing_amount
        })

    result_df = pd.DataFrame(results)

    # 🔢 Add totals row
    total_row = pd.DataFrame([{
        "Month": "🔢 Total",
        "Available": result_df["Available"].sum(),
        "Leave": result_df["Leave"].sum(),
        "Extra": result_df["Extra"].sum(),
        "Billable Days": result_df["Billable Days"].sum(),
        "Billing Amount": result_df["Billing Amount"].sum()
    }])

    result_df = pd.concat([result_df, total_row], ignore_index=True)

    # 📄 Display billing summary
    st.markdown("### 📄 Billing Summary")
    st.dataframe(result_df.style.format({
        "Billing Amount": "₹{:,.0f}",
        "Billable Days": "{:.0f}"
    }))

    # 💰 Total revenue highlight
    total_revenue = result_df[result_df["Month"] == "🔢 Total"]["Billing Amount"].values[0]
    st.markdown(f"### 🧾 Total Revenue: ₹{int(total_revenue):,}")

    # 📊 Monthly billing chart (excluding total row)
    chart_data = result_df[result_df["Month"] != "🔢 Total"]

    st.markdown("### 📊 Monthly Billing Chart")
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X("Month:N", title="Month"),
        y=alt.Y("Billing Amount:Q", title="Amount"),
        color=alt.Color("Month:N", legend=None),
        tooltip=["Month", "Billing Amount"]
    )
    st.altair_chart(chart, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import re


def load_data(file_path: str, sheet_index: int = 1) -> pd.DataFrame:
    df = pd.read_excel(file_path, sheet_name=sheet_index)
    df.columns = [c.strip() for c in df.columns]
    df['ServiceLine'] = df['ServiceLine'].astype(str).str.strip().str.upper()
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.title("🔎 Filter By")

    filters = {
        'AssociateName': st.sidebar.multiselect("Associate Name", df['AssociateName'].dropna().unique()),
        'PracticeLine': st.sidebar.multiselect("Practice Line", df['PracticeLine'].dropna().unique()),
        'Region': st.sidebar.multiselect("Region", df['Region'].dropna().unique()),
    }

    for key, selected in filters.items():
        if selected:
            df = df[df[key].isin(selected)]

    with st.expander("📋 Active Filters"):
        for key, selected in filters.items():
            st.write(f"**{key}**: {', '.join(selected) if selected else 'All'}")

    return df


def extract_months(df: pd.DataFrame) -> list:
    pattern = re.compile(r'^([A-Za-z]+)-Available Days$')
    months = []
    for col in df.columns:
        match = pattern.match(col)
        if match:
            month = match.group(1)
            if month not in months:
                months.append(month)
    return months


def calculate_billing(row, month):
    try:
        available = row.get(f"{month}-Available Days", 0) or 0
        leave = row.get(f"{month}-Leave Days", 0) or 0
        extra = row.get(f"{month}-Extra Working Days", 0) or 0
        rate = row.get("BillingRateByMonth", 0) or 0
        return (available + extra - leave) * rate
    except:
        return 0


def prepare_billing_data(df: pd.DataFrame, month_order: list) -> pd.DataFrame:
    actual_data = []
    for sl in df['ServiceLine'].unique():
        for month in month_order:
            sub_df = df[df['ServiceLine'] == sl]
            billing_total = sum(calculate_billing(row, month) for _, row in sub_df.iterrows())
            actual_data.append({'ServiceLine': sl, 'Month': month, 'Billing Amount': billing_total})
    return pd.DataFrame(actual_data)


def generate_forecast(df: pd.DataFrame, month_order: list, months_to_forecast: int) -> pd.DataFrame:
    forecast_data = []
    for sl in df['ServiceLine'].unique():
        history = []
        sub_df = df[df['ServiceLine'] == sl]
        for month in month_order:
            billing_total = sum(calculate_billing(row, month) for _, row in sub_df.iterrows())
            history.append(billing_total)
        avg = sum(history[-3:]) / 3 if len(history) >= 3 else sum(history) / max(len(history), 1)
        for i in range(months_to_forecast):
            forecast_month = f"Forecast M+{i + 1}"
            forecast_data.append({'ServiceLine': sl, 'Month': forecast_month, 'Billing Amount': round(avg)})
    return pd.DataFrame(forecast_data)


def plot_billing_chart(combined_df: pd.DataFrame, months_to_forecast: int):
    fig = px.bar(
        combined_df,
        x='Month',
        y='Billing Amount',
        color='ServiceLine',
        barmode='group',
        text='Billing Amount',
        title=f"💰 Billing Forecast for Next {months_to_forecast} Month(s)",
        height=500
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title="Month", yaxis_title="Billing Amount (₹)")
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.set_page_config(page_title="Billing Forecast", layout="wide")
    st.title("💰 Workforce Billing Forecast")

    df = load_data("BaseDatasheet.xlsx")
    df = apply_filters(df)

    months_to_forecast = st.slider("🔮 Forecast next N months", 1, 6, 3)

    month_order = extract_months(df)

    actual_df = prepare_billing_data(df, month_order)
    forecast_df = generate_forecast(df, month_order, months_to_forecast)

    combined_df = pd.concat([actual_df, forecast_df])

    if combined_df.empty:
        st.warning("⚠️ No data available for the selected filters.")
    else:
        plot_billing_chart(combined_df, months_to_forecast)


if __name__ == "__main__":
    main()

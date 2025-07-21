import streamlit as st
import pandas as pd
import plotly.express as px
import re


def load_data(file_path: str, sheet_index: int = 1) -> pd.DataFrame:
    """Load and clean the Excel data."""
    df = pd.read_excel(file_path, sheet_name=sheet_index)
    df.columns = [c.strip() for c in df.columns]
    df['ServiceLine'] = df['ServiceLine'].astype(str).str.strip().str.upper()
    return df

def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Add sidebar filters and filter the DataFrame accordingly."""
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

def extract_months(df: pd.DataFrame, target: str) -> list:
    """Extract unique month names dynamically from column headers."""
    pattern = re.compile(r'^([A-Za-z]+)-' + re.escape(target) + r'$')
    months = []

    for col in df.columns:
        match = pattern.match(col)
        if match:
            month = match.group(1)
            if month not in months:
                months.append(month)
    return months

def generate_forecast(df: pd.DataFrame, month_order: list, target: str, months_to_forecast: int) -> pd.DataFrame:
    """Generate forecasted values using a simple 3-month moving average."""
    service_lines = df['ServiceLine'].unique()
    forecast_data = []

    for sl in service_lines:
        history = []
        for month in month_order:
            col = f"{month}-{target}"
            total = df[df['ServiceLine'] == sl][col].sum() if col in df.columns else 0
            history.append(total)

        avg = sum(history[-3:]) / 3 if len(history) >= 3 else sum(history) / max(len(history), 1)
        for i in range(months_to_forecast):
            forecast_month = f"Forecast M+{i + 1}"
            forecast_data.append({'ServiceLine': sl, 'Month': forecast_month, target: round(avg)})

    return pd.DataFrame(forecast_data)

def prepare_actual_data(df: pd.DataFrame, month_order: list, target: str) -> pd.DataFrame:
    """Prepare actual data for plotting."""
    actual_data = []
    for sl in df['ServiceLine'].unique():
        for month in month_order:
            col = f"{month}-{target}"
            total = df[df['ServiceLine'] == sl][col].sum() if col in df.columns else 0
            actual_data.append({'ServiceLine': sl, 'Month': month, target: total})
    return pd.DataFrame(actual_data)

def plot_forecast_chart(combined_df: pd.DataFrame, target: str, months_to_forecast: int):
    """Plot grouped bar chart with forecast and actual data."""
    fig = px.bar(
        combined_df,
        x='Month',
        y=target,
        color='ServiceLine',
        barmode='group',
        title=f"{target} Forecast for Next {months_to_forecast} Month(s)",
        text=target,
        height=500
    )
    fig.update_traces(textposition='outside')
    fig.update_layout(xaxis_title="Month", yaxis_title=target)
    st.plotly_chart(fig, use_container_width=True)

def main():
    #st.set_page_config(page_title="Workforce Forecast Billing Hours", layout="wide")
    st.title("📈 Workforce Forecast Calculator")

    # Load data
    df = load_data("BaseDatasheet.xlsx")

    # Target selection
    target = st.selectbox("Select value to forecast", ['Available Days', 'Leave Days', 'Extra Working Days'])

    # Forecast horizon
    months_to_forecast = st.slider("Forecast next N months", min_value=1, max_value=6, value=3)

    # Filter data
    df = apply_filters(df)

    # Extract months dynamically based on target
    month_order = extract_months(df, target)

    # Prepare forecast + actual data
    forecast_df = generate_forecast(df, month_order, target, months_to_forecast)
    actual_df = prepare_actual_data(df, month_order, target)

    # Combine and plot
    combined_df = pd.concat([actual_df, forecast_df])
    if combined_df.empty:
        st.warning("⚠️ No data available for the selected filters. Please adjust the filters and try again.")
    else:
        plot_forecast_chart(combined_df, target, months_to_forecast)


if __name__ == "__main__":
    main()
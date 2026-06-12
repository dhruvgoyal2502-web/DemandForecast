import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Detailed Forecasts", page_icon="🔍", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("../UpdatedForecast_Results_Final.xlsx")
    # Convert Forecast to integer to remove decimal points
    df['Forecast'] = df['Forecast'].round(0).astype(int)
    # Ensure Month is datetime
    df['Month'] = pd.to_datetime(df['Month'])
    return df

st.title("Detailed Forecasts")
st.markdown("Filter and view detailed forecasting data for specific regions, models, and vehicle types.")

try:
    df = load_data()

    # Filters
    st.sidebar.header("Filter Data")
    
    selected_model = st.sidebar.selectbox("Select Model", df['Model'].unique())
    selected_halb = st.sidebar.selectbox("Select HALB (Region)", ["All"] + df['HALB'].unique().tolist())
    selected_engine = st.sidebar.selectbox("Select Engine Type", ["All"] + df['Engine_Type'].unique().tolist())
    selected_vehicle = st.sidebar.selectbox("Select Vehicle Type", ["All"] + df['Vehicle_Type'].unique().tolist())

    # Date filter
    min_date = df['Month'].min().date()
    max_date = df['Month'].max().date()
    
    st.sidebar.markdown("---")
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    # Apply filters
    filtered_df = df[df['Model'] == selected_model]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[(filtered_df['Month'].dt.date >= start_date) & (filtered_df['Month'].dt.date <= end_date)]
    elif len(date_range) == 1:
        start_date = date_range[0]
        filtered_df = filtered_df[filtered_df['Month'].dt.date >= start_date]
    
    if selected_halb != "All":
        filtered_df = filtered_df[filtered_df['HALB'] == selected_halb]
    if selected_engine != "All":
        filtered_df = filtered_df[filtered_df['Engine_Type'] == selected_engine]
    if selected_vehicle != "All":
        filtered_df = filtered_df[filtered_df['Vehicle_Type'] == selected_vehicle]

    st.subheader(f"Data Preview ({len(filtered_df)} records)")
    st.markdown("The `Forecast` column is displayed as whole numbers.")
    
    # Show data table
    display_df = filtered_df[['HALB', 'Engine_Type', 'Map_Model', 'Vehicle_Type', 'Month', 'Actual_Demand', 'Forecast', 'Accuracy_Pct']]
    
    # Format month for display
    display_df_copy = display_df.copy()
    display_df_copy['Month'] = display_df_copy['Month'].dt.strftime('%Y-%m')
    
    st.dataframe(display_df_copy, use_container_width=True)

    st.markdown("---")

    # Time series for the filtered selection
    if not filtered_df.empty:
        st.subheader("Specific Trend: Actual vs Forecast")
        
        # Aggregate by Month just in case there are multiple map_models left
        trend_df = filtered_df.groupby('Month')[['Actual_Demand', 'Forecast']].sum().reset_index()

        fig = px.line(
            trend_df, 
            x="Month", 
            y=["Actual_Demand", "Forecast"],
            labels={"value": "Demand Volume", "variable": "Demand Type"},
            title=f"Trend for Filtered Selection ({selected_model})",
            markers=True
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")

except Exception as e:
    st.error(f"Error loading data: {e}")

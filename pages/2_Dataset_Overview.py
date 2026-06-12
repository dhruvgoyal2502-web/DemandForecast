import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dataset Overview", page_icon="📊", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("../UpdatedForecast_Results_Final.xlsx")
    # Convert Forecast to integer to remove decimal points
    df['Forecast'] = df['Forecast'].round(0).astype(int)
    # Ensure Month is datetime
    df['Month'] = pd.to_datetime(df['Month'])
    return df

st.title("Dataset Overview")
st.markdown("Explore the underlying data structures and the top drivers of demand.")

try:
    df = load_data()
    
    # We only need one record per Month/HALB/Vehicle/Engine/Model for actual demand analysis
    base_data = df.drop_duplicates(subset=['HALB', 'Engine_Type', 'Map_Model', 'Vehicle_Type', 'Month'])

    unique_regions = df['HALB'].nunique()
    unique_vehicles = df['Vehicle_Type'].nunique()
    unique_engines = df['Engine_Type'].nunique()
    unique_map_models = df['Map_Model'].nunique()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Unique Regions (HALB)", unique_regions)
    col2.metric("Vehicle Types", unique_vehicles)
    col3.metric("Engine Types", unique_engines)
    col4.metric("Specific Models", unique_map_models)

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("Records by Vehicle Type")
        vehicle_counts = base_data['Vehicle_Type'].value_counts().reset_index()
        vehicle_counts.columns = ['Vehicle_Type', 'Count']
        
        # Using a qualitative color palette for better distinguishable colors
        fig_vehicle = px.pie(
            vehicle_counts, 
            names='Vehicle_Type', 
            values='Count',
            title="Distribution of Vehicle Types",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_vehicle.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_vehicle, use_container_width=True)

    with col_chart2:
        st.subheader("Top 5 Engine Types by Demand")
        engine_demand = base_data.groupby('Engine_Type')['Actual_Demand'].sum().reset_index()
        engine_demand = engine_demand.sort_values('Actual_Demand', ascending=False).head(5)
        
        fig_engine = px.bar(
            engine_demand, 
            x='Engine_Type', 
            y='Actual_Demand',
            title="Top 5 Engine Types",
            text_auto='.2s',
            color='Engine_Type',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_engine.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_engine, use_container_width=True)

    st.markdown("---")
    
    st.subheader("Top 10 Vehicle Models by Actual Demand")
    model_demand = base_data.groupby('Map_Model')['Actual_Demand'].sum().reset_index()
    # Get top 10 models
    top_models = model_demand.sort_values('Actual_Demand', ascending=True).tail(10)
    
    fig_top_models = px.bar(
        top_models, 
        y='Map_Model', 
        x='Actual_Demand',
        orientation='h',
        title="Top 10 Best-Selling Vehicle Models (All Time)",
        text_auto='.2s',
        color='Actual_Demand',
        color_continuous_scale="Purples"
    )
    fig_top_models.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_top_models, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")

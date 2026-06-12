import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Model Performance", page_icon="🏆", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_excel("../UpdatedForecast_Results_Final.xlsx")
    return df

st.title("Model Performance Comparison")
st.markdown("Compare the performance of different machine learning models used for forecasting.")

try:
    df = load_data()
    
    # Group by Model to get average metrics
    # We take the mean of MAE, RMSE, MAPE, and Accuracy_Pct across all regions/vehicles
    model_metrics = df.groupby('Model')[['MAE', 'RMSE', 'MAPE', 'Accuracy_Pct']].mean().reset_index()

    st.subheader("Model Error Metrics (Averages)")
    
    # Display as a styled dataframe but keep it light without matplotlib dependencies
    st.dataframe(model_metrics.style.format({
        'MAE': "{:.2f}",
        'RMSE': "{:.2f}",
        'MAPE': "{:.2f}%",
        'Accuracy_Pct': "{:.2f}%"
    }), use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Accuracy Comparison")
        fig_acc = px.bar(
            model_metrics, 
            x='Model', 
            y='Accuracy_Pct', 
            color='Accuracy_Pct',
            title="Average Accuracy % by Model",
            text_auto='.2f',
            color_continuous_scale="Viridis"
        )
        fig_acc.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_acc, use_container_width=True)

    with col2:
        st.subheader("Error Comparison (RMSE)")
        fig_err = px.bar(
            model_metrics, 
            x='Model', 
            y='RMSE', 
            color='RMSE',
            title="Average RMSE by Model (Lower is better)",
            text_auto='.2f',
            color_continuous_scale="Reds"
        )
        fig_err.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_err, use_container_width=True)

except Exception as e:
    st.error(f"Error loading data: {e}")

import streamlit as st
import plotly.express as px
import pandas as pd
from utils.data_loader import load_data

# Page config must be first
st.set_page_config(
    page_title="Interactive Explorer",
    page_icon="🔍",
    layout="wide"
)

# Load data
cost_data, delivery_data, warehouse_data, shift_data = load_data()

# Check data
if delivery_data.empty:
    st.error("Failed to load delivery data")
    st.stop()

# Convert date to datetime if not already
if not pd.api.types.is_datetime64_any_dtype(delivery_data['Date']):
    delivery_data['Date'] = pd.to_datetime(delivery_data['Date'])

# Page title
st.title("🔍 Interactive Data Explorer")

# Tabs
tab1, tab2 = st.tabs(["Delivery Analysis", "Warehouse Analysis"])

with tab1:
    # Region filter
    regions = st.multiselect(
        "Select Regions",
        options=delivery_data['Region'].unique(),
        default=[delivery_data['Region'].unique()[0]] if len(delivery_data['Region'].unique()) > 0 else []
    )
    
    # Date range slider using Unix timestamps
    min_date = delivery_data['Date'].min()
    max_date = delivery_data['Date'].max()
    
    # Convert to datetime.date for Streamlit compatibility
    min_date_date = min_date.date()
    max_date_date = max_date.date()
    
    selected_dates = st.slider(
        "Select Date Range",
        min_value=min_date_date,
        max_value=max_date_date,
        value=(min_date_date, max_date_date),
        format="YYYY-MM-DD"
    )
    
    # Convert back to Timestamp for filtering
    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])
    
    # Filter data
    if regions:
        filtered = delivery_data[
            (delivery_data['Region'].isin(regions)) &
            (delivery_data['Date'] >= start_date) &
            (delivery_data['Date'] <= end_date)
        ]
        
        if not filtered.empty:
            col1, col2 = st.columns(2)
            with col1:
                fig1 = px.line(
                    filtered.groupby('Date')['On-Time Rate'].mean().reset_index(),
                    x='Date',
                    y='On-Time Rate',
                    title='On-Time Rate Trend'
                )
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                fig2 = px.pie(
                    filtered.groupby('Region')['Delayed Deliveries'].sum().reset_index(),
                    names='Region',
                    values='Delayed Deliveries',
                    title='Delay Distribution by Region'
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No data available for the selected filters")
    else:
        st.warning("Please select at least one region")

with tab2:
    # Warehouse selection
    warehouse = st.selectbox(
        "Select Warehouse",
        options=sorted(warehouse_data['Warehouse ID'].unique())
    )
    
    # Filter data
    wh_data = warehouse_data[warehouse_data['Warehouse ID'] == warehouse]
    
    # Visualizations
    if not wh_data.empty:
        fig3 = px.histogram(
            wh_data,
            x=['Average Load Time (mins)', 'Average Unload Time (mins)'],
            barmode='overlay',
            title=f'Processing Times - Warehouse {warehouse}'
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        fig4 = px.scatter(
            warehouse_data,
            x='Average Load Time (mins)',
            y='Average Unload Time (mins)',
            color='Warehouse ID',
            title='All Warehouses Comparison'
        )
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("No data available for selected warehouse")

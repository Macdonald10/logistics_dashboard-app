import pandas as pd
import streamlit as st

def _raw_load_data():
    """Load and validate data without caching"""
    try:
        cost_data = pd.read_csv("cost_breakdown_data.csv")
        delivery_data = pd.read_csv("delivery_performance_data.csv")
        warehouse_data = pd.read_csv("warehouse_turnaround_data.csv")
        shift_data = pd.read_csv("shift_performance_data.csv")
        
        # Convert numeric columns
        numeric_cols = {
            'delivery': ['On-Time Deliveries', 'Delayed Deliveries'],
            'warehouse': ['Average Load Time (mins)', 'Average Unload Time (mins)'],
            'shift': ['Average Deliveries per Shift', 'Idle Time (hours)']
        }
        
        # Convert to numeric and handle errors
        for col in numeric_cols['delivery']:
            delivery_data[col] = pd.to_numeric(delivery_data[col], errors='coerce')
        
        for col in numeric_cols['warehouse']:
            warehouse_data[col] = pd.to_numeric(warehouse_data[col], errors='coerce')
        
        for col in numeric_cols['shift']:
            shift_data[col] = pd.to_numeric(shift_data[col], errors='coerce')
        
        # Calculate on-time rate
        delivery_data["On-Time Rate"] = (
            delivery_data["On-Time Deliveries"] / 
            (delivery_data["On-Time Deliveries"] + delivery_data["Delayed Deliveries"])
        ) * 100
        
        # Convert dates
        if 'Date' in delivery_data.columns:
            delivery_data['Date'] = pd.to_datetime(delivery_data['Date'])
        
        return cost_data, delivery_data, warehouse_data, shift_data
        
    except Exception as e:
        st.error(f"Data loading error: {str(e)}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def load_data():
    """Main function to load data with caching"""
    if 'cached_data' not in st.session_state:
        st.session_state.cached_data = _raw_load_data()
    return st.session_state.cached_data

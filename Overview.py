import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_data

# Page config
st.set_page_config(
    page_title="Dashboard Overview",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .kpi-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    .positive {
        background-color: #d4edda;
        color: #155724;
    }
    .negative {
        background-color: #f8d7da;
        color: #721c24;
    }
    .trend-icon {
        font-size: 1.2rem;
        margin-left: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1 style='text-align: center; margin: 0;'>Logistics Performance Dashboard</h1>
    <p style='text-align: center; margin: 0;'>Real-time supply chain analytics</p>
</div>
""", unsafe_allow_html=True)

# Load data
cost_data, delivery_data, warehouse_data, shift_data = load_data()

# Check if data loaded successfully
if cost_data.empty or delivery_data.empty or warehouse_data.empty or shift_data.empty:
    st.error("Failed to load required data")
    st.stop()

# Data Processing
# Convert month to datetime if needed
if 'Month' in cost_data.columns:
    try:
        cost_data['Month'] = pd.to_datetime(cost_data['Month'])
    except Exception as e:
        st.error(f"Error converting dates: {str(e)}")
        st.stop()

# Calculate KPIs
total_deliveries = delivery_data['On-Time Deliveries'].sum() + delivery_data['Delayed Deliveries'].sum()
on_time_rate = (delivery_data['On-Time Deliveries'].sum() / total_deliveries) * 100 if total_deliveries > 0 else 0
delay_rate = (delivery_data['Delayed Deliveries'].sum() / total_deliveries) * 100 if total_deliveries > 0 else 0

# Cost metrics
total_cost = cost_data['Fuel Cost'].sum() + cost_data['Maintenance Cost'].sum()
cost_per_delivery = total_cost / total_deliveries if total_deliveries > 0 else 0
budget_variance = 0.15  # Example value - would normally come from budget data

# Warehouse metrics
avg_load_time = warehouse_data['Average Load Time (mins)'].mean()
avg_unload_time = warehouse_data['Average Unload Time (mins)'].mean()

# Shift metrics
day_shift_avg = shift_data[shift_data['Shift Type'] == 'Day Shift']['Average Deliveries per Shift'].mean()
night_shift_avg = shift_data[shift_data['Shift Type'] == 'Night Shift']['Average Deliveries per Shift'].mean()
productivity_gap = ((day_shift_avg - night_shift_avg) / day_shift_avg) * 100

# Metrics Section
st.subheader("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

with col1:
    trend = "↑" if on_time_rate > 82 else "↓"
    trend_class = "positive" if on_time_rate > 82 else "negative"
    st.markdown(f"""
    <div class="metric-card">
        <h3>On-Time Delivery</h3>
        <h1>{on_time_rate:.1f}% <span class="kpi-badge {trend_class}">{trend} vs last quarter</span></h1>
        <p>Industry benchmark: 95%</p>
        <p>Target: 90%</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    trend = "↑" if delay_rate < 18 else "↓"
    trend_class = "positive" if delay_rate < 18 else "negative"
    st.markdown(f"""
    <div class="metric-card">
        <h3>Delay Rate</h3>
        <h1>{delay_rate:.1f}% <span class="kpi-badge {trend_class}">{trend} vs last quarter</span></h1>
        <p>Last quarter: 18.2%</p>
        <p>Target: 10%</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Cost per Delivery</h3>
        <h1>${cost_per_delivery:.2f}</h1>
        <p>Budget: ${cost_per_delivery * 0.85:.2f}</p>
        <p>Variance: +15%</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <h3>Warehouse Efficiency</h3>
        <h1>Load: {avg_load_time:.1f} mins</h1>
        <h1>Unload: {avg_unload_time:.1f} mins</h1>
        <p>Target: 60 mins (combined)</p>
    </div>
    """, unsafe_allow_html=True)

# Cost Analysis Section
st.subheader("Cost Breakdown Analysis")

# Calculate cost proportions
cost_data['Total Cost'] = cost_data['Fuel Cost'] + cost_data['Maintenance Cost']
cost_data['Fuel %'] = (cost_data['Fuel Cost'] / cost_data['Total Cost']) * 100
cost_data['Maintenance %'] = (cost_data['Maintenance Cost'] / cost_data['Total Cost']) * 100

tab1, tab2, tab3 = st.tabs(["Trend", "Composition", "Efficiency"])

with tab1:
    fig1 = px.line(
        cost_data,
        x='Month',
        y=['Fuel Cost', 'Maintenance Cost'],
        title='Monthly Operational Costs',
        labels={'value': 'Cost ($)', 'variable': 'Cost Type'}
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.bar(
        cost_data.melt(id_vars=['Month'], 
                     value_vars=['Fuel %', 'Maintenance %']),
        x='Month',
        y='value',
        color='variable',
        title='Cost Composition Over Time',
        labels={'value': 'Percentage (%)', 'variable': 'Cost Type'}
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    # Calculate deliveries per cost
    monthly_deliveries = delivery_data.groupby(delivery_data['Date'].dt.to_period('M'))['On-Time Deliveries'].sum().reset_index()
    monthly_deliveries['Month'] = pd.to_datetime(monthly_deliveries['Date'].astype(str))
    cost_efficiency = pd.merge(cost_data, monthly_deliveries, on='Month')
    cost_efficiency['Deliveries per $1k'] = (cost_efficiency['On-Time Deliveries'] / (cost_efficiency['Total Cost'] / 1000))
    
    fig3 = px.line(
        cost_efficiency,
        x='Month',
        y='Deliveries per $1k',
        title='Operational Efficiency (Deliveries per $1k Spent)',
        markers=True
    )
    st.plotly_chart(fig3, use_container_width=True)

# Performance Benchmarking Section
st.subheader("Performance Benchmarking")

bench_col1, bench_col2 = st.columns(2)

with bench_col1:
    # Warehouse performance comparison
    warehouse_summary = warehouse_data.groupby('Warehouse ID').agg({
        'Average Load Time (mins)': 'mean',
        'Average Unload Time (mins)': 'mean'
    }).reset_index()
    warehouse_summary['Total Processing Time'] = warehouse_summary['Average Load Time (mins)'] + warehouse_summary['Average Unload Time (mins)']
    
    fig4 = px.bar(
        warehouse_summary.sort_values('Total Processing Time'),
        x='Warehouse ID',
        y='Total Processing Time',
        color='Total Processing Time',
        title='Warehouse Efficiency Ranking',
        color_continuous_scale='RdYlGn_r'
    )
    st.plotly_chart(fig4, use_container_width=True)

with bench_col2:
    # Shift productivity comparison
    shift_productivity = shift_data.groupby('Shift Type').agg({
        'Average Deliveries per Shift': 'mean',
        'Idle Time (hours)': 'mean'
    }).reset_index()
    
    fig5 = px.bar(
        shift_productivity,
        x='Shift Type',
        y='Average Deliveries per Shift',
        color='Idle Time (hours)',
        title='Shift Productivity vs Idle Time',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig5, use_container_width=True)

# Alert Section
st.subheader("Priority Alerts")

if delay_rate > 15:
    st.error("""
    🚨 **High Delay Rate Alert**  
    Current delay rate is above 15%. Immediate action recommended in:
    - East region warehouses
    - Night shift scheduling
    """)

if cost_per_delivery > 50:
    st.warning("""
    ⚠️ **Cost Efficiency Warning**  
    Cost per delivery exceeds $50. Focus areas:
    - Fuel consumption optimization
    - Preventive maintenance program
    """)

if productivity_gap > 20:
    st.info("""
    ℹ️ **Productivity Gap Notice**  
    Night shift productivity is significantly lower than day shift. Consider:
    - Shift realignment
    - Additional training
    - Incentive programs
    """)

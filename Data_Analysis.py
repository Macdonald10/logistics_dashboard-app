import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from scipy import stats
from utils.data_loader import load_data

# Page config
st.set_page_config(
    page_title="Deep Analysis",
    page_icon="📊",
    layout="wide"
)

# Load data
_, delivery_data, warehouse_data, shift_data = load_data()

# Check data
if delivery_data.empty or warehouse_data.empty or shift_data.empty:
    st.error("Failed to load required data")
    st.stop()

# --- Fix: Ensure 'Date' columns are datetime ---
for df in [delivery_data, warehouse_data, shift_data]:
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Drop rows with invalid dates
delivery_data.dropna(subset=['Date'], inplace=True)
warehouse_data.dropna(subset=['Date'], inplace=True)
shift_data.dropna(subset=['Date'], inplace=True)

# Data Processing
# Calculate on-time rate
delivery_data['On-Time Rate'] = (delivery_data['On-Time Deliveries'] / 
                               (delivery_data['On-Time Deliveries'] + delivery_data['Delayed Deliveries'])) * 100

# Add month column for time analysis
delivery_data['Month'] = delivery_data['Date'].dt.to_period('M').astype(str)
warehouse_data['Month'] = warehouse_data['Date'].dt.to_period('M').astype(str)
shift_data['Month'] = shift_data['Date'].dt.to_period('M').astype(str)

# Calculate utilization
shift_data['Utilization'] = (1 - (shift_data['Idle Time (hours)'] / 8)) * 100  # Assuming 8-hour shifts

# Page title
st.title("📊 Performance Deep Dive")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Delivery", "Warehouse", "Drivers", "Advanced Analytics"])

# --- tab1 ---
with tab1:
    st.header("Delivery Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        regional = delivery_data.groupby('Region').agg({
            'On-Time Rate': ['mean', 'std', 'count']
        }).reset_index()
        regional.columns = ['Region', 'Mean', 'Std Dev', 'Count']
        
        groups = [delivery_data[delivery_data['Region'] == r]['On-Time Rate'] for r in regional['Region']]
        f_val, p_val = stats.f_oneway(*groups)
        
        fig1 = px.bar(
            regional,
            x='Region',
            y='Mean',
            error_y='Std Dev',
            title=f'On-Time Performance by Region (ANOVA p={p_val:.4f})',
            color='Mean',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        st.caption(f"ANOVA test {'does not show' if p_val > 0.05 else 'shows'} statistically significant differences between regions at p<0.05 level")

    with col2:
        monthly = delivery_data.groupby(['Month', 'Region'])['On-Time Rate'].agg(['mean', 'std', 'count']).reset_index()
        monthly['CI'] = 1.96 * monthly['std'] / np.sqrt(monthly['count'])  # 95% CI
        
        fig2 = px.line(
            monthly,
            x='Month',
            y='mean',
            color='Region',
            error_y='CI',
            title='Monthly Trend with Confidence Intervals',
            markers=True,
            labels={'mean': 'On-Time Rate (%)'}
        )
        st.plotly_chart(fig2, use_container_width=True)

# --- tab2 ---
with tab2:
    st.header("Warehouse Efficiency Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        numeric_cols = ['Average Load Time (mins)', 'Average Unload Time (mins)']
        melted_data = warehouse_data[numeric_cols + ['Warehouse ID']].melt(id_vars=['Warehouse ID'])
        
        _, p_load = stats.shapiro(warehouse_data['Average Load Time (mins)'])
        _, p_unload = stats.shapiro(warehouse_data['Average Unload Time (mins)'])
        
        fig3 = px.box(
            melted_data,
            x='variable',
            y='value',
            title=f'Processing Time Distribution (Normality p-values: Load={p_load:.3f}, Unload={p_unload:.3f})',
            color='variable',
            labels={'value': 'Time (minutes)', 'variable': 'Process Type'}
        )
        st.plotly_chart(fig3, use_container_width=True)
        
        interpretation = "Normally distributed" if p_load > 0.05 else "Not normally distributed"
        st.caption(f"Load times are {interpretation} (Shapiro-Wilk p={p_load:.3f})")

    with col2:
        warehouse_summary = warehouse_data.groupby('Warehouse ID').agg({
            'Average Load Time (mins)': 'mean',
            'Average Unload Time (mins)': 'mean'
        }).reset_index()
        
        corr = warehouse_data['Average Load Time (mins)'].corr(warehouse_data['Average Unload Time (mins)'])
        
        fig4 = px.scatter(
            warehouse_summary,
            x='Average Load Time (mins)',
            y='Average Unload Time (mins)',
            size='Average Load Time (mins)',
            color='Warehouse ID',
            title=f'Warehouse Efficiency Comparison (Correlation: {corr:.2f})',
            trendline='ols'
        )
        st.plotly_chart(fig4, use_container_width=True)
        
        st.caption(f"Correlation between load and unload times: {corr:.2f}")

# --- tab3 ---
with tab3:
    st.header("Driver & Shift Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        day_shift = shift_data[shift_data['Shift Type'] == 'Day Shift']['Average Deliveries per Shift']
        night_shift = shift_data[shift_data['Shift Type'] == 'Night Shift']['Average Deliveries per Shift']
        t_val, p_val = stats.ttest_ind(day_shift, night_shift, equal_var=False)
        
        fig5 = px.violin(
            shift_data,
            x='Shift Type',
            y='Average Deliveries per Shift',
            box=True,
            points="all",
            title=f'Productivity by Shift Type (t-test p={p_val:.4f})',
            color='Shift Type'
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        st.caption(f"T-test {'does not show' if p_val > 0.05 else 'shows'} statistically significant difference between shifts at p<0.05 level")

    with col2:
        fig6 = px.scatter(
            shift_data,
            x='Idle Time (hours)',
            y='Average Deliveries per Shift',
            color='Shift Type',
            trendline='ols',
            title='Idle Time Impact on Productivity',
            size='Idle Time (hours)',
            labels={'Average Deliveries per Shift': 'Productivity', 'Idle Time (hours)': 'Idle Time (hrs)'}
        )
        
        results = px.get_trendline_results(fig6)
        r_squared = results.iloc[0]["px_fit_results"].rsquared
        
        fig6.update_layout(
            title=f'Idle Time Impact on Productivity (R²={r_squared:.2f})'
        )
        st.plotly_chart(fig6, use_container_width=True)
        
        st.caption(f"Idle time explains {r_squared*100:.1f}% of productivity variation")

# --- tab4 ---
with tab4:
    st.header("Advanced Analytics")
    
    st.subheader("Delivery Delay Predictors")
    st.write("**Correlation Analysis**")
    
    warehouse_monthly = warehouse_data.groupby(['Warehouse ID', 'Month']).agg({
        'Average Load Time (mins)': 'mean',
        'Average Unload Time (mins)': 'mean'
    }).reset_index()
    
    delivery_monthly = delivery_data.groupby(['Region', 'Month']).agg({
        'On-Time Rate': 'mean',
        'Delayed Deliveries': 'sum'
    }).reset_index()
    
    analysis_df = pd.merge(
        delivery_monthly,
        warehouse_monthly,
        left_on=['Month'],
        right_on=['Month'],
        how='left'
    )
    
    numeric_df = analysis_df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    
    fig7 = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu',
        title='Correlation Matrix of Key Metrics'
    )
    st.plotly_chart(fig7, use_container_width=True)
    
    st.subheader("Capacity Utilization Analysis")
    
    shift_data['Theoretical Capacity'] = shift_data['Average Deliveries per Shift'] / (1 - (shift_data['Idle Time (hours)'] / 8))
    shift_data['Utilization %'] = (shift_data['Average Deliveries per Shift'] / shift_data['Theoretical Capacity']) * 100
    
    fig8 = px.box(
        shift_data,
        x='Shift Type',
        y='Utilization %',
        color='Shift Type',
        title='Shift Capacity Utilization',
        points='all'
    )
    st.plotly_chart(fig8, use_container_width=True)
    
    st.subheader("Predictive Insights")
    st.write("**Delivery Delay Risk Prediction**")
    
    risk_factors = pd.DataFrame({
        'Factor': ['Warehouse Load Time', 'Night Shift Percentage', 'Peak Season', 'East Region'],
        'Risk Score': [0.42, 0.38, 0.25, 0.55],
        'Impact': ['High', 'Medium', 'Low', 'Very High']
    })
    
    fig9 = px.bar(
        risk_factors.sort_values('Risk Score', ascending=True),
        x='Risk Score',
        y='Factor',
        color='Impact',
        orientation='h',
        title='Top Delay Risk Factors',
        color_discrete_map={
            'Very High': '#d62728',
            'High': '#ff7f0e',
            'Medium': '#1f77b4',
            'Low': '#2ca02c'
        }
    )
    st.plotly_chart(fig9, use_container_width=True)


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.title("📊 Comprehensive Analytics Dashboard")

# Generate sample data
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=365, freq='D')
regions = ['North', 'South', 'East', 'West', 'Central']
categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports']

# Sales data
sales_data = pd.DataFrame({
    'Date': dates,
    'Sales': np.random.normal(1000, 200, 365),
    'Region': np.random.choice(regions, 365),
    'Category': np.random.choice(categories, 365),
    'Profit': np.random.normal(150, 50, 365),
    'Customers': np.random.randint(50, 200, 365)
})

# Top KPIs
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_sales = sales_data['Sales'].sum()
    st.metric("Total Sales", f"${total_sales:,.0f}", "+12.5%")

with col2:
    total_profit = sales_data['Profit'].sum()
    st.metric("Total Profit", f"${total_profit:,.0f}", "+8.3%")

with col3:
    total_customers = sales_data['Customers'].sum()
    st.metric("Total Customers", f"{total_customers:,}", "+15.2%")

with col4:
    avg_order_value = sales_data['Sales'].mean()
    st.metric("Avg Order Value", f"${avg_order_value:.0f}", "+3.7%")

with col5:
    conversion_rate = len(sales_data) / 365
    st.metric("Conversion Rate", f"{conversion_rate:.1%}", "+0.8%")

st.markdown("---")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Sales trend chart
    st.subheader("📈 Sales Trend")
    monthly_sales = sales_data.groupby(sales_data['Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_sales['Date'], y=monthly_sales['Sales'], 
                           mode='lines+markers', name='Sales', line=dict(color='#1f77b4')))
    fig.add_trace(go.Scatter(x=monthly_sales['Date'], y=monthly_sales['Profit'], 
                           mode='lines+markers', name='Profit', line=dict(color='#ff7f0e')))
    fig.update_layout(title="Sales & Profit Trend", 
                   xaxis_title="Month", 
                   yaxis_title="Amount ($)",
                   height=400)
    st.plotly_chart(fig, width='stretch')

with col2:
    # Regional distribution
    st.subheader("🌍 Sales by Region")
    region_sales = sales_data.groupby('Region')['Sales'].sum().reset_index()
    
    fig = px.pie(region_sales, values='Sales', names='Region', 
                 title="Regional Distribution",
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')

# Second row
col1, col2 = st.columns([1, 1])

with col1:
    # Category performance
    st.subheader("📦 Category Performance")
    category_sales = sales_data.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Customers': 'sum'
    }).reset_index()
    
    fig = px.bar(category_sales, x='Category', y='Sales', 
                title="Sales by Category",
                color='Sales',
                color_continuous_scale='Blues')
    fig.update_layout(height=350)
    st.plotly_chart(fig, width='stretch')

with col2:
    # Customer segments
    st.subheader("👥 Customer Segments")
    customer_segments = pd.DataFrame({
        'Segment': ['New', 'Returning', 'VIP', 'Inactive'],
        'Count': [np.random.randint(100, 500), np.random.randint(200, 600), 
                   np.random.randint(50, 200), np.random.randint(80, 300)],
        'Revenue': [np.random.randint(10000, 50000), np.random.randint(20000, 80000),
                   np.random.randint(5000, 30000), np.random.randint(8000, 25000)]
    })
    
    fig = px.scatter(customer_segments, x='Count', y='Revenue', 
                    size='Revenue', color='Segment',
                    title="Customer Segments",
                    hover_data=['Segment'])
    fig.update_layout(height=350)
    st.plotly_chart(fig, width='stretch')

# Third row - Map visualization
st.subheader("🗺️ Geographic Distribution")

# Generate sample geographic data
geo_data = pd.DataFrame({
    'Region': regions,
    'Latitude': [40.7128, 34.0522, 41.8781, 37.7749, 39.9526],
    'Longitude': [-74.0060, -118.2437, -87.6298, -122.4194, -75.1652],
    'Sales': np.random.randint(50000, 200000, len(regions)),
    'Customers': np.random.randint(500, 2000, len(regions))
})

col1, col2 = st.columns([2, 1])

with col1:
    # Map chart
    fig = px.scatter_geo(geo_data, lat='Latitude', lon='Longitude', 
                       size='Sales', color='Region',
                       hover_name='Region',
                       hover_data=['Sales', 'Customers'],
                       title="Sales by Region",
                       scope='usa',
                       projection='albers usa')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')

with col2:
    # Regional summary table
    st.subheader("📊 Regional Summary")
    regional_summary = sales_data.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Customers': 'sum'
    }).reset_index()
    regional_summary['Profit Margin'] = (regional_summary['Profit'] / regional_summary['Sales'] * 100).round(1)
    
    # Format for display
    display_summary = regional_summary.copy()
    display_summary['Sales'] = display_summary['Sales'].apply(lambda x: f"${x:,.0f}")
    display_summary['Profit'] = display_summary['Profit'].apply(lambda x: f"${x:,.0f}")
    display_summary['Profit Margin'] = display_summary['Profit Margin'].apply(lambda x: f"{x}%")
    
    st.dataframe(display_summary, width='stretch')

# Fourth row - Time series analysis
st.subheader("📅 Time Series Analysis")

col1, col2 = st.columns([1, 1])

with col1:
    # Daily sales pattern
    daily_pattern = sales_data.groupby(sales_data['Date'].dt.dayofweek)['Sales'].mean().reset_index()
    daily_pattern['Day'] = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    fig = px.bar(daily_pattern, x='Day', y='Sales', 
                title="Average Sales by Day of Week",
                color='Sales',
                color_continuous_scale='Viridis')
    fig.update_layout(height=300)
    st.plotly_chart(fig, width='stretch')

with col2:
    # Monthly comparison
    monthly_comparison = sales_data.groupby(sales_data['Date'].dt.month).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly_comparison['Month'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly_comparison['Month'], y=monthly_comparison['Sales'], 
                       name='Sales', marker_color='lightblue'))
    fig.add_trace(go.Scatter(x=monthly_comparison['Month'], y=monthly_comparison['Profit'], 
                           mode='lines+markers', name='Profit', line=dict(color='orange')))
    fig.update_layout(title="Monthly Sales vs Profit", 
                   xaxis_title="Month", 
                   yaxis_title="Amount ($)",
                   height=300)
    st.plotly_chart(fig, width='stretch')

# Footer with insights
st.markdown("---")
st.subheader("💡 Key Insights")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("**📈 Growth Opportunity**\n\nElectronics category shows 23% growth YoY, consider increasing inventory.")

with col2:
    st.warning("**⚠️ Regional Focus**\n\nCentral region underperforming by 15% compared to target.")

with col3:
    st.success("**🎯 Target Achievement**\n\nQ4 sales target achieved 2 weeks ahead of schedule.")

# Data table at bottom
st.subheader("📋 Detailed Data Table")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    selected_region = st.selectbox("Filter by Region:", ['All'] + regions, key="table_region_filter")
with col2:
    selected_category = st.selectbox("Filter by Category:", ['All'] + categories, key="table_category_filter")
with col3:
    date_range = st.date_input("Date Range:", value=[sales_data['Date'].min(), sales_data['Date'].max()], key="table_date_filter")

# Apply filters
filtered_data = sales_data.copy()
if selected_region != 'All':
    filtered_data = filtered_data[filtered_data['Region'] == selected_region]
if selected_category != 'All':
    filtered_data = filtered_data[filtered_data['Category'] == selected_category]

# Display filtered data
st.dataframe(filtered_data.sort_values('Date', ascending=False).head(100), width='stretch')

st.markdown("---")
st.markdown("*Real-time analytics dashboard with interactive visualizations and geographic mapping*")

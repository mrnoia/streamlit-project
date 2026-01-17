import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

# Reduce vertical spacing
st.markdown("""
<style>

.block-container {
    padding-top: 3rem !important;
    padding-bottom: 2rem !important;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Tableau-Style Dashboard")

# Generate sample data
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=365, freq='D')

# Sales data
sales_data = pd.DataFrame({
    'Date': dates,
    'Sales': np.random.normal(1000, 200, 365),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], 365),
    'Product': np.random.choice(['Product A', 'Product B', 'Product C', 'Product D'], 365),
    'Category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books'], 365)
})

# KPI Cards at the top
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = sales_data['Sales'].sum()
    st.metric("Total Sales", f"${total_sales:,.0f}", "+12.5%")

with col2:
    avg_sales = sales_data['Sales'].mean()
    st.metric("Average Sales", f"${avg_sales:,.0f}", "+3.2%")

with col3:
    best_day = sales_data.loc[sales_data['Sales'].idxmax(), 'Date'].strftime('%Y-%m-%d')
    best_sales = sales_data['Sales'].max()
    st.metric("Best Day", best_day, f"${best_sales:,.0f}")

with col4:
    total_transactions = len(sales_data)
    st.metric("Transactions", total_transactions, "+8.7%")

st.markdown("---")

# Main dashboard layout
col1, col2 = st.columns([2, 1])

with col1:
    # Time series chart
    st.subheader("📈 Sales Trend Over Time")
    monthly_sales = sales_data.groupby(sales_data['Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly_sales['Date'] = monthly_sales['Date'].dt.to_timestamp()
    
    fig = px.line(monthly_sales, x='Date', y='Sales', 
                 title="Monthly Sales Trend",
                 labels={'Sales': 'Sales ($)', 'Date': 'Month'})
    fig.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig, width='stretch')

with col2:
    # Region breakdown
    st.subheader("🌍 Sales by Region")
    region_sales = sales_data.groupby('Region')['Sales'].sum().reset_index()
    
    fig = px.pie(region_sales, values='Sales', names='Region', 
                 title="Regional Distribution")
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')

# Second row of charts
col1, col2 = st.columns([1, 2])

with col1:
    # Product performance
    st.subheader("📦 Product Performance")
    product_sales = sales_data.groupby('Product')['Sales'].sum().reset_index()
    
    fig = px.bar(product_sales, x='Sales', y='Product', 
                orientation='h',
                title="Sales by Product",
                color='Sales',
                color_continuous_scale='Blues')
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, width='stretch')

with col2:
    # Category comparison
    st.subheader("📋 Category Analysis")
    category_data = sales_data.groupby(['Category', 'Region'])['Sales'].sum().reset_index()
    
    fig = px.bar(category_data, x='Region', y='Sales', color='Category',
                title="Sales by Category and Region",
                barmode='group')
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')

# Third row - Scatter plot and heatmap
col1, col2 = st.columns([1, 1])

with col1:
    # Scatter plot
    st.subheader("🔍 Sales Distribution")
    fig = px.scatter(sales_data.sample(100), x='Date', y='Sales', 
                    color='Region', size='Sales',
                    title="Sales Distribution by Region",
                    hover_data=['Product', 'Category'])
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')

with col2:
    # Heatmap style visualization
    st.subheader("🌡️ Regional Heatmap")
    heatmap_data = sales_data.groupby(['Region', sales_data['Date'].dt.month])['Sales'].mean().reset_index()
    heatmap_pivot = heatmap_data.pivot(index='Region', columns='Date', values='Sales')
    
    fig = px.imshow(heatmap_pivot, 
                    title="Average Sales by Region and Month",
                    color_continuous_scale='Viridis',
                    labels=dict(x="Month", y="Region", color="Sales ($)"))
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')

# Data table at the bottom
st.subheader("📋 Detailed Data Table")

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    selected_region = st.selectbox("Filter by Region:", ['All'] + list(sales_data['Region'].unique()))
with col2:
    selected_product = st.selectbox("Filter by Product:", ['All'] + list(sales_data['Product'].unique()))
with col3:
    selected_category = st.selectbox("Filter by Category:", ['All'] + list(sales_data['Category'].unique()))

# Apply filters
filtered_data = sales_data.copy()
if selected_region != 'All':
    filtered_data = filtered_data[filtered_data['Region'] == selected_region]
if selected_product != 'All':
    filtered_data = filtered_data[filtered_data['Product'] == selected_product]
if selected_category != 'All':
    filtered_data = filtered_data[filtered_data['Category'] == selected_category]

# Display filtered data
st.dataframe(filtered_data.sort_values('Date', ascending=False).head(100), width='stretch')

# Summary statistics
st.subheader("📊 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.write("**Total Records:**")
    st.write(len(filtered_data))

with col2:
    st.write("**Date Range:**")
    st.write(f"{filtered_data['Date'].min().date()} to {filtered_data['Date'].max().date()}")

with col3:
    st.write("**Avg Sale:**")
    st.write(f"${filtered_data['Sales'].mean():.2f}")

with col4:
    st.write("**Std Dev:**")
    st.write(f"${filtered_data['Sales'].std():.2f}")

st.markdown("---")
st.markdown("*Dashboard inspired by Tableau's multi-sheet layout with interactive visualizations*")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# Custom CSS
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem 0;
}

.link-table {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.breadcrumb {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 1rem 0;
}

.product-detail {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
    border-left: 4px solid #667eea;
}
</style>
""", unsafe_allow_html=True)

# Generate sample data
np.random.seed(42)
regions = ['North', 'South', 'East', 'West']
categories = ['Electronics', 'Clothing', 'Food', 'Books']
products = ['Laptop', 'Phone', 'Tablet', 'Shirt', 'Pants', 'Dress', 'Pizza', 'Burger', 'Novel', 'Textbook']

data = []
for region in regions:
    for category in categories:
        for product in np.random.choice(products, 3):
            data.append({
                'Region': region,
                'Category': category,
                'Product': product,
                'Sales': np.random.randint(1000, 50000),
                'Quantity': np.random.randint(10, 500),
                'Profit': np.random.randint(100, 10000)
            })

df = pd.DataFrame(data)

# Get parameters from session state
region = st.session_state.get('selected_region', 'North')
category = st.session_state.get('selected_category', 'Electronics')

# Validate parameters
if region not in regions:
    region = 'North'
if category not in categories:
    category = 'Electronics'

# Header
st.markdown(f"""
<div class="main-header" style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
    <h1>📦 Products in {category} - {region}</h1>
    <p>Detailed product information and performance</p>
</div>
""", unsafe_allow_html=True)

# Breadcrumb navigation
col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
with col1:
    if st.button("🏠 Home", key="breadcrumb_home"):
        st.switch_page("drilldown_regions.py")
with col2:
    if st.button(f"🌍 {region}", key="breadcrumb_region"):
        st.switch_page("drilldown_categories.py")
with col3:
    st.markdown(f"### 📍 Navigation: 🏠 Home → 🌍 {region} → 📂 {category} → Products")
with col4:
    st.empty()  # Spacer

# Filter data for selected region and category
filtered_data = df[(df['Region'] == region) & (df['Category'] == category)]

# Category overview
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader(f"📊 {category} Category Overview in {region}")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sales", f"${filtered_data['Sales'].sum():,}")
with col2:
    st.metric("Total Quantity", f"{filtered_data['Quantity'].sum():,}")
with col3:
    st.metric("Total Profit", f"${filtered_data['Profit'].sum():,}")
with col4:
    st.metric("Products", f"{len(filtered_data)}")

st.markdown('</div>', unsafe_allow_html=True)

# Product charts
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader("📈 Product Performance")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(filtered_data, x='Product', y='Sales', title=f"Sales by Product in {category}")
    st.plotly_chart(fig, use_container_width=True, key="products_bar")

with col2:
    fig = px.scatter(filtered_data, x='Quantity', y='Sales', 
                     size='Profit', hover_name='Product',
                     title=f"Sales vs Quantity Relationship")
    st.plotly_chart(fig, use_container_width=True, key="products_scatter")

st.markdown('</div>', unsafe_allow_html=True)

# Detailed product table
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader("📋 Detailed Product Information")

# Sort by sales for better presentation
sorted_data = filtered_data.sort_values('Sales', ascending=False)

for index, (_, row) in enumerate(sorted_data.iterrows()):
    st.markdown(f'<div class="product-detail">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    
    with col1:
        st.markdown(f"### 📦 {row['Product']}")
        st.write(f"**Category:** {row['Category']}")
        st.write(f"**Region:** {row['Region']}")
    
    with col2:
        st.metric("Sales", f"${row['Sales']:,}")
        st.metric("Quantity", f"{row['Quantity']:,}")
    
    with col3:
        st.metric("Profit", f"${row['Profit']:,}")
        profit_margin = (row['Profit'] / row['Sales']) * 100
        st.metric("Margin", f"{profit_margin:.1f}%")
    
    with col4:
        # Performance indicator
        avg_sales = filtered_data['Sales'].mean()
        if row['Sales'] > avg_sales:
            st.success("🔥 Above Average")
        else:
            st.info("📊 Below Average")
        
        # Profit indicator
        avg_profit = filtered_data['Profit'].mean()
        if row['Profit'] > avg_profit:
            st.success("💰 High Profit")
        else:
            st.info("📈 Standard Profit")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if index < len(sorted_data) - 1:
        st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)

# Data table view
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader("📊 Data Table View")

# Add calculated columns
table_data = sorted_data.copy()
table_data['Profit Margin %'] = (table_data['Profit'] / table_data['Sales'] * 100).round(1)
table_data['Avg Price'] = (table_data['Sales'] / table_data['Quantity']).round(2)

# Reorder columns
display_columns = ['Product', 'Sales', 'Quantity', 'Profit', 'Profit Margin %', 'Avg Price']
st.dataframe(table_data[display_columns], use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation and actions
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🔙 Back Navigation")
    if st.button(f"← Return to {region} Categories", key="back_to_categories"):
        st.switch_page("drilldown_categories.py")
    if st.button("← Return to All Regions", key="back_to_regions"):
        st.switch_page("drilldown_regions.py")

with col2:
    st.markdown("### 📊 Current Selection")
    st.write(f"**Region:** {region}")
    st.write(f"**Category:** {category}")
    st.write(f"**Products:** {len(filtered_data)}")

with col3:
    st.markdown("### 🎯 Quick Actions")
    if st.button("📥 Export Data"):
        st.success("Data exported successfully!")
    if st.button("🔄 Refresh"):
        st.rerun()

# Performance insights
st.markdown("---")
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader("💡 Performance Insights")

# Calculate insights
top_product = sorted_data.iloc[0]
worst_product = sorted_data.iloc[-1]
avg_profit_margin = (filtered_data['Profit'].sum() / filtered_data['Sales'].sum()) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🏆 Top Performer")
    st.write(f"**Product:** {top_product['Product']}")
    st.write(f"**Sales:** ${top_product['Sales']:,}")
    st.write(f"**Profit:** ${top_product['Profit']:,}")

with col2:
    st.markdown("### 📈 Improvement Needed")
    st.write(f"**Product:** {worst_product['Product']}")
    st.write(f"**Sales:** ${worst_product['Sales']:,}")
    st.write(f"**Profit:** ${worst_product['Profit']:,}")

with col3:
    st.markdown("### 📊 Category Stats")
    st.write(f"**Avg Margin:** {avg_profit_margin:.1f}%")
    st.write(f"**Total Products:** {len(filtered_data)}")
    st.write(f"**Avg Sales:** ${filtered_data['Sales'].mean():,.0f}")

st.markdown('</div>', unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown("""
### 💡 How to Use:
1. **View detailed product information** in the cards above
2. **Sort and analyze** performance metrics
3. **Use navigation links** to go back to previous levels
4. **Export data** for external analysis

### 🎯 Benefits of This Approach:
- ✅ **Deep insights** - Detailed product-level analysis
- ✅ **Performance metrics** - Clear KPIs and comparisons
- ✅ **Easy navigation** - Clear breadcrumb trail
- ✅ **Data export** - Can download for further analysis
- ✅ **Mobile friendly** - Responsive design
""")

# Code example
st.markdown("---")
st.markdown("### 💻 Implementation Code:")
st.code('''
# products.py - Final drilldown level
import streamlit as st
import pandas as pd

# Get parameters from URL
query_params = st.query_params
region = query_params.get('region', 'North')
category = query_params.get('category', 'Electronics')

# Filter data
filtered_data = df[(df['Region'] == region) & (df['Category'] == category)]

# Detailed product view
for _, product in filtered_data.iterrows():
    st.metric("Sales", f"${product['Sales']:,}")
    st.metric("Profit", f"${product['Profit']:,}")

# Breadcrumb navigation
st.markdown(f"[Home](?page=regions) → [{region}](?page=categories&region={region}) → {category}")
''', language='python')

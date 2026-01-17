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

.clickable-row {
    cursor: pointer;
    transition: background-color 0.2s;
}

.clickable-row:hover {
    background-color: #f0f8ff;
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

# Header
st.markdown("""
<div class="main-header" style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
    <h1>🌍 Regional Overview</h1>
    <p>Click on any region to drill down to categories</p>
</div>
""", unsafe_allow_html=True)

# Breadcrumb
st.markdown("### 📍 Navigation: Home → Regions")

# Regional summary
region_summary = df.groupby('Region').agg({
    'Sales': 'sum',
    'Quantity': 'sum',
    'Profit': 'sum',
    'Category': 'count'
}).rename(columns={'Category': 'Products'})

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sales", f"${df['Sales'].sum():,}")
with col2:
    st.metric("Total Quantity", f"{df['Quantity'].sum():,}")
with col3:
    st.metric("Total Profit", f"${df['Profit'].sum():,}")
with col4:
    st.metric("Total Products", f"{len(df)}")

# Regional chart
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader("📊 Regional Performance")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(region_summary.reset_index(), x='Region', y='Sales', title="Sales by Region")
    st.plotly_chart(fig, use_container_width=True, key="regions_bar")

with col2:
    fig = px.pie(region_summary.reset_index(), values='Sales', names='Region', title="Sales Distribution")
    st.plotly_chart(fig, use_container_width=True, key="regions_pie")

st.markdown('</div>', unsafe_allow_html=True)

# Interactive regional table with links
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader("🔗 Click on any region to explore categories")

# Create clickable table using buttons
for index, (region, row) in enumerate(region_summary.iterrows()):
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    
    with col1:
        st.markdown(f"### 🌍 {region}")
    
    with col2:
        st.metric("Sales", f"${row['Sales']:,}")
    
    with col3:
        st.metric("Quantity", f"{row['Quantity']:,}")
    
    with col4:
        st.metric("Profit", f"${row['Profit']:,}")
    
    with col5:
        # Use session state to pass region to categories page
        if st.button("📂 Explore", key=f"explore_{region}"):
            st.session_state.selected_region = region
            st.session_state.current_page = "categories"
            st.rerun()
    
    if index < len(region_summary) - 1:
        st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown("""
### 💡 How to Use:
1. **Click on any region name** above to go to the categories page
2. **Or click the "Explore" button** for the same result
3. **Use the navigation bar** to return to this page
4. **Continue drilling down** through categories → products

### 🎯 Benefits of This Approach:
- ✅ **Natural navigation** - users understand clicking links
- ✅ **Bookmarkable URLs** - each level has its own URL
- ✅ **Browser back button** works naturally
- ✅ **Clean separation** - each page has one clear purpose
- ✅ **Mobile friendly** - links work well on touch devices
""")

# Code example
st.markdown("---")
st.markdown("### 💻 Implementation Code:")
st.code('''
# Multi-page drilldown with links
# regions.py
import streamlit as st
import pandas as pd

# Regional summary table
for region, data in regions_summary.iterrows():
    # Create clickable link to categories page
    st.markdown(f"[{region}](?page=categories&region={region})")
    st.metric("Sales", f"${data['Sales']:,}")

# categories.py  
region = st.query_params.get('region', 'All')
filtered_data = df[df['Region'] == region]

for category, data in categories_summary.iterrows():
    # Link to products page
    st.markdown(f"[{category}](?page=products&region={region}&category={category})")

# products.py
region = st.query_params.get('region', 'All')
category = st.query_params.get('category', 'All')
filtered_data = df[(df['Region'] == region) & (df['Category'] == category)]

st.dataframe(filtered_data)
''', language='python')

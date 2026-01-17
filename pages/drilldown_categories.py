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

# Get region from session state
region = st.session_state.get('selected_region', 'North')

if region not in regions:
    region = 'North'

# Header
st.markdown(f"""
<div class="main-header" style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
    <h1>📂 Categories in {region} Region</h1>
    <p>Click on any category to see products</p>
</div>
""", unsafe_allow_html=True)

# Breadcrumb navigation
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("🏠 Home", key="breadcrumb_home"):
        st.switch_page("drilldown_regions.py")
with col2:
    st.markdown(f"### 📍 Navigation: 🏠 Home → {region} Region → Categories")
with col3:
    st.empty()  # Spacer

# Filter data for selected region
region_data = df[df['Region'] == region]

# Category summary
category_summary = region_data.groupby('Category').agg({
    'Sales': 'sum',
    'Quantity': 'sum',
    'Profit': 'sum',
    'Product': 'count'
}).rename(columns={'Product': 'Products'})

# Region overview
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader(f"🌍 {region} Region Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sales", f"${region_data['Sales'].sum():,}")
with col2:
    st.metric("Total Quantity", f"{region_data['Quantity'].sum():,}")
with col3:
    st.metric("Total Profit", f"${region_data['Profit'].sum():,}")
with col4:
    st.metric("Categories", f"{len(category_summary)}")

st.markdown('</div>', unsafe_allow_html=True)

# Category chart
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader("📊 Category Performance")

col1, col2 = st.columns(2)
with col1:
    fig = px.bar(category_summary.reset_index(), x='Category', y='Sales', title=f"Sales by Category in {region}")
    st.plotly_chart(fig, use_container_width=True, key="categories_bar")

with col2:
    fig = px.pie(category_summary.reset_index(), values='Sales', names='Category', title=f"Category Distribution in {region}")
    st.plotly_chart(fig, use_container_width=True, key="categories_pie")

st.markdown('</div>', unsafe_allow_html=True)

# Interactive category table with links
st.markdown('<div class="link-table">', unsafe_allow_html=True)
st.subheader("🔗 Click on any category to explore products")

# Create clickable table using buttons
for index, (category, row) in enumerate(category_summary.iterrows()):
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    
    with col1:
        st.markdown(f"### 📂 {category}")
    
    with col2:
        st.metric("Sales", f"${row['Sales']:,}")
    
    with col3:
        st.metric("Quantity", f"{row['Quantity']:,}")
    
    with col4:
        st.metric("Products", f"{row['Products']:,}")
    
    with col5:
        # Use session state to pass category to products page
        if st.button("📦 Explore", key=f"explore_{category}"):
            st.session_state.selected_region = region
            st.session_state.selected_category = category
            st.switch_page("drilldown_products.py")
    
    if index < len(category_summary) - 1:
        st.markdown("---")

st.markdown('</div>', unsafe_allow_html=True)

# Navigation buttons
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔙 Back Navigation")
    if st.button("← Return to Regions", key="back_to_regions"):
        st.switch_page("drilldown_regions.py")

with col2:
    st.markdown("### 📊 Quick Stats")
    st.write(f"**Region:** {region}")
    st.write(f"**Categories:** {len(category_summary)}")
    st.write(f"**Total Products:** {len(region_data)}")

# Instructions
st.markdown("---")
st.markdown("""
### 💡 How to Use:
1. **Click on any category name** above to go to the products page
2. **Or click the "Explore" button** for the same result
3. **Use the breadcrumb navigation** to go back to regions
4. **Continue drilling down** to see individual products

### 🎯 Benefits of This Approach:
- ✅ **Clear hierarchy** - Users always know where they are
- ✅ **Easy navigation** - Simple links and breadcrumbs
- ✅ **Bookmarkable URLs** - Each level has unique URL
- ✅ **Browser back button** works naturally
- ✅ **Mobile friendly** - Touch-friendly links
""")

# Code example
st.markdown("---")
st.markdown("### 💻 Implementation Code:")
st.code('''
# categories.py - Multi-page drilldown
import streamlit as st
import pandas as pd

# Get parameters from URL
query_params = st.query_params
region = query_params.get('region', 'North')

# Filter data
region_data = df[df['Region'] == region]
category_summary = region_data.groupby('Category').sum()

# Create clickable links to products
for category, data in category_summary.iterrows():
    st.markdown(f"[{category}](?page=products&region={region}&category={category})")
    st.metric("Sales", f"${data['Sales']:,}")

# Breadcrumb navigation
st.markdown(f"[Home](?page=regions) → {region} → Categories")
''', language='python')

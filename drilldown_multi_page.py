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

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'regions'
if 'selected_region' not in st.session_state:
    st.session_state.selected_region = 'North'
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = 'Electronics'

# Get current page from session state
current_page = st.session_state.current_page
selected_region = st.session_state.selected_region
selected_category = st.session_state.selected_category

# Header based on current page
if current_page == 'regions':
    st.markdown("""
    <div class="main-header" style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>🌍 Regional Overview</h1>
        <p>Click on any region to drill down to categories</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Breadcrumb
    st.markdown("📍 Navigation: 🏠 Home → Regions")
    
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

    # Interactive regional table
    st.markdown('<div class="link-table">', unsafe_allow_html=True)
    st.subheader("🔗 Click on any region to explore categories")

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
            if st.button("📂 Explore", key=f"explore_{region}"):
                st.session_state.selected_region = region
                st.session_state.current_page = 'categories'
                st.rerun()
        
        if index < len(region_summary) - 1:
            st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == 'categories':
    st.markdown(f"""
    <div class="main-header" style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>📂 Categories in {selected_region} Region</h1>
        <p>Click on any category to see products</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Breadcrumb navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🏠 Home", key="breadcrumb_home"):
            st.session_state.current_page = 'regions'
            st.rerun()
    with col2:
        st.markdown(f"📍 Navigation: 🏠 Home → {selected_region} Region → Categories")
    with col3:
        st.empty()

    # Filter data for selected region
    region_data = df[df['Region'] == selected_region]
    category_summary = region_data.groupby('Category').agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Profit': 'sum',
        'Product': 'count'
    }).rename(columns={'Product': 'Products'})

    # Category overview
    st.markdown('<div class="link-table">', unsafe_allow_html=True)
    st.subheader(f"🌍 {selected_region} Region Overview")

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
        fig = px.bar(category_summary.reset_index(), x='Category', y='Sales', title=f"Sales by Category in {selected_region}")
        st.plotly_chart(fig, use_container_width=True, key="categories_bar")

    with col2:
        fig = px.pie(category_summary.reset_index(), values='Sales', names='Category', title=f"Category Distribution in {selected_region}")
        st.plotly_chart(fig, use_container_width=True, key="categories_pie")

    st.markdown('</div>', unsafe_allow_html=True)

    # Interactive category table
    st.markdown('<div class="link-table">', unsafe_allow_html=True)
    st.subheader("🔗 Click on any category to explore products")

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
            if st.button("📦 Explore", key=f"explore_{category}"):
                st.session_state.selected_category = category
                st.session_state.current_page = 'products'
                st.rerun()
        
        if index < len(category_summary) - 1:
            st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)

elif current_page == 'products':
    st.markdown(f"""
    <div class="main-header" style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
        <h1>📦 Products in {selected_category} - {selected_region}</h1>
        <p>Detailed product information and performance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Breadcrumb navigation
    col1, col2, col3, col4 = st.columns([1, 1, 2, 1])
    with col1:
        if st.button("🏠 Home", key="breadcrumb_home"):
            st.session_state.current_page = 'regions'
            st.rerun()
    with col2:
        if st.button(f"🌍 {selected_region}", key="breadcrumb_region"):
            st.session_state.current_page = 'categories'
            st.rerun()
    with col3:
        st.markdown(f"📍 Navigation: 🏠 Home → 🌍 {selected_region} → 📂 {selected_category} → Products")
    with col4:
        st.empty()

    # Filter data for selected region and category
    filtered_data = df[(df['Region'] == selected_region) & (df['Category'] == selected_category)]

    # Category overview
    st.markdown('<div class="link-table">', unsafe_allow_html=True)
    st.subheader(f"📊 {selected_category} Category Overview in {selected_region}")

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
        fig = px.bar(filtered_data, x='Product', y='Sales', title=f"Sales by Product in {selected_category}")
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
        st.markdown(f'<div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid #667eea;">', unsafe_allow_html=True)
        
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
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if index < len(sorted_data) - 1:
            st.markdown("---")

    st.markdown('</div>', unsafe_allow_html=True)

# Instructions
st.markdown("---")
st.markdown("""
### 💡 How to Use:
1. **Start at Regions** - See overview of all regions
2. **Click "📂 Explore"** - Go to categories for selected region
3. **Click "📦 Explore"** - Go to products for selected category
4. **Use breadcrumb navigation** - Click any level to go back

### 🎯 Benefits of This Approach:
- ✅ **Single page** - No navigation issues
- ✅ **Session state** - Maintains context
- ✅ **Fast navigation** - Instant page switching
- ✅ **Mobile friendly** - Touch-friendly buttons
- ✅ **Professional design** - Clean and intuitive
""")

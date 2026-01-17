import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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

.filter-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 1rem 0;
}

.drilldown-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header" style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 10px; color: white; text-align: center; margin-bottom: 2rem;">
    <h1>🔍 Streamlit-Friendly Data Exploration</h1>
    <p>Modern approaches to data exploration in Streamlit</p>
</div>
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

# Method 1: Filter-Based Approach (Most Streamlit-Friendly)
st.header("🎯 Method 1: Filter-Based Exploration")
st.markdown("*The most Streamlit-native approach - use filters instead of drilldowns*")

st.markdown('<div class="filter-section">', unsafe_allow_html=True)

# Multi-level filters
col1, col2, col3 = st.columns(3)

with col1:
    selected_region = st.selectbox("🌍 Select Region", ['All'] + regions, key="filter_region")

with col2:
    if selected_region != 'All':
        available_categories = df[df['Region'] == selected_region]['Category'].unique()
        selected_category = st.selectbox("📂 Select Category", ['All'] + list(available_categories), key="filter_category")
    else:
        selected_category = 'All'
        st.selectbox("📂 Select Category", ['All'], disabled=True, key="filter_category_disabled")

with col3:
    if selected_category != 'All' and selected_region != 'All':
        available_products = df[(df['Region'] == selected_region) & (df['Category'] == selected_category)]['Product'].unique()
        selected_product = st.selectbox("📦 Select Product", ['All'] + list(available_products), key="filter_product")
    else:
        selected_product = 'All'
        st.selectbox("📦 Select Product", ['All'], disabled=True, key="filter_product_disabled")

st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]
if selected_product != 'All':
    filtered_df = filtered_df[filtered_df['Product'] == selected_product]

# Display results
st.markdown('<div class="drilldown-card">', unsafe_allow_html=True)

# Current selection breadcrumb
st.markdown("### 📍 Current Selection:")
breadcrumb_parts = []
if selected_region != 'All':
    breadcrumb_parts.append(f"🌍 {selected_region}")
if selected_category != 'All':
    breadcrumb_parts.append(f"📂 {selected_category}")
if selected_product != 'All':
    breadcrumb_parts.append(f"📦 {selected_product}")

if breadcrumb_parts:
    st.markdown(" → ".join(breadcrumb_parts))
else:
    st.markdown("🌍 All Data")

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Sales", f"${filtered_df['Sales'].sum():,}", f"+{np.random.randint(5, 25)}%")
with col2:
    st.metric("Total Quantity", f"{filtered_df['Quantity'].sum():,}", f"+{np.random.randint(3, 15)}%")
with col3:
    st.metric("Total Profit", f"${filtered_df['Profit'].sum():,}", f"+{np.random.randint(8, 30)}%")
with col4:
    st.metric("Items", f"{len(filtered_df)}", f"+{np.random.randint(1, 10)}")

# Charts
col1, col2 = st.columns(2)

with col1:
    if selected_product != 'All':
        # Product detail view
        product_data = filtered_df.groupby('Product')[['Sales', 'Quantity', 'Profit']].sum().reset_index()
        fig = px.bar(product_data, x='Product', y='Sales', title=f"Sales by {selected_category}")
        st.plotly_chart(fig, use_container_width=True, key="product_detail_chart")
    elif selected_category != 'All':
        # Category view
        category_data = filtered_df.groupby('Product')[['Sales', 'Quantity', 'Profit']].sum().reset_index()
        fig = px.bar(category_data, x='Product', y='Sales', title=f"Products in {selected_category}")
        st.plotly_chart(fig, use_container_width=True, key="category_chart")
    else:
        # Region view
        region_data = filtered_df.groupby('Region')[['Sales', 'Quantity', 'Profit']].sum().reset_index()
        fig = px.pie(region_data, values='Sales', names='Region', title="Sales by Region")
        st.plotly_chart(fig, use_container_width=True, key="region_pie_chart")

with col2:
    # Trend chart
    if len(filtered_df) > 0:
        fig = px.scatter(filtered_df, x='Quantity', y='Sales', 
                        color='Category' if selected_category == 'All' else 'Product',
                        title="Sales vs Quantity Relationship")
        st.plotly_chart(fig, use_container_width=True, key="trend_chart")

# Data table
st.subheader("📊 Data Table")
st.dataframe(filtered_df, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Code example
st.markdown("---")
st.markdown("### 💻 Code for Filter-Based Approach:")
st.code('''
# Filter-based exploration (Streamlit-friendly)
col1, col2, col3 = st.columns(3)

with col1:
    region = st.selectbox("Region", ['All'] + regions)

with col2:
    if region != 'All':
        category = st.selectbox("Category", ['All'] + categories)
    else:
        category = 'All'

with col3:
    if category != 'All':
        product = st.selectbox("Product", ['All'] + products)
    else:
        product = 'All'

# Apply filters
filtered_df = df.copy()
if region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == region]
if category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == category]
if product != 'All':
    filtered_df = filtered_df[filtered_df['Product'] == product]

# Display results
st.dataframe(filtered_df)
''', language='python')

st.markdown("---")

# Method 2: Tab-Based Exploration
st.header("📑 Method 2: Tab-Based Exploration")
st.markdown("*Use tabs to organize different levels of data*")

tab1, tab2, tab3, tab4 = st.tabs(["🌍 Regions", "📂 Categories", "📦 Products", "📈 Analytics"])

with tab1:
    st.markdown('<div class="drilldown-card">', unsafe_allow_html=True)
    st.subheader("Regional Overview")
    
    region_summary = df.groupby('Region')[['Sales', 'Quantity', 'Profit']].sum().reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(region_summary, x='Region', y='Sales', title="Sales by Region")
        st.plotly_chart(fig, use_container_width=True, key="tab_region_bar")
    
    with col2:
        fig = px.pie(region_summary, values='Profit', names='Region', title="Profit Distribution")
        st.plotly_chart(fig, use_container_width=True, key="tab_region_pie")
    
    st.dataframe(region_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="drilldown-card">', unsafe_allow_html=True)
    st.subheader("Category Analysis")
    
    category_summary = df.groupby('Category')[['Sales', 'Quantity', 'Profit']].sum().reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(category_summary, x='Category', y='Sales', title="Sales by Category")
        st.plotly_chart(fig, use_container_width=True, key="tab_category_bar")
    
    with col2:
        fig = px.sunburst(df, path=['Region', 'Category'], values='Sales', title="Category Distribution")
        st.plotly_chart(fig, use_container_width=True, key="tab_category_sunburst")
    
    st.dataframe(category_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="drilldown-card">', unsafe_allow_html=True)
    st.subheader("Product Details")
    
    product_summary = df.groupby(['Category', 'Product'])[['Sales', 'Quantity', 'Profit']].sum().reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.treemap(product_summary, path=['Category', 'Product'], values='Sales', title="Product Sales Hierarchy")
        st.plotly_chart(fig, use_container_width=True, key="tab_product_treemap")
    
    with col2:
        top_products = product_summary.nlargest(10, 'Sales')
        fig = px.bar(top_products, x='Product', y='Sales', title="Top 10 Products")
        st.plotly_chart(fig, use_container_width=True, key="tab_product_bar")
    
    st.dataframe(product_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="drilldown-card">', unsafe_allow_html=True)
    st.subheader("Advanced Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        # Correlation heatmap
        corr_data = df[['Sales', 'Quantity', 'Profit']].corr()
        fig = px.imshow(corr_data, text_auto=True, aspect="auto", title="Correlation Matrix")
        st.plotly_chart(fig, use_container_width=True, key="tab_analytics_heatmap")
    
    with col2:
        # Performance distribution
        fig = px.histogram(df, x='Sales', color='Region', title="Sales Distribution by Region")
        st.plotly_chart(fig, use_container_width=True, key="tab_analytics_histogram")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Code for tab-based approach
st.markdown("---")
st.markdown("### 💻 Code for Tab-Based Approach:")
st.code('''
# Tab-based exploration
tab1, tab2, tab3 = st.tabs(["Overview", "Details", "Analytics"])

with tab1:
    st.subheader("High-level view")
    st.dataframe(summary_data)

with tab2:
    st.subheader("Detailed analysis")
    st.dataframe(detailed_data)

with tab3:
    st.subheader("Advanced analytics")
    st.plotly_chart(analytics_chart)
''', language='python')

st.markdown("---")

# Method 3: Expandable Sections
st.header("📂 Method 3: Expandable Sections")
st.markdown("*Use nested expanders for hierarchical data*")

st.markdown('<div class="drilldown-card">', unsafe_allow_html=True)

for region in regions:
    with st.expander(f"🌍 {region} Region"):
        region_data = df[df['Region'] == region]
        region_summary = region_data.groupby('Category')[['Sales', 'Quantity', 'Profit']].sum()
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**Total Sales:** ${region_data['Sales'].sum():,}")
            st.write(f"**Total Products:** {len(region_data)}")
        
        with col2:
            fig = px.pie(region_summary.reset_index(), values='Sales', names='Category', title=f"{region} Categories")
            st.plotly_chart(fig, use_container_width=True, key=f"pie_{region}")
        
        for category in region_data['Category'].unique():
            with st.expander(f"📂 {category} in {region}"):
                category_data = region_data[region_data['Category'] == category]
                
                st.dataframe(category_data[['Product', 'Sales', 'Quantity', 'Profit']], use_container_width=True)
                
                # Product chart
                product_summary = category_data.groupby('Product')[['Sales', 'Quantity']].sum().reset_index()
                fig = px.bar(product_summary, x='Product', y='Sales', title=f"Products in {category}")
                st.plotly_chart(fig, use_container_width=True, key=f"bar_{region}_{category}")

st.markdown('</div>', unsafe_allow_html=True)

# Code for expandable approach
st.markdown("---")
st.markdown("### 💻 Code for Expandable Sections:")
st.code('''
# Expandable sections approach
for region in regions:
    with st.expander(f"🌍 {region} Region"):
        region_data = df[df['Region'] == region]
        
        st.write(f"Total Sales: ${region_data['Sales'].sum():,}")
        
        for category in region_data['Category'].unique():
            with st.expander(f"📂 {category}"):
                category_data = region_data[region_data['Category'] == category]
                st.dataframe(category_data)
''', language='python')

st.markdown("---")

# Method 4: Multi-Page Drilldown System
st.header("🔗 Method 4: Multi-Page Drilldown System")
st.markdown("*Use separate pages with button navigation - the most intuitive approach*")

st.markdown('<div class="drilldown-card">', unsafe_allow_html=True)

st.subheader("🌍 How Multi-Page Drilldown Works:")
st.markdown("""
**📑 Three-Level Navigation:**
1. **Regions Page** - Overview of all regions with metrics
2. **Categories Page** - Categories for selected region  
3. **Products Page** - Detailed product information

**🔗 Navigation Features:**
- **Button-based navigation** - Click "Explore" buttons to drill down
- **Breadcrumb navigation** - Click any level to go back
- **Session state** - Maintains context across pages
- **Mobile-friendly** - Touch-friendly buttons

**✅ Benefits:**
- Most intuitive for users
- Bookmarkable URLs
- Browser back button works
- Clean separation of concerns
""")

# Demo buttons to show the multi-page system
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🌍 Start Here")
    st.write("Regional overview with all metrics")
    st.info("👆 Click 'Multi-Page Drilldown' in the top navbar to start")
    st.markdown("**Or navigate manually:**")
    st.markdown("1. Click **🌍 Multi-Page Drilldown** in navbar")
    st.markdown("2. Click **📂 Explore** on any region")
    st.markdown("3. Click **📦 Explore** on any category")

with col2:
    st.markdown("### 📂 Categories")
    st.write("Categories breakdown for selected region")
    st.info("Select a region first, then explore categories")

with col3:
    st.markdown("### 📦 Products")
    st.write("Detailed product information")
    st.info("Select region and category first")

st.markdown('</div>', unsafe_allow_html=True)

# Code example for multi-page approach
st.markdown("---")
st.markdown("### 💻 Code for Multi-Page Drilldown:")
st.code('''
# regions.py - Starting page
if st.button("📂 Explore", key=f"explore_{region}"):
    st.session_state.selected_region = region
    st.switch_page("categories.py")

# categories.py - Middle level
region = st.session_state.get('selected_region', 'North')
if st.button("📦 Explore", key=f"explore_{category}"):
    st.session_state.selected_category = category
    st.switch_page("products.py")

# products.py - Final level
region = st.session_state.get('selected_region', 'North')
category = st.session_state.get('selected_category', 'Electronics')
filtered_data = df[(df['Region'] == region) & (df['Category'] == category)]

# Breadcrumb navigation
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🏠 Home"):
        st.switch_page("regions.py")
with col2:
    if st.button(f"🌍 {region}"):
        st.switch_page("categories.py")
''', language='python')

st.markdown("---")

# Comparison and Recommendations
st.header("🎯 Comparison & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="drilldown-card">', unsafe_allow_html=True)
    st.subheader("✅ Streamlit-Friendly Methods")
    
    st.markdown("""
    **🎯 Filter-Based (Recommended for simple cases)**
    - ✅ Most intuitive for users
    - ✅ Easy to implement
    - ✅ Works with bookmarks
    - ✅ Mobile-friendly
    
    **📑 Tab-Based**
    - ✅ Clear organization
    - ✅ Good for distinct views
    - ✅ Easy navigation
    
    **📂 Expandable Sections**
    - ✅ Hierarchical view
    - ✅ Progressive disclosure
    - ✅ Good for exploration
    
    **🔗 Multi-Page System (Recommended for complex drilldowns)**
    - ✅ Most professional approach
    - ✅ Clean separation of concerns
    - ✅ Bookmarkable URLs
    - ✅ Browser back button works
    - ✅ Best for large datasets
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="drilldown-card">', unsafe_allow_html=True)
    st.subheader("❌ Traditional Drilldown Issues")
    
    st.markdown("""
    **🚫 Why Traditional Drilldowns Fail in Streamlit:**
    
    - No native breadcrumb navigation
    - Complex session state management
    - URL doesn't reflect drilldown state
    - Can't bookmark drilldown levels
    - Back button doesn't work naturally
    - Hard to maintain context
    - Mobile unfriendly
    
    **💡 Better Alternatives:**
    - Use filters instead (for simple cases)
    - Implement tabs (for distinct views)
    - Use expandable sections (for exploration)
    - **Multi-page system** (for complex drilldowns)
    - Consider Power BI/Tableau for complex drilldowns
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
## 🎉 Conclusion

Streamlit offers **four excellent approaches** to data exploration:

- **🎯 Filter-Based** - Best for simple, interactive filtering
- **📑 Tab-Based** - Great for organizing distinct views  
- **📂 Expandable Sections** - Perfect for hierarchical exploration
- **🔗 Multi-Page System** - Ideal for complex drilldowns with clean separation

**Best Practice:** Choose the approach that matches your complexity needs. For complex drilldowns, the **multi-page system** is the most professional and user-friendly solution!
""")

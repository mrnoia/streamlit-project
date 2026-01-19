import streamlit as st

st.set_page_config(layout="wide")

# Custom CSS
st.markdown("""
<style>
.help-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.help-section {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 4px solid #667eea;
}

.code-example {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 5px;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
    overflow-x: auto;
}
</style>
""", unsafe_allow_html=True)

st.title("🦆 DuckDB Dashboard - How Filtering Works")
st.markdown("*Complete guide to understanding the advanced filtering system*")

# Overview
st.markdown('<div class="help-container">', unsafe_allow_html=True)
st.markdown("""
## 🎯 **Quick Overview**

The DuckDB Dashboard uses **dynamic SQL filtering** with **real-time updates** to provide a powerful, responsive data exploration experience.

### 📊 **What You Can Filter:**
- 📅 **Date Range** - Filter transactions by time period
- 🌍 **Regions** - Select one or more geographic areas  
- 📦 **Categories** - Choose product categories to analyze
- 🛍️ **Products** - Filter by specific products (depends on categories)
- 💰 **Sales Amount** - Set minimum/maximum transaction values
- 📦 **Quantity** - Filter by transaction volume

### ⚡ **How It Works:**
1. **Select filters** in sidebar → **Page automatically refreshes**
2. **DuckDB executes** optimized SQL queries → **Results update instantly**
3. **Charts and data** update to reflect your selections
4. **All components** stay synchronized with your filter choices
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Detailed Filtering Process
st.subheader("🔍 Step-by-Step Filtering Process")

st.markdown('<div class="help-section">', unsafe_allow_html=True)
st.markdown("""
### 1️⃣ **Category Selection - The Smart Filter**

When you select categories in the sidebar, here's what happens:

#### 📝 **Code Behind It:**
```python
# Get available categories
categories = conn.execute("SELECT DISTINCT category FROM sales ORDER BY category").fetchall()

# Show multiselect widget
selected_categories = st.sidebar.multiselect(
    "📦 Categories",
    options=[c[0] for c in categories],
    default=[c[0] for c in categories],  # All selected by default
    key="category_filter"
)
```

#### 🔄 **What Happens When You Click:**

1. **Streamlit detects** your selection change
2. **Page automatically reruns** with new filter values
3. **Product filter updates** to show only products from your selected categories
4. **All queries rebuild** with your new category selection

#### 💡 **Smart Dependencies:**
- **Product filter is hidden** when no categories selected
- **Product options change** based on your category choices
- **Real-time updates** - No manual refresh needed
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="help-section">', unsafe_allow_html=True)
st.markdown("""
### 2️⃣ **Dynamic WHERE Clause Building**

The dashboard builds SQL queries dynamically based on your selections:

#### 📋 **Filter Combination Example:**
```python
# Build WHERE conditions
where_conditions = []
params = []

if selected_categories:
    where_conditions.append(f"category IN ({','.join(['?' for _ in selected_categories])})")
    params.extend(selected_categories)

if selected_regions:
    where_conditions.append(f"region IN ({','.join(['?' for _ in selected_regions])})")
    params.extend(selected_regions)

# Final WHERE clause
where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
```

#### 🎯 **Generated SQL:**
```sql
SELECT date, region, category, product, quantity, unit_price, discount, sales_amount
FROM sales
WHERE date BETWEEN '2024-01-01' AND '2024-12-31'
  AND region IN ('North', 'South')
  AND category IN ('Electronics', 'Clothing')
  AND sales_amount BETWEEN 0 AND 10000
  AND quantity BETWEEN 1 AND 100
```

#### ⚡ **Performance Benefits:**
- **Single query execution** - All filters applied in one database call
- **Parameterized queries** - Secure and efficient SQL
- **Automatic optimization** - DuckDB processes only matching data
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="help-section">', unsafe_allow_html=True)
st.markdown("""
### 3️⃣ **Real-Time Updates and Performance**

#### 🔄 **Automatic Page Refreshes:**
- **Every filter change** triggers `st.rerun()`
- **Session state management** - Preserves filter values
- **Instant visual feedback** - Charts update immediately

#### 🧠 **Memory Efficiency:**
- **In-memory database** - All data stored in RAM
- **Columnar Parquet format** - Efficient data storage
- **Smart query optimization** - Only processes needed columns

#### 📊 **Chart Synchronization:**
- **All visualizations** update with your filters
- **Consistent data view** - Charts and tables show same filtered data
- **Interactive exploration** - Smooth drilling down into data
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Technical Implementation
st.subheader("💻 Technical Implementation")

st.markdown('<div class="code-example">', unsafe_allow_html=True)
st.markdown('''
#### 🗄️ **DuckDB Connection Setup:**
```python
@st.cache_resource
def get_duckdb_connection():
    conn = duckdb.connect(":memory:")
    conn.execute("INSTALL httpfs")
    conn.execute("LOAD httpfs")
    return conn
```

#### 📂 **Parquet Data Loading:**
```python
# Load data from Parquet file
conn.execute(f"""
    CREATE OR REPLACE TABLE sales AS 
    SELECT * FROM read_parquet('{parquet_path}')
""")
```

#### 🔍 **Dynamic Query Building:**
```python
# Build parameterized WHERE clause
def build_where_clause(filters):
    conditions = []
    params = []
    
    if filters['categories']:
        conditions.append("category IN ({})".format(
            ','.join(['?' for _ in filters['categories']])
        ))
        params.extend(filters['categories'])
    
    return " AND ".join(conditions), params
```

#### ⚡ **Query Execution:**
```python
# Execute with parameters
filtered_data = conn.execute(query, params).fetchdf()
```
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Tips and Best Practices
st.subheader("💡 Pro Tips")

st.markdown('<div class="help-section">', unsafe_allow_html=True)
st.markdown("""
#### 🎯 **Filtering Best Practices:**

1. **Start Broad, Then Narrow** - Begin with all data, then apply specific filters
2. **Use Date Ranges** - Time-based filtering is very powerful for trend analysis
3. **Combine Filters** - Use multiple filters together for precise insights
4. **Check Memory Usage** - Monitor the "🧠 Memory Usage" metric for performance

#### 🔧 **Keyboard Shortcuts:**
- **Tab key** - Navigate between filter widgets
- **Shift + Click** - Select multiple items quickly
- **Ctrl/Cmd + Enter** - Apply filter changes

#### 📊 **Data Exploration Workflow:**
1. **Filter by Date** → See temporal patterns
2. **Add Region Filter** → Compare geographic performance  
3. **Select Categories** → Focus on specific product types
4. **Apply Product Filter** → Drill down to specific items
5. **Export Results** → Download filtered data for further analysis
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation Help
st.subheader("🧭 Navigation Guide")

st.markdown('<div class="help-section">', unsafe_allow_html=True)
st.markdown("""
#### 📱 **Getting Around the Dashboard:**

- **📚 Streamlit Tutorial** - Learn all available components and features
- **🦆 DuckDB Dashboard** - Return here for filtering help and data exploration
- **📈 Tableau Dashboard** - Professional visual analytics with different style
- **📉 Analytics Dashboard** - Advanced business intelligence with code examples
- **🧩 UI Components** - Interactive widget demonstrations
- **🔍 Drilldown Demo** - Compare different data exploration approaches
- **🌍 Multi-Page Drilldown** - Advanced navigation system with breadcrumbs

#### 🎯 **Recommended Learning Path:**
1. **Start with Tutorial** → Understand all components
2. **Try DuckDB Dashboard** → Experience advanced filtering
3. **Explore Other Dashboards** → See different visualization styles
4. **Check Components Demo** → Learn specific widget implementations
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("*This help page explains the DuckDB Dashboard filtering system. Use it to understand how to effectively explore your data!*")

# Quick return button
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔙 Back to Dashboard"):
        st.switch_page("duckdb_dashboard.py")

with col2:
    st.write("")

with col3:
    if st.button("🏠 Home"):
        st.switch_page("streamlit_showcase.py")

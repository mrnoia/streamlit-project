import streamlit as st

st.set_page_config(
    layout="wide",
    page_title="Dashboard Building Tutorial",
    page_icon="🛠️"
)

# Custom CSS
st.markdown("""
<style>
.tutorial-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 10px;
    margin: 1rem 0;
}

.step-container {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    margin: 1rem 0;
    border-left: 4px solid #667eea;
}

.code-block {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 5px;
    font-family: 'Courier New', monospace;
    font-size: 0.9rem;
    overflow-x: auto;
    margin: 1rem 0;
}

.tip-box {
    background: #e8f5e8;
    padding: 1rem;
    border-radius: 5px;
    border-left: 4px solid #28a745;
    margin: 1rem 0;
}

.warning-box {
    background: #fff3cd;
    padding: 1rem;
    border-radius: 5px;
    border-left: 4px solid #ffc107;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

st.title("🛠️ Complete Dashboard Building Tutorial")
st.markdown("*Step-by-step guide to building professional Streamlit dashboards*")

# Overview
st.markdown('<div class="tutorial-container">', unsafe_allow_html=True)
st.markdown("""
## 🎯 **What You'll Learn**

This comprehensive tutorial will teach you how to build professional dashboards like the ones in this project:

### 📊 **Dashboard Types Covered:**
- **📈 Simple Dashboard** - Basic metrics and charts
- **📉 Analytics Dashboard** - Advanced BI with code examples
- **🦆 DuckDB Dashboard** - High-performance analytics with Parquet
- **📊 Tableau Dashboard** - Professional visual analytics

### 🛠️ **Skills You'll Master:**
- **Data handling** - Pandas, DuckDB, Parquet files
- **Visualization** - Plotly, charts, graphs
- **Layout design** - Columns, containers, styling
- **Interactivity** - Filters, widgets, navigation
- **Performance** - Caching, optimization
- **Code organization** - Structure, best practices
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Step 1: Setup and Dependencies
st.subheader("📋 Step 1: Project Setup")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Setting Up Your Dashboard Project**

#### 📁 **Project Structure:**
```
dashboard-project/
├── main.py              # Main navigation
├── requirements.txt      # Dependencies
├── data/                # Data files
│   └── sales_data.parquet
├── pages/               # Additional pages
│   └── dashboard.py
└── styles/              # Custom CSS
```

#### 📦 **Dependencies (requirements.txt):**
```text
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
duckdb>=1.1.3
numpy>=1.24.0
```

#### 🚀 **Installation:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run Streamlit
streamlit run main.py
```
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Step 2: Basic Dashboard Structure
st.subheader("🏗️ Step 2: Basic Dashboard Structure")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Creating Your First Dashboard**

#### 📝 **Basic Dashboard Template:**
""")

code = '''import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="My Dashboard",
    page_icon="📊"
)

# Custom CSS
st.markdown("""
<style>
.metric-container {
    background: #f0f2f6;
    padding: 1rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}
.chart-container {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 My Analytics Dashboard")
st.markdown("*Real-time data visualization and insights*")

# Generate or load data
@st.cache_data
def load_data():
    # Your data loading logic here
    return df

df = load_data()

# Sidebar for filters
st.sidebar.header("🔍 Filters")
# Add your filters here

# Main content
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("📈 Sales Trend")
    # Add chart here
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🥧 Category Distribution")
    # Add chart here
    st.markdown('</div>', unsafe_allow_html=True)'''

st.code(code, language='python')

st.markdown("""
#### 💡 **Key Components Explained:**

- **`st.set_page_config()`** - Sets page title, layout, and icon
- **Custom CSS** - Professional styling for your dashboard
- **`@st.cache_data`** - Caches data loading for performance
- **Columns** - `st.columns()` for layout management
- **Containers** - HTML divs for custom styling
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Step 3: Data Handling
st.subheader("📊 Step 3: Data Handling")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Working with Different Data Sources**

#### 🐼 **Pandas Approach (Simple Dashboard):**
""")

code = '''import pandas as pd
import numpy as np

@st.cache_data
def generate_sample_data():
    """Generate sample sales data"""
    np.random.seed(42)
    
    # Create date range
    dates = pd.date_range('2024-01-01', periods=730, freq='D')
    
    # Generate data
    data = []
    regions = ['North', 'South', 'East', 'West', 'Central']
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports']
    
    for date in dates:
        for region in regions:
            for category in categories:
                quantity = np.random.randint(1, 50)
                unit_price = np.random.uniform(10, 500)
                discount = np.random.uniform(0, 0.3)
                
                data.append({
                    'date': date,
                    'region': region,
                    'category': category,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'discount': discount,
                    'sales_amount': quantity * unit_price * (1 - discount)
                })
    
    return pd.DataFrame(data)

# Load data
df = generate_sample_data()
st.success(f"Loaded {len(df):,} records")'''

st.code(code, language='python')

st.markdown("""
#### 🦆 **DuckDB Approach (High Performance):**
""")

code = '''import duckdb
import pandas as pd

@st.cache_resource
def get_duckdb_connection():
    """Initialize DuckDB connection"""
    conn = duckdb.connect(":memory:")
    conn.execute("INSTALL httpfs")
    conn.execute("LOAD httpfs")
    return conn

@st.cache_data
def generate_and_load_data():
    """Generate data and load into DuckDB"""
    conn = get_duckdb_connection()
    
    # Generate sample data (same as above)
    df = generate_sample_data()
    
    # Save as Parquet for efficiency
    df.to_parquet('data/sales_data.parquet', index=False)
    
    # Load into DuckDB
    conn.execute("""
        CREATE OR REPLACE TABLE sales AS 
        SELECT * FROM read_parquet('data/sales_data.parquet')
    """)
    
    return conn

# Use DuckDB for queries
conn = generate_and_load_data()
result = conn.execute("SELECT COUNT(*) FROM sales").fetchone()
st.success(f"Loaded {result[0]:,} records into DuckDB")'''

st.code(code, language='python')

st.markdown('<div class="tip-box">', unsafe_allow_html=True)
st.markdown("""
**💡 Performance Tip:** Use DuckDB for large datasets (>100K rows) and Pandas for smaller datasets. DuckDB is 10-100x faster for analytical queries!
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Step 4: Creating Visualizations
st.subheader("📈 Step 4: Creating Visualizations")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Building Charts and Graphs**

#### 📊 **Line Chart (Time Series):**
""")

code = '''import plotly.express as px
import plotly.graph_objects as go

# Line chart for sales trend
def create_sales_trend(df):
    # Aggregate data by date
    daily_sales = df.groupby(df['date'].dt.date)['sales_amount'].sum().reset_index()
    
    fig = px.line(
        daily_sales, 
        x='date', 
        y='sales_amount',
        title="Daily Sales Trend",
        labels={'sales_amount': 'Sales Amount ($)', 'date': 'Date'}
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="Sales Amount ($)",
        hovermode='x unified'
    )
    
    fig.update_traces(
        line=dict(color='#1f77b4', width=2),
        mode='lines+markers'
    )
    
    return fig

# Display chart
fig = create_sales_trend(df)
st.plotly_chart(fig, use_container_width=True)'''

st.code(code, language='python')

st.markdown("""
#### 🥧 **Pie Chart (Distribution):**
""")

code = '''# Pie chart for regional distribution
def create_regional_pie(df):
    regional_sales = df.groupby('region')['sales_amount'].sum().reset_index()
    
    fig = px.pie(
        regional_sales,
        values='sales_amount',
        names='region',
        title="Sales by Region",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.2f}<br>Percentage: %{percent}'
    )
    
    fig.update_layout(height=400)
    return fig

fig = create_regional_pie(df)
st.plotly_chart(fig, use_container_width=True)'''

st.code(code, language='python')

st.markdown("""
#### 📊 **Bar Chart (Comparisons):**
""")

code = '''# Bar chart for category performance
def create_category_bar(df):
    category_sales = df.groupby('category')['sales_amount'].sum().reset_index()
    category_sales = category_sales.sort_values('sales_amount', ascending=False)
    
    fig = px.bar(
        category_sales,
        x='category',
        y='sales_amount',
        title="Sales by Category",
        color='sales_amount',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Category",
        yaxis_title="Sales Amount ($)"
    )
    
    return fig

fig = create_category_bar(df)
st.plotly_chart(fig, use_container_width=True)'''

st.code(code, language='python')

st.markdown('</div>', unsafe_allow_html=True)

# Step 5: Adding Interactivity
st.subheader("🎮 Step 5: Adding Interactivity")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Creating Interactive Filters**

#### 📅 **Date Range Filter:**
""")

code = '''# Date range filter
min_date = df['date'].min().date()
max_date = df['date'].max().date()

date_range = st.sidebar.date_input(
    "📅 Select Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Filter data based on date selection
filtered_df = df[
    (df['date'].dt.date >= date_range[0]) & 
    (df['date'].dt.date <= date_range[1])
]'''

st.code(code, language='python')

st.markdown("""
#### 🌍 **Multi-Select Filters:**
""")

code = '''# Multi-select filters
regions = df['region'].unique().tolist()
selected_regions = st.sidebar.multiselect(
    "🌍 Select Regions",
    options=regions,
    default=regions
)

categories = df['category'].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "📦 Select Categories",
    options=categories,
    default=categories
)

# Apply filters
if selected_regions:
    filtered_df = filtered_df[filtered_df['region'].isin(selected_regions)]
if selected_categories:
    filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]'''

st.code(code, language='python')

st.markdown("""
#### 💰 **Range Sliders:**
""")

code = '''# Range sliders for numeric values
min_sales, max_sales = st.sidebar.slider(
    "💰 Sales Amount Range",
    min_value=float(df['sales_amount'].min()),
    max_value=float(df['sales_amount'].max()),
    value=(float(df['sales_amount'].min()), float(df['sales_amount'].max())),
    step=100.0
)

min_qty, max_qty = st.sidebar.slider(
    "📦 Quantity Range",
    min_value=int(df['quantity'].min()),
    max_value=int(df['quantity'].max()),
    value=(int(df['quantity'].min()), int(df['quantity'].max()))
)

# Apply numeric filters
filtered_df = filtered_df[
    (filtered_df['sales_amount'] >= min_sales) & 
    (filtered_df['sales_amount'] <= max_sales)
]
filtered_df = filtered_df[
    (filtered_df['quantity'] >= min_qty) & 
    (filtered_df['quantity'] <= max_qty)
]'''

st.code(code, language='python')

st.markdown('</div>', unsafe_allow_html=True)

# Step 6: KPIs and Metrics
st.subheader("📊 Step 6: KPIs and Metrics")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Creating Key Performance Indicators**

#### 📈 **Basic KPIs:**
""")

code = '''# Calculate KPIs
total_sales = filtered_df['sales_amount'].sum()
total_transactions = len(filtered_df)
avg_sale = filtered_df['sales_amount'].mean()
total_quantity = filtered_df['quantity'].sum()

# Display KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales", 
        f"${total_sales:,.2f}",
        delta=f"{(total_sales / df['sales_amount'].sum() - 1) * 100:.1f}%"
    )

with col2:
    st.metric(
        "Transactions", 
        f"{total_transactions:,}",
        delta=f"{total_transactions - len(df):,}"
    )

with col3:
    st.metric(
        "Average Sale", 
        f"${avg_sale:.2f}",
        delta=f"${avg_sale - df['sales_amount'].mean():.2f}"
    )

with col4:
    st.metric(
        "Total Quantity", 
        f"{total_quantity:,}",
        delta=f"{total_quantity - df['quantity'].sum():,}"
    )'''

st.code(code, language='python')

st.markdown("""
#### 🎯 **Advanced KPIs with DuckDB:**
""")

code = '''# Advanced KPIs using DuckDB
@st.cache_data
def calculate_kpis(conn, date_range, regions, categories):
    """Calculate KPIs using DuckDB for performance"""
    
    # Build WHERE clause
    where_conditions = []
    params = []
    
    where_conditions.append("date BETWEEN ? AND ?")
    params.extend([date_range[0], date_range[1]])
    
    if regions:
        placeholders = ','.join(['?' for _ in regions])
        where_conditions.append(f"region IN ({placeholders})")
        params.extend(regions)
    
    if categories:
        placeholders = ','.join(['?' for _ in categories])
        where_conditions.append(f"category IN ({placeholders})")
        params.extend(categories)
    
    where_clause = " AND ".join(where_conditions)
    
    # Execute KPI query
    kpi_query = f"""
        SELECT 
            COUNT(*) as total_transactions,
            SUM(sales_amount) as total_sales,
            AVG(sales_amount) as avg_sale,
            SUM(quantity) as total_quantity,
            AVG(discount) * 100 as avg_discount_pct,
            COUNT(DISTINCT region) as regions_covered,
            COUNT(DISTINCT category) as categories_covered
        FROM sales
        WHERE {where_clause}
    """
    
    return conn.execute(kpi_query, params).fetchone()

# Display advanced KPIs
kpis = calculate_kpis(conn, date_range, selected_regions, selected_categories)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Transactions", f"{kpis[0]:,}")
    st.metric("Avg Discount", f"{kpis[4]:.1f}%")

with col2:
    st.metric("Total Sales", f"${kpis[1]:,.2f}")
    st.metric("Regions Covered", kpis[5])

with col3:
    st.metric("Avg Sale", f"${kpis[2]:,.2f}")
    st.metric("Categories Covered", kpis[6])'''

st.code(code, language='python')

st.markdown('</div>', unsafe_allow_html=True)

# Step 7: Advanced Features
st.subheader("🚀 Step 7: Advanced Features")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Adding Professional Features**

#### 📋 **Data Tables with Export:**
""")

code = '''# Data table with download option
def create_data_table(df):
    """Create interactive data table with export"""
    
    # Format data for display
    display_df = df.copy()
    display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
    display_df['unit_price'] = display_df['unit_price'].round(2)
    display_df['discount'] = (display_df['discount'] * 100).round(1).astype(str) + '%'
    display_df['sales_amount'] = display_df['sales_amount'].round(2)
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name='dashboard_data.csv',
        mime='text/csv'
    )
    
    # Display table
    st.dataframe(display_df, use_container_width=True, height=400)

create_data_table(filtered_df)'''

st.code(code, language='python')

st.markdown("""
#### 🗺️ **Geographic Visualizations:**
""")

code = '''# Geographic map visualization
import plotly.express as px

def create_geo_map(df):
    """Create geographic sales map"""
    
    # Sample coordinates for regions (in real app, use actual coordinates)
    region_coords = {
        'North': (40.7128, -74.0060),  # New York
        'South': (34.0522, -118.2437), # Los Angeles
        'East': (42.3601, -71.0589),   # Boston
        'West': (37.7749, -122.4194), # San Francisco
        'Central': (41.8781, -87.6298) # Chicago
    }
    
    # Aggregate data by region
    geo_data = df.groupby('region').agg({
        'sales_amount': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    # Add coordinates
    geo_data['lat'] = geo_data['region'].map(lambda x: region_coords[x][0])
    geo_data['lon'] = geo_data['region'].map(lambda x: region_coords[x][1])
    
    fig = px.scatter_geo(
        geo_data,
        lat='lat',
        lon='lon',
        size='sales_amount',
        hover_name='region',
        hover_data=['sales_amount', 'quantity'],
        title="Sales by Region",
        scope='usa',
        projection='albers usa'
    )
    
    fig.update_layout(height=500)
    return fig

fig = create_geo_map(filtered_df)
st.plotly_chart(fig, use_container_width=True)'''

st.code(code, language='python')

st.markdown("""
#### 📊 **Advanced Analytics:**
""")

code = '''# Correlation analysis
def create_correlation_heatmap(df):
    """Create correlation heatmap"""
    
    # Select numeric columns
    numeric_cols = ['quantity', 'unit_price', 'discount', 'sales_amount']
    corr_matrix = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        title="Feature Correlation Heatmap",
        color_continuous_scale='RdBu_r'
    )
    
    fig.update_layout(height=400)
    return fig

# Scatter plot for price vs quantity
def create_scatter_plot(df):
    """Create scatter plot with regression"""
    
    fig = px.scatter(
        df.sample(min(5000, len(df))),  # Sample for performance
        x='unit_price',
        y='quantity',
        color='category',
        size='sales_amount',
        title="Unit Price vs Quantity Analysis",
        hover_data=['sales_amount', 'discount']
    )
    
    fig.update_layout(height=400)
    return fig

# Display advanced analytics
col1, col2 = st.columns(2)

with col1:
    fig = create_correlation_heatmap(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = create_scatter_plot(filtered_df)
    st.plotly_chart(fig, use_container_width=True)'''

st.code(code, language='python')

st.markdown('</div>', unsafe_allow_html=True)

# Step 8: Performance Optimization
st.subheader("⚡ Step 8: Performance Optimization")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Making Your Dashboard Fast**

#### 🚀 **Caching Strategies:**
""")

code = '''import streamlit as st
import time

# Cache expensive operations
@st.cache_data(ttl=3600)  # Cache for 1 hour
def expensive_data_processing(data):
    """Process data with expensive computations"""
    time.sleep(2)  # Simulate expensive operation
    return data.groupby('category').agg({
        'sales_amount': ['sum', 'mean', 'count']
    }).round(2)

# Cache resources (connections, models)
@st.cache_resource
def get_database_connection():
    """Cache database connection"""
    import duckdb
    conn = duckdb.connect(":memory:")
    conn.execute("INSTALL httpfs")
    conn.execute("LOAD httpfs")
    return conn

# Cache with dependencies
@st.cache_data
def filter_data(df, date_range, regions, categories):
    """Cache filtered data"""
    mask = (
        (df['date'].dt.date >= date_range[0]) & 
        (df['date'].dt.date <= date_range[1])
    )
    
    if regions:
        mask &= df['region'].isin(regions)
    if categories:
        mask &= df['category'].isin(categories)
    
    return df[mask]'''

st.code(code, language='python')

st.markdown("""
#### 📊 **Data Loading Optimization:**
""")

code = '''# Lazy loading for large datasets
@st.cache_data
def load_data_chunk(chunk_size=10000):
    """Load data in chunks for memory efficiency"""
    
    # For CSV files
    chunks = []
    for chunk in pd.read_csv('large_dataset.csv', chunksize=chunk_size):
        # Process chunk
        processed_chunk = process_chunk(chunk)
        chunks.append(processed_chunk)
    
    return pd.concat(chunks, ignore_index=True)

# For Parquet files (recommended)
@st.cache_data
def load_parquet_data():
    """Load Parquet data efficiently"""
    return pd.read_parquet('data/sales_data.parquet')

# DuckDB for analytical queries
@st.cache_data
def query_data_duckdb(query):
    """Use DuckDB for fast analytical queries"""
    conn = get_database_connection()
    return conn.execute(query).fetchdf()'''

st.code(code, language='python')

st.markdown('<div class="warning-box">', unsafe_allow_html=True)
st.markdown("""
**⚠️ Performance Warning:** Always cache expensive operations and use appropriate data formats. Parquet is 10x faster than CSV for analytical queries!
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Step 9: Deployment
st.subheader("🚀 Step 9: Deployment")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Deploying Your Dashboard**

#### ☁️ **Streamlit Cloud (Easiest):**
""")

code = '''# 1. Push to GitHub
git add .
git commit -m "Add dashboard"
git push origin main

# 2. Go to streamlit.io
# - Connect your GitHub account
# - Select your repository
# - Deploy automatically

# 3. Add secrets (if needed)
# In Streamlit Cloud dashboard:
# - Settings → Secrets
# - Add database credentials, API keys, etc.'''

st.code(code, language='bash')

st.markdown("""
#### 🐳 **Docker Deployment:**
""")

code = '''# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

# docker-compose.yml
version: '3.8'
services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    volumes:
      - ./data:/app/data

# Run with Docker
docker-compose up -d'''

st.code(code, language='docker')

st.markdown("""
#### 🌐 **Other Options:**
- **Heroku** - Free tier available
- **AWS EC2** - Full control
- **Google Cloud Run** - Serverless
- **Azure App Service** - Enterprise features
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Step 10: Best Practices
st.subheader("✨ Step 10: Best Practices")

st.markdown('<div class="step-container">', unsafe_allow_html=True)
st.markdown("""
### 🎯 **Professional Dashboard Best Practices**

#### 🎨 **Design Principles:**
""")

code = '''# 1. Consistent Layout
def create_dashboard_layout():
    """Create consistent dashboard layout"""
    
    # Header
    st.title("📊 Analytics Dashboard")
    st.markdown("---")
    
    # KPIs Row
    col1, col2, col3, col4 = st.columns(4)
    
    # Charts Row 1
    col1, col2 = st.columns(2)
    
    # Charts Row 2
    col1, col2, col3 = st.columns(3)
    
    # Data Table
    st.markdown("---")
    st.subheader("📋 Detailed Data")

# 2. Color Scheme
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    'success': '#2ca02c',
    'warning': '#ff7f0e',
    'danger': '#d62728'
}

# 3. Consistent Styling
def apply_custom_styles():
    st.markdown(f"""
    <style>
    .metric-container {{
        background: {COLORS['primary']}10;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid {COLORS['primary']};
    }}
    .chart-container {{
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    </style>
    """, unsafe_allow_html=True)'''

st.code(code, language='python')

st.markdown("""
#### 📊 **Data Visualization Best Practices:**
""")

code = '''# 1. Choose the Right Chart
def choose_chart_type(data_type, analysis_type):
    """Choose appropriate chart based on data and analysis"""
    
    chart_guidelines = {
        ('time_series', 'trend'): 'line_chart',
        ('categorical', 'comparison'): 'bar_chart',
        ('categorical', 'proportion'): 'pie_chart',
        ('numerical', 'correlation'): 'scatter_plot',
        ('geographical', 'distribution'): 'map'
    }
    
    return chart_guidelines.get((data_type, analysis_type), 'bar_chart')

# 2. Consistent Chart Styling
def style_chart(fig, title=None):
    """Apply consistent styling to charts"""
    
    fig.update_layout(
        title=title,
        font=dict(size=12, family="Arial, sans-serif"),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# 3. Interactive Features
def add_interactivity(fig):
    """Add interactive features to charts"""
    
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +
                     "Value: %{y}<br>" +
                     "<extra></extra>"
    )
    
    return fig'''

st.code(code, language='python')

st.markdown("""
#### 🔧 **Code Organization:**
""")

code = '''# 1. Modular Structure
# dashboard.py
import streamlit as st
from components import charts, filters, kpis
from utils import data_loader, styling

def main():
    # Load data
    df = data_loader.load_data()
    
    # Apply filters
    filtered_df = filters.apply_filters(df)
    
    # Display KPIs
    kpis.display_kpis(filtered_df)
    
    # Display charts
    charts.display_charts(filtered_df)

# 2. Configuration Management
import configparser

def load_config():
    """Load dashboard configuration"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config

# 3. Error Handling
def safe_execute(func, *args, **kwargs):
    """Safely execute functions with error handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# 4. Logging
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def log_user_action(action):
    """Log user interactions"""
    logger.info(f"User action: {action}")'''

st.code(code, language='python')

st.markdown('<div class="tip-box">', unsafe_allow_html=True)
st.markdown("""
**💡 Pro Tip:** Always structure your code with clear separation of concerns. Use functions for reusable components and maintain consistent styling throughout your dashboard!
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Conclusion
st.markdown('<div class="tutorial-container">', unsafe_allow_html=True)
st.markdown("""
## 🎉 **Congratulations!**

You've now learned how to build professional Streamlit dashboards from scratch! Here's what you've mastered:

### ✅ **Skills Acquired:**
- **📊 Data handling** with Pandas and DuckDB
- **📈 Visualization** with Plotly charts and graphs
- **🎮 Interactivity** with filters and widgets
- **⚡ Performance** optimization with caching
- **🚀 Deployment** to cloud platforms
- **✨ Best practices** for professional dashboards

### 🎯 **Next Steps:**
1. **Build your own dashboard** using these techniques
2. **Experiment with different data sources**
3. **Add advanced features** like real-time updates
4. **Share your work** with the Streamlit community
5. **Contribute to open source** dashboard projects

### 📚 **Resources:**
- **Streamlit Documentation** - docs.streamlit.io
- **Plotly Gallery** - plotly.com/python
- **DuckDB Docs** - duckdb.org/docs
- **Community Forums** - discuss.streamlit.io

### 🌟 **Remember:**
- **Start simple** and add complexity gradually
- **Focus on user experience** and performance
- **Test thoroughly** before deployment
- **Iterate based on feedback**

Happy dashboard building! 🚀
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Navigation buttons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔙 Back to Tutorial"):
        st.switch_page("streamlit_showcase.py")

with col2:
    st.write("")

with col3:
    if st.button("🦆 Try DuckDB Dashboard"):
        st.switch_page("duckdb_dashboard.py")

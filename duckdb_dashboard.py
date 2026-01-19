import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import duckdb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

st.set_page_config(layout="wide")

# Custom CSS
st.markdown("""
<style>
.sidebar-filter {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.5rem;
    border-radius: 10px;
    text-align: center;
    margin: 0.5rem 0;
}

.chart-container {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin: 1rem 0;
}

.data-info {
    background: #e8f4fd;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #2196F3;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Initialize DuckDB connection
@st.cache_resource
def get_duckdb_connection():
    """Initialize DuckDB connection with extensions"""
    conn = duckdb.connect(":memory:")
    conn.execute("INSTALL httpfs")
    conn.execute("LOAD httpfs")
    return conn

# Generate and save sample data as Parquet
@st.cache_data
def generate_sample_data():
    """Generate sample sales data and save as Parquet"""
    np.random.seed(42)
    
    # Generate date range
    dates = pd.date_range('2024-01-01', periods=730, freq='D')
    
    # Generate data
    data = []
    regions = ['North', 'South', 'East', 'West', 'Central']
    categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Sports', 'Home', 'Beauty']
    products = {
        'Electronics': ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Smartwatch'],
        'Clothing': ['Shirt', 'Pants', 'Dress', 'Jacket', 'Shoes'],
        'Food': ['Pizza', 'Burger', 'Salad', 'Pasta', 'Sandwich'],
        'Books': ['Fiction', 'Non-Fiction', 'Textbook', 'Magazine', 'Comic'],
        'Sports': ['Ball', 'Racket', 'Shoes', 'Equipment', 'Accessories'],
        'Home': ['Furniture', 'Decor', 'Kitchen', 'Bathroom', 'Garden'],
        'Beauty': ['Skincare', 'Makeup', 'Haircare', 'Fragrance', 'Tools']
    }
    
    for date in dates:
        for region in regions:
            for category in categories:
                # Random number of transactions per category per day
                num_transactions = np.random.randint(1, 8)
                
                for _ in range(num_transactions):
                    product = np.random.choice(products[category])
                    quantity = np.random.randint(1, 20)
                    unit_price = np.random.uniform(10, 500)
                    discount = np.random.uniform(0, 0.3)
                    
                    data.append({
                        'date': date,
                        'region': region,
                        'category': category,
                        'product': product,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'discount': discount,
                        'sales_amount': quantity * unit_price * (1 - discount),
                        'customer_id': f"CUST_{np.random.randint(1000, 9999)}",
                        'sales_rep': f"REP_{np.random.randint(100, 999)}",
                        'store_id': f"STORE_{np.random.randint(1, 50)}"
                    })
    
    df = pd.DataFrame(data)
    
    # Save to Parquet
    os.makedirs('data', exist_ok=True)
    parquet_path = 'data/sales_data.parquet'
    df.to_parquet(parquet_path, index=False)
    
    return parquet_path, len(df)

# Main function
def main():
    st.title("🦆 DuckDB Analytics Dashboard")
    st.markdown("*High-performance analytics with DuckDB and Parquet files*")
    
    # Initialize connection and data
    conn = get_duckdb_connection()
    
    # Generate or load data
    with st.spinner("Preparing data..."):
        parquet_path, total_records = generate_sample_data()
        
        # Load data into DuckDB
        conn.execute(f"""
            CREATE OR REPLACE TABLE sales AS 
            SELECT * FROM read_parquet('{parquet_path}')
        """)
        
        # Get table memory usage - simplified approach
        row_count = conn.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        
        # Estimate memory usage based on data types
        # String columns: average length * count
        avg_string_length = 10  # Average string length estimate
        string_columns = 6  # region, category, product, customer_id, sales_rep, store_id
        string_bytes = row_count * avg_string_length * string_columns
        
        # Numeric columns: 8 bytes each
        numeric_columns = 5  # date, quantity, unit_price, discount, sales_amount
        numeric_bytes = row_count * 8 * numeric_columns
        
        total_bytes = string_bytes + numeric_bytes
        memory_mb = total_bytes / (1024 * 1024)
        memory_per_row = total_bytes / row_count
        
        # Store in tuple for consistency
        memory_info = (row_count, total_bytes)
        
        # Get basic info
        data_info = conn.execute("""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT region) as regions,
                COUNT(DISTINCT category) as categories,
                COUNT(DISTINCT product) as products,
                MIN(date) as start_date,
                MAX(date) as end_date
            FROM sales
        """).fetchone()
    
    # Data info banner
    with st.container():
        st.markdown(f"""
        <div class="data-info">
            <strong>📊 Dataset Overview:</strong> 
            {data_info[0]:,} records | 
            {data_info[1]} regions | 
            {data_info[2]} categories | 
            {data_info[3]} products | 
            {data_info[4].strftime('%Y-%m-%d')} to {data_info[5].strftime('%Y-%m-%d')} |
            <strong>🧠 Memory Usage:</strong> {memory_mb:.2f} MB total ({memory_per_row:.1f} bytes/row)
        </div>
        """, unsafe_allow_html=True)
    
    # Sidebar for filters
    st.sidebar.markdown('<div class="sidebar-filter">', unsafe_allow_html=True)
    st.sidebar.markdown("### 🔍 Filters")
    
    # Date range filter
    min_date = data_info[4].date()
    max_date = data_info[5].date()
    
    date_range = st.sidebar.date_input(
        "📅 Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        key="date_filter"
    )
    
    # Region filter
    regions = conn.execute("SELECT DISTINCT region FROM sales ORDER BY region").fetchall()
    selected_regions = st.sidebar.multiselect(
        "🌍 Regions",
        options=[r[0] for r in regions],
        default=[r[0] for r in regions],
        key="region_filter"
    )
    
    # Category filter
    categories = conn.execute("SELECT DISTINCT category FROM sales ORDER BY category").fetchall()
    selected_categories = st.sidebar.multiselect(
        "📦 Categories",
        options=[c[0] for c in categories],
        default=[c[0] for c in categories],
        key="category_filter"
    )
    
    # Product filter (dependent on selected categories)
    if selected_categories:
        product_query = f"""
            SELECT DISTINCT product 
            FROM sales 
            WHERE category IN ({','.join([f"'{cat}'" for cat in selected_categories])})
            ORDER BY product
        """
        products = conn.execute(product_query).fetchall()
        selected_products = st.sidebar.multiselect(
            "🛍️ Products",
            options=[p[0] for p in products],
            default=[],
            key="product_filter"
        )
    else:
        selected_products = []
    
    # Sales amount range
    sales_range = conn.execute("SELECT MIN(sales_amount), MAX(sales_amount) FROM sales").fetchone()
    min_sales, max_sales = st.sidebar.slider(
        "💰 Sales Amount Range",
        min_value=0.0,
        max_value=float(sales_range[1]),
        value=(0.0, float(sales_range[1])),
        step=100.0,
        key="sales_filter"
    )
    
    # Quantity range
    qty_range = conn.execute("SELECT MIN(quantity), MAX(quantity) FROM sales").fetchone()
    min_qty, max_qty = st.sidebar.slider(
        "📦 Quantity Range",
        min_value=int(qty_range[0]),
        max_value=int(qty_range[1]),
        value=(int(qty_range[0]), int(qty_range[1])),
        key="qty_filter"
    )
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Build WHERE clause for filters
    where_conditions = []
    params = []
    
    if len(date_range) == 2:
        where_conditions.append("date BETWEEN ? AND ?")
        params.extend([date_range[0], date_range[1]])
    
    if selected_regions:
        where_conditions.append(f"region IN ({','.join(['?' for _ in selected_regions])})")
        params.extend(selected_regions)
    
    if selected_categories:
        where_conditions.append(f"category IN ({','.join(['?' for _ in selected_categories])})")
        params.extend(selected_categories)
    
    if selected_products:
        where_conditions.append(f"product IN ({','.join(['?' for _ in selected_products])})")
        params.extend(selected_products)
    
    where_conditions.append("sales_amount BETWEEN ? AND ?")
    params.extend([min_sales, max_sales])
    
    where_conditions.append("quantity BETWEEN ? AND ?")
    params.extend([min_qty, max_qty])
    
    where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
    
    # Execute filtered query
    filtered_query = f"""
        SELECT 
            date,
            region,
            category,
            product,
            quantity,
            unit_price,
            discount,
            sales_amount,
            customer_id,
            sales_rep,
            store_id
        FROM sales
        WHERE {where_clause}
    """
    
    filtered_data = conn.execute(filtered_query, params).fetchdf()
    
    # Display filtered record count
    st.info(f"📊 Showing {len(filtered_data):,} records (filtered from {data_info[0]:,} total records)")
    
    if len(filtered_data) == 0:
        st.warning("No data matches the selected filters. Please adjust your filter criteria.")
        return
    
    # KPIs using DuckDB aggregations
    kpi_query = f"""
        SELECT 
            COUNT(*) as total_transactions,
            SUM(sales_amount) as total_sales,
            AVG(sales_amount) as avg_sale,
            SUM(quantity) as total_quantity,
            AVG(discount) * 100 as avg_discount_pct
        FROM sales
        WHERE {where_clause}
    """
    
    kpi_data = conn.execute(kpi_query, params).fetchone()
    
    # Display KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Transactions", f"{kpi_data[0]:,}")
    
    with col2:
        st.metric("Total Sales", f"${kpi_data[1]:,.2f}")
    
    with col3:
        st.metric("Avg Sale", f"${kpi_data[2]:,.2f}")
    
    with col4:
        st.metric("Total Quantity", f"{kpi_data[3]:,}")
    
    with col5:
        st.metric("Avg Discount", f"{kpi_data[4]:.1f}%")
    
    # KPIs Code Section
    with st.expander("💻 KPIs Code", expanded=False):
        st.code('''
# KPIs using DuckDB aggregations
kpi_query = f"""
    SELECT 
        COUNT(*) as total_transactions,
        SUM(sales_amount) as total_sales,
        AVG(sales_amount) as avg_sale,
        SUM(quantity) as total_quantity,
        AVG(discount) * 100 as avg_discount_pct
    FROM sales
    WHERE {where_clause}
"""

kpi_data = conn.execute(kpi_query, params).fetchone()

# Display KPIs
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Transactions", f"{kpi_data[0]:,}")

with col2:
    st.metric("Total Sales", f"${kpi_data[1]:,.2f}")

with col3:
    st.metric("Avg Sale", f"${kpi_data[2]:,.2f}")

with col4:
    st.metric("Total Quantity", f"{kpi_data[3]:,}")

with col5:
    st.metric("Avg Discount", f"{kpi_data[4]:.1f}%")
        ''', language='python')
    
    # Charts section
    st.markdown("---")
    
    # Sales trend over time
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📈 Sales Trend")
        
        trend_query = f"""
            SELECT 
                DATE_TRUNC('month', date) as month,
                SUM(sales_amount) as monthly_sales,
                COUNT(*) as transactions
            FROM sales
            WHERE {where_clause}
            GROUP BY DATE_TRUNC('month', date)
            ORDER BY month
        """
        
        trend_data = conn.execute(trend_query, params).fetchdf()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=trend_data['month'],
            y=trend_data['monthly_sales'],
            mode='lines+markers',
            name='Sales',
            line=dict(color='#1f77b4', width=3)
        ))
        
        fig.update_layout(
            title="Monthly Sales Trend",
            xaxis_title="Month",
            yaxis_title="Sales Amount ($)",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🥧 Sales by Region")
        
        region_query = f"""
            SELECT 
                region,
                SUM(sales_amount) as total_sales
            FROM sales
            WHERE {where_clause}
            GROUP BY region
            ORDER BY total_sales DESC
        """
        
        region_data = conn.execute(region_query, params).fetchdf()
        
        fig = px.pie(
            region_data,
            values='total_sales',
            names='region',
            title="Regional Distribution"
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Charts Code Section
    with st.expander("💻 Charts Code", expanded=False):
        st.code('''
# Sales Trend Chart
trend_query = f"""
    SELECT 
        DATE_TRUNC('month', date) as month,
        SUM(sales_amount) as monthly_sales,
        COUNT(*) as transactions
    FROM sales
    WHERE {where_clause}
    GROUP BY DATE_TRUNC('month', date)
    ORDER BY month
"""

trend_data = conn.execute(trend_query, params).fetchdf()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=trend_data['month'],
    y=trend_data['monthly_sales'],
    mode='lines+markers',
    name='Sales',
    line=dict(color='#1f77b4', width=3)
))

fig.update_layout(
    title="Monthly Sales Trend",
    xaxis_title="Month",
    yaxis_title="Sales Amount ($)",
    height=400
)

st.plotly_chart(fig, use_container_width=True)

# Regional Pie Chart
region_query = f"""
    SELECT 
        region,
        SUM(sales_amount) as total_sales
    FROM sales
    WHERE {where_clause}
    GROUP BY region
    ORDER BY total_sales DESC
"""

region_data = conn.execute(region_query, params).fetchdf()

fig = px.pie(
    region_data,
    values='total_sales',
    names='region',
    title="Regional Distribution"
)

fig.update_traces(textposition='inside', textinfo='percent+label')
fig.update_layout(height=400)

st.plotly_chart(fig, use_container_width=True)
        ''', language='python')
    
    # Category performance
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📦 Category Performance")
        
        category_query = f"""
            SELECT 
                category,
                SUM(sales_amount) as total_sales,
                COUNT(*) as transactions,
                AVG(sales_amount) as avg_sale
            FROM sales
            WHERE {where_clause}
            GROUP BY category
            ORDER BY total_sales DESC
        """
        
        category_data = conn.execute(category_query, params).fetchdf()
        
        fig = px.bar(
            category_data,
            x='category',
            y='total_sales',
            title="Sales by Category",
            color='total_sales',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(height=350, xaxis_title="", yaxis_title="Sales Amount ($)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🏆 Top Products")
        
        product_query = f"""
            SELECT 
                product,
                SUM(sales_amount) as total_sales,
                SUM(quantity) as total_quantity
            FROM sales
            WHERE {where_clause}
            GROUP BY product
            ORDER BY total_sales DESC
            LIMIT 10
        """
        
        product_data = conn.execute(product_query, params).fetchdf()
        
        fig = px.bar(
            product_data,
            x='total_sales',
            y='product',
            orientation='h',
            title="Top 10 Products by Sales",
            color='total_sales',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(height=350, xaxis_title="Sales Amount ($)", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Category & Product Charts Code Section
    with st.expander("💻 Category & Product Code", expanded=False):
        st.code('''
# Category Performance Bar Chart
category_query = f"""
    SELECT 
        category,
        SUM(sales_amount) as total_sales,
        COUNT(*) as transactions,
        AVG(sales_amount) as avg_sale
    FROM sales
    WHERE {where_clause}
    GROUP BY category
    ORDER BY total_sales DESC
"""

category_data = conn.execute(category_query, params).fetchdf()

fig = px.bar(
    category_data,
    x='category',
    y='total_sales',
    title="Sales by Category",
    color='total_sales',
    color_continuous_scale='Blues'
)

fig.update_layout(height=350, xaxis_title="", yaxis_title="Sales Amount ($)")
st.plotly_chart(fig, use_container_width=True)

# Top Products Horizontal Bar Chart
product_query = f"""
    SELECT 
        product,
        SUM(sales_amount) as total_sales,
        SUM(quantity) as total_quantity
    FROM sales
    WHERE {where_clause}
    GROUP BY product
    ORDER BY total_sales DESC
    LIMIT 10
"""

product_data = conn.execute(product_query, params).fetchdf()

fig = px.bar(
    product_data,
    x='total_sales',
    y='product',
    orientation='h',
    title="Top 10 Products by Sales",
    color='total_sales',
    color_continuous_scale='Viridis'
)

fig.update_layout(height=350, xaxis_title="Sales Amount ($)", yaxis_title="")
st.plotly_chart(fig, use_container_width=True)
        ''', language='python')
    
    # Advanced analytics section
    st.markdown("---")
    st.subheader("🔬 Advanced Analytics")
    
    # Correlation analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💰 Price vs Quantity Analysis")
        
        scatter_query = f"""
            SELECT 
                unit_price,
                quantity,
                discount,
                sales_amount
            FROM sales
            WHERE {where_clause}
            LIMIT 5000
        """
        
        scatter_data = conn.execute(scatter_query, params).fetchdf()
        
        fig = px.scatter(
            scatter_data,
            x='unit_price',
            y='quantity',
            size='sales_amount',
            color='discount',
            title="Unit Price vs Quantity",
            hover_data=['sales_amount']
        )
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Sales Distribution")
        
        dist_query = f"""
            SELECT 
                sales_bucket,
                COUNT(*) as count
            FROM (
                SELECT 
                    CASE 
                        WHEN sales_amount < 50 THEN '< $50'
                        WHEN sales_amount < 100 THEN '$50-$100'
                        WHEN sales_amount < 200 THEN '$100-$200'
                        WHEN sales_amount < 500 THEN '$200-$500'
                        ELSE '> $500'
                    END as sales_bucket
                FROM sales
                WHERE {where_clause}
            ) subquery
            GROUP BY sales_bucket
            ORDER BY 
                CASE sales_bucket
                    WHEN '< $50' THEN 1
                    WHEN '$50-$100' THEN 2
                    WHEN '$100-$200' THEN 3
                    WHEN '$200-$500' THEN 4
                    WHEN '> $500' THEN 5
                END
        """
        
        dist_data = conn.execute(dist_query, params).fetchdf()
        
        fig = px.bar(
            dist_data,
            x='sales_bucket',
            y='count',
            title="Sales Amount Distribution",
            color='count',
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(height=350, xaxis_title="Sales Amount", yaxis_title="Number of Transactions")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Advanced Analytics Code Section
    with st.expander("💻 Advanced Analytics Code", expanded=False):
        st.code('''
# Price vs Quantity Scatter Plot
scatter_query = f"""
    SELECT 
        unit_price,
        quantity,
        discount,
        sales_amount
    FROM sales
    WHERE {where_clause}
    LIMIT 5000
"""

scatter_data = conn.execute(scatter_query, params).fetchdf()

fig = px.scatter(
    scatter_data,
    x='unit_price',
    y='quantity',
    size='sales_amount',
    color='discount',
    title="Unit Price vs Quantity",
    hover_data=['sales_amount']
)

fig.update_layout(height=350)
st.plotly_chart(fig, use_container_width=True)

# Sales Distribution Histogram
dist_query = f"""
    SELECT 
        sales_bucket,
        COUNT(*) as count
    FROM (
        SELECT 
            CASE 
                WHEN sales_amount < 50 THEN '< $50'
                WHEN sales_amount < 100 THEN '$50-$100'
                WHEN sales_amount < 200 THEN '$100-$200'
                WHEN sales_amount < 500 THEN '$200-$500'
                ELSE '> $500'
            END as sales_bucket
        FROM sales
        WHERE {where_clause}
    ) subquery
    GROUP BY sales_bucket
    ORDER BY 
        CASE sales_bucket
            WHEN '< $50' THEN 1
            WHEN '$50-$100' THEN 2
            WHEN '$100-$200' THEN 3
            WHEN '$200-$500' THEN 4
            WHEN '> $500' THEN 5
        END
"""

dist_data = conn.execute(dist_query, params).fetchdf()

fig = px.bar(
    dist_data,
    x='sales_bucket',
    y='count',
    title="Sales Amount Distribution",
    color='count',
    color_continuous_scale='Reds'
)

fig.update_layout(height=350, xaxis_title="Sales Amount", yaxis_title="Number of Transactions")
st.plotly_chart(fig, use_container_width=True)
        ''', language='python')
    # Data table with simple display
    st.markdown("---")
    st.subheader("📋 Detailed Data")
    
    # Data info
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"Total: {len(filtered_data):,} filtered records")
    
    with col2:
        st.write(f"Memory usage: {memory_mb:.2f} MB for this table")
    
    # Get all data (Streamlit will handle scrolling)
    full_data_query = f"""
        SELECT 
            date,
            region,
            category,
            product,
            quantity,
            unit_price,
            discount,
            sales_amount
        FROM sales
        WHERE {where_clause}
        ORDER BY date DESC, sales_amount DESC
    """
    
    full_data = conn.execute(full_data_query, params).fetchdf()
    
    # Format for display
    display_data = full_data.copy()
    display_data['unit_price'] = display_data['unit_price'].round(2)
    display_data['discount'] = (display_data['discount'] * 100).round(1).astype(str) + '%'
    display_data['sales_amount'] = display_data['sales_amount'].round(2)
    
    # Display dataframe with height limit for scrolling
    st.dataframe(
        display_data, 
        use_container_width=True,
        height=500
    )
    
    # Data Table & Performance Code Section
    with st.expander("💻 Data Table & Performance Code", expanded=False):
        st.code('''
# Full Data Display (no artificial limits)
full_data_query = f"""
    SELECT 
        date,
        region,
        category,
        product,
        quantity,
        unit_price,
        discount,
        sales_amount
    FROM sales
    WHERE {where_clause}
    ORDER BY date DESC, sales_amount DESC
"""

full_data = conn.execute(full_data_query, params).fetchdf()

# Format for display
display_data = full_data.copy()
display_data['unit_price'] = display_data['unit_price'].round(2)
display_data['discount'] = (display_data['discount'] * 100).round(1).astype(str) + '%'
display_data['sales_amount'] = display_data['sales_amount'].round(2)

# Display dataframe with native scrolling
st.dataframe(
    display_data, 
    use_container_width=True,
    height=500
)

# Performance Metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("Table Memory", f"{memory_mb:.2f} MB")

with col2:
    st.metric("Total Rows", f"{memory_info[0]:,}")
        ''', language='python')
    
    # Code section
    with st.expander("💻 DuckDB Code Examples", expanded=False):
        st.code('''
# Initialize DuckDB connection
conn = duckdb.connect(":memory:")
conn.execute("INSTALL httpfs")
conn.execute("LOAD httpfs")

# Load Parquet data
conn.execute("""
    CREATE OR REPLACE TABLE sales AS 
    SELECT * FROM read_parquet('data/sales_data.parquet')
""")

# Query with filters
query = """
    SELECT 
        region,
        SUM(sales_amount) as total_sales
    FROM sales
    WHERE date BETWEEN '2024-01-01' AND '2024-12-31'
    GROUP BY region
    ORDER BY total_sales DESC
"""

results = conn.execute(query).fetchdf()

# Advanced analytics
correlation_query = """
    SELECT 
        CORR(unit_price, quantity) as price_qty_corr,
        CORR(discount, sales_amount) as discount_sales_corr
    FROM sales
"""
        ''', language='python')

if __name__ == "__main__":
    main()

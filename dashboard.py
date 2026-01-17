import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")

st.header("📊 Dashboard")

# Sample metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Users", "1,234", "+12%")
with col2:
    st.metric("Revenue", "$45,678", "+8%")
with col3:
    st.metric("Orders", "567", "-3%")
with col4:
    st.metric("Conversion", "3.2%", "+0.5%")

# Sample data
st.subheader("Recent Activity")
data = pd.DataFrame({
    'Date': pd.date_range('2024-01-01', periods=10),
    'Sales': np.random.randint(100, 1000, 10),
    'Users': np.random.randint(50, 200, 10)
})
st.dataframe(data, width='stretch')

# Simple chart
st.subheader("Sales Trend")
st.line_chart(data.set_index('Date')['Sales'])

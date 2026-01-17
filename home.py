import streamlit as st

st.set_page_config(layout="wide")

st.header("🏠 Home Page")
st.write("Welcome to the main application!")

# Sample content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Quick Stats")
    st.metric("Active Users", "1,234")
    st.metric("Today's Visits", "567")
    st.metric("Conversion Rate", "3.2%")

with col2:
    st.subheader("Recent Activity")
    st.write("- User login spike detected")
    st.write("- New feature deployed")
    st.write("- System performance optimal")

st.subheader("Getting Started")
st.write("Use the navigation bar above to switch between pages:")
st.write("🏠 **Home** - Main dashboard and overview")
st.write("📊 **Dashboard** - Detailed analytics and data")

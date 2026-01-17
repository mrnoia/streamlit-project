import streamlit as st

# Configure page to remove deploy button and other default elements
st.set_page_config(
    page_title="My App",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to hide deploy button and other elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Top Navigation Bar
def create_navbar():
    # CSS for navbar styling
    navbar_css = """
    <style>
    .navbar {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .navbar-brand {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .navbar-links {
        display: flex;
        gap: 2rem;
    }
    .navbar-link {
        text-decoration: none;
        color: #333;
        font-weight: 500;
        transition: color 0.3s;
    }
    .navbar-link:hover {
        color: #1f77b4;
    }
    </style>
    """
    
    st.markdown(navbar_css, unsafe_allow_html=True)
    
    # Navbar content
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.markdown('<div class="navbar-brand">🎯 My App</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("Home", key="nav_home"):
            st.session_state.page = "home"
    
    with col3:
        if st.button("Data", key="nav_data"):
            st.session_state.page = "data"
    
    with col4:
        if st.button("Analytics", key="nav_analytics"):
            st.session_state.page = "analytics"
    
    with col5:
        if st.button("Settings", key="nav_settings"):
            st.session_state.page = "settings"

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = "home"

# Create navbar
create_navbar()

# Page content based on selection
if st.session_state.page == "home":
    st.header("🏠 Home Page")
    st.write("Welcome to the home page!")
    st.write("This is where your main content goes.")
    
    # Example content
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Users", "1,234", "+12%")
        st.metric("Revenue", "$45,678", "+8%")
    with col2:
        st.metric("Orders", "567", "-3%")
        st.metric("Conversion", "3.2%", "+0.5%")

elif st.session_state.page == "data":
    st.header("📊 Data Page")
    st.write("Manage and view your data here.")
    
    # Example data table
    import pandas as pd
    import numpy as np
    
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'Age': [25, 30, 35, 28],
        'City': ['New York', 'London', 'Tokyo', 'Paris'],
        'Score': [85, 92, 78, 88]
    })
    
    st.dataframe(df, width='stretch')
    
    # Add new data
    with st.expander("Add New Entry"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120)
        city = st.text_input("City")
        score = st.slider("Score", 0, 100)
        
        if st.button("Add Entry"):
            st.success(f"Added {name} to the database!")

elif st.session_state.page == "analytics":
    st.header("📈 Analytics Page")
    st.write("View analytics and charts here.")
    
    # Example charts
    import pandas as pd
    import numpy as np
    
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['Sales', 'Marketing', 'Development']
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Performance Trends")
        st.line_chart(chart_data)
    
    with col2:
        st.subheader("Department Comparison")
        st.bar_chart(chart_data)
    
    # Metrics
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales", "$123,456", "+15%")
    with col2:
        st.metric("Active Users", "8,901", "+23%")
    with col3:
        st.metric("Conversion Rate", "4.5%", "+0.8%")
    with col4:
        st.metric("Avg. Order Value", "$67.89", "+$2.34")

elif st.session_state.page == "settings":
    st.header("⚙️ Settings Page")
    st.write("Configure your application settings.")
    
    # Settings form
    with st.form("settings_form"):
        st.subheader("General Settings")
        app_name = st.text_input("Application Name", value="My App")
        theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
        language = st.selectbox("Language", ["English", "Spanish", "French", "German"])
        
        st.subheader("Notification Settings")
        email_notifications = st.checkbox("Email Notifications", value=True)
        push_notifications = st.checkbox("Push Notifications", value=False)
        weekly_report = st.checkbox("Weekly Report", value=True)
        
        st.subheader("Data Settings")
        data_refresh_rate = st.selectbox("Data Refresh Rate", ["Real-time", "Every 5 minutes", "Every hour", "Daily"])
        export_format = st.selectbox("Default Export Format", ["CSV", "Excel", "PDF"])
        
        submitted = st.form_submit_button("Save Settings")
        
        if submitted:
            st.success("Settings saved successfully!")
            st.balloons()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        Built with Streamlit • © 2024 My App
    </div>
    """, 
    unsafe_allow_html=True
)

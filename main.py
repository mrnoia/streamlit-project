import streamlit as st

# Define your pages - organized by categories
# 📚 Learning & Tutorials
showcase_page = st.Page("streamlit_showcase.py", title="Streamlit Tutorial", icon="📚")

# 🏠 Basic Pages
home_page = st.Page("home.py", title="Home", icon="🏠")

# 📊 Dashboards & Analytics
dashboard_page = st.Page("dashboard.py", title="Simple Dashboard", icon="📊")
tableau_page = st.Page("tableau_dashboard.py", title="Tableau Dashboard", icon="📈")
comprehensive_page = st.Page("comprehensive_dashboard.py", title="Analytics Dashboard", icon="📉")

# 🧩 Components & Features
components_page = st.Page("components_demo.py", title="UI Components", icon="🧩")
dropdown_page = st.Page("dropdown_demo.py", title="Navigation Demo", icon="📋")
drilldown_page = st.Page("drilldown_demo.py", title="Drilldown Demo", icon="🔍")
duckdb_page = st.Page("duckdb_dashboard.py", title="DuckDB Dashboard", icon="🦆")

# 🌍 Multi-Page Drilldown System
multi_drilldown_page = st.Page("drilldown_multi_page.py", title="Multi-Page Drilldown", icon="🌍")

# Initialize navigation at top
pg = st.navigation([
    showcase_page,
    home_page,
    dashboard_page, 
    tableau_page, 
    comprehensive_page,
    components_page, 
    dropdown_page, 
    drilldown_page,
    duckdb_page,
    multi_drilldown_page
], position="top")

# Run the selected page
pg.run()

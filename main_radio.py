import streamlit as st

# Radio button navigation in sidebar
st.sidebar.title("Navigation")
page_selection = st.sidebar.radio(
    "Choose a page:",
    ["Home", "Dashboard", "Components"],
    index=0
)

# Define your pages
home_page = st.Page("home.py", title="Home", icon="🙂")
dashboard_page = st.Page("dashboard.py", title="Dashboard", icon=":material/dashboard:")
components_page = st.Page("components_demo.py", title="Components", icon=":material/widgets:")

# Map selection to pages
if page_selection == "Home":
    home_page.run()
elif page_selection == "Dashboard":
    dashboard_page.run()
elif page_selection == "Components":
    components_page.run()

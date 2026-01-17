import streamlit as st

st.set_page_config(layout="wide")

st.header("📋 Dropdown Navigation Demo")

st.write("This page demonstrates different dropdown navigation options:")

# Option 1: Simple Selectbox
st.subheader("Option 1: Simple Selectbox")
selected_option1 = st.selectbox(
    "Choose an option:",
    ["Dashboard", "Analytics", "Reports", "Settings"],
    key="selectbox1"
)
st.write(f"Selected: {selected_option1}")

# Option 2: Selectbox with icons
st.subheader("Option 2: Selectbox with Icons")
selected_option2 = st.selectbox(
    "Navigate to:",
    ["🏠 Home", "📊 Dashboard", "📈 Analytics", "⚙️ Settings"],
    key="selectbox2"
)
st.write(f"Selected: {selected_option2}")

# Option 3: Multi-level navigation
st.subheader("Option 3: Multi-level Navigation")
category = st.selectbox(
    "Select Category:",
    ["Data", "Analytics", "Reports"],
    key="category"
)

if category == "Data":
    sub_option = st.selectbox(
        "Select Data Type:",
        ["User Data", "Sales Data", "Product Data"],
        key="data_sub"
    )
elif category == "Analytics":
    sub_option = st.selectbox(
        "Select Analytics Type:",
        ["User Analytics", "Sales Analytics", "Performance Analytics"],
        key="analytics_sub"
    )
else:
    sub_option = st.selectbox(
        "Select Report Type:",
        ["Daily Report", "Weekly Report", "Monthly Report"],
        key="report_sub"
    )

st.write(f"Category: {category}, Sub-option: {sub_option}")

# Option 4: Custom styled dropdown
st.subheader("Option 4: Custom Styled Navigation")

# Custom CSS for dropdown styling
custom_css = """
<style>
.custom-dropdown {
    background-color: #f0f2f6;
    padding: 20px;
    border-radius: 10px;
    border: 2px solid #e1e5e9;
    margin: 10px 0;
}
.custom-dropdown h4 {
    color: #1f77b4;
    margin-top: 0;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="custom-dropdown">', unsafe_allow_html=True)
    st.markdown('<h4>🎯 Quick Navigation</h4>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        quick_nav = st.selectbox(
            "Quick Access:",
            ["📱 Mobile View", "💻 Desktop View", "📊 Full Dashboard", "🔧 Admin Panel"],
            key="quick_nav"
        )
    
    with col2:
        action = st.selectbox(
            "Action:",
            ["View Details", "Edit", "Delete", "Export"],
            key="action"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Option 5: Interactive demo
st.subheader("Option 5: Interactive Navigation Demo")

navigation_choice = st.selectbox(
    "Simulate Navigation:",
    ["Home Page", "User Profile", "Settings", "Help Center"],
    key="interactive_nav"
)

# Show different content based on selection
if navigation_choice == "Home Page":
    st.info("🏠 Welcome to the Home Page!")
    st.write("This would show the main dashboard and overview.")
elif navigation_choice == "User Profile":
    st.info("👤 User Profile")
    st.write("This would show user information and settings.")
elif navigation_choice == "Settings":
    st.info("⚙️ Settings")
    st.write("This would show application configuration options.")
elif navigation_choice == "Help Center":
    st.info("❓ Help Center")
    st.write("This would show documentation and support resources.")

# Navigation summary
st.subheader("Navigation Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Option 1", selected_option1[:10] + "...")

with col2:
    st.metric("Option 2", selected_option2.split()[0])

with col3:
    st.metric("Category", category)

with col4:
    st.metric("Quick Nav", quick_nav.split()[0])

st.write("---")
st.write("💡 **Tip**: While `st.navigation` doesn't support dropdowns directly, you can use `st.selectbox()` or `st.radio()` to create dropdown-style navigation in your apps.")

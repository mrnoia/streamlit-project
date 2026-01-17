import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

st.set_page_config(
    page_title="Streamlit Showcase",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.feature-card {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 1rem 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>✨ Streamlit Showcase & Tutorial</h1>
    <p>Master the art of building beautiful, interactive web applications with Python</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
Welcome to the comprehensive Streamlit showcase! This interactive tutorial demonstrates
the full power and flexibility of Streamlit components and features.

## 🎯 What You'll Learn:
- **Interactive Widgets** - All input components with working examples
- **💻 Code Examples** - Copy-paste ready code for each component
- **Best Practices** - Professional implementation patterns
- **Real Applications** - See components in action
""")

# 🧪 TEST CODE SECTION
st.markdown("## 🧪 TEST: Can you see this code section?")
st.markdown("This should be VERY visible - please let me know if you can see this!")
st.code('''
import streamlit as st

# This is a test code block
st.write("Hello World!")
st.button("Click me")
''', language='python')
st.markdown("---")

# UI Components Section
st.header("🎨 UI Components Showcase")

# Basic Inputs
st.subheader("📝 Basic Input Widgets")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

text_input = st.text_input("Text Input", placeholder="Enter text...")
number_input = st.number_input("Number Input", min_value=0, max_value=100, value=25)
slider = st.slider("Slider", 0, 100, 50)

st.write(f"Text: {text_input}")
st.write(f"Number: {number_input}")
st.write(f"Slider: {slider}")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Basic Inputs
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Use this in your own Streamlit app*")
st.code('''
# Basic input widgets
text_input = st.text_input("Enter your text")
number_input = st.number_input("Enter number", min_value=0, max_value=100)
slider = st.slider("Select value", 0, 100, 50)

# Display results
st.write(f"Text: {text_input}")
st.write(f"Number: {number_input}")
st.write(f"Slider: {slider}")
''', language='python')
st.markdown("---")

# Selection Widgets
st.subheader("🎯 Selection Widgets")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

selectbox = st.selectbox("Select Box", ["Option 1", "Option 2", "Option 3"])
multiselect = st.multiselect("Multi Select", ["A", "B", "C", "D"])
radio = st.radio("Radio Buttons", ["Choice 1", "Choice 2", "Choice 3"])
checkbox = st.checkbox("Check this box")

st.write(f"Selected: {selectbox}")
st.write(f"Multi: {multiselect}")
st.write(f"Radio: {radio}")
st.write(f"Checked: {checkbox}")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Selection Widgets
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Perfect for selection widgets*")
st.code('''
# Selection widgets
selectbox = st.selectbox("Choose option", ["Option 1", "Option 2", "Option 3"])
multiselect = st.multiselect("Select multiple", ["A", "B", "C", "D"])
radio = st.radio("Radio choice", ["Choice 1", "Choice 2", "Choice 3"])
checkbox = st.checkbox("Check me")

# Display selections
st.write(f"Selected: {selectbox}")
st.write(f"Multi-selected: {multiselect}")
st.write(f"Radio choice: {radio}")
st.write(f"Checked: {checkbox}")
''', language='python')
st.markdown("---")

# Advanced Widgets
st.subheader("🚀 Advanced Widgets")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

date_input = st.date_input("Date Picker")
time_input = st.time_input("Time Picker")
color_picker = st.color_picker("Color Picker", "#667eea")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Advanced Widgets
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Date, time, and color widgets*")
st.code('''
# Date and time widgets
date_input = st.date_input("Select date")
time_input = st.time_input("Select time")
color_picker = st.color_picker("Choose color", "#667eea")

# Display values
st.write(f"Date: {date_input}")
st.write(f"Time: {time_input}")
st.write(f"Color: {color_picker}")
''', language='python')
st.markdown("---")

# File Upload
st.subheader("📁 File Handling")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

file_uploader = st.file_uploader("Upload File", type=['csv', 'txt'])
if file_uploader:
    st.success(f"File uploaded: {file_uploader.name}")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for File Upload
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*File upload handling*")
st.code('''
# File upload
uploaded_file = st.file_uploader("Choose file", type=['csv', 'txt'])

if uploaded_file is not None:
    st.success(f"File uploaded: {uploaded_file.name}")
    # Process file
    df = pd.read_csv(uploaded_file)
    st.dataframe(df)
''', language='python')
st.markdown("---")

# Expandable and Popover
st.subheader("🎭 Interactive Elements")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

with st.expander("📋 Expandable Section"):
    st.write("This is an expandable section!")
    st.write("You can put any content here.")

with st.popover("🎯 Popover"):
    st.write("This appears when clicked!")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Interactive Elements
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Expandable and popover elements*")
st.code('''
# Expandable and popover
with st.expander("Click to expand"):
    st.write("Hidden content here!")

with st.popover("Click for popover"):
    st.write("Popover content!")
''', language='python')
st.markdown("---")

# Text Display Components
st.subheader("📝 Text & Display Components")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

st.text("This is st.text() - plain text")
st.markdown("**This is st.markdown() - **bold** and *italic* text")
st.code("print('This is st.code() - code display')", language='python')
st.latex(r"\int_a^b f(x) dx = F(b) - F(a)")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Text Display
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Text and display components*")
st.code('''
# Text display components
st.text("Plain text display")
st.markdown("**Markdown** with *formatting*")
st.code("print('Code block')", language='python')
st.latex(r"\int_a^b f(x) dx = F(b) - F(a)")
''', language='python')
st.markdown("---")

# Media Components
st.subheader("🖼️ Media Components")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

# Create sample data for media
sample_image_data = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="

st.image(sample_image_data, caption="Sample Image", width=200)

# Simple audio placeholder
st.write("🎵 Audio component (requires actual audio file)")
st.write("Use: st.audio('path/to/audio.mp3')")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Media
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Image, audio, and video components*")
st.code('''
# Media components
st.image("path/to/image.jpg", caption="My Image", width=300)
st.audio("path/to/audio.mp3")
st.video("path/to/video.mp4")

# From URL
st.image("https://example.com/image.jpg")
st.audio("https://example.com/audio.mp3")
''', language='python')
st.markdown("---")

# Data Display Components
st.subheader("📊 Data Display Components")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

# Sample data
sample_df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 28],
    'City': ['New York', 'London', 'Paris', 'Tokyo'],
    'Salary': [50000, 60000, 70000, 55000]
})

st.dataframe(sample_df, use_container_width=True)

st.table(sample_df.head(2))

st.json({
    "name": "Streamlit",
    "version": "1.28.0",
    "features": ["widgets", "charts", "dataframes"]
})

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Data Display
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Data display components*")
st.code('''
# Data display components
import pandas as pd

df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30]
})

# Interactive dataframe
st.dataframe(df)

# Static table
st.table(df)

# JSON display
st.json({"key": "value"})

# Metrics
st.metric("Total", 1000, "+10%")
''', language='python')
st.markdown("---")

# Status Messages
st.subheader("🔔 Status Messages")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.success("✅ Success!")
with col2:
    st.info("ℹ️ Info")
with col3:
    st.warning("⚠️ Warning")
with col4:
    st.error("❌ Error")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Status Messages
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Status and alert components*")
st.code('''
# Status messages
st.success("Operation completed successfully!")
st.info("Here's some useful information")
st.warning("Please be careful")
st.error("Something went wrong!")

# Exception handling
try:
    # Your code here
    pass
except Exception as e:
    st.error(f"Error: {e}")
''', language='python')
st.markdown("---")

# Progress and Loading
st.subheader("⏳ Progress & Loading")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

# Progress bar
progress_bar = st.progress(0)
for i in range(101):
    progress_bar.progress(i)
    time.sleep(0.01)

# Spinner
with st.spinner("Loading..."):
    time.sleep(1)
st.success("Done!")

# Empty placeholder
placeholder = st.empty()
placeholder.text("Loading data...")
time.sleep(1)
placeholder.text("Data loaded!")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Progress
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Progress and loading components*")
st.code('''
# Progress bar
progress_bar = st.progress(0)
for i in range(101):
    progress_bar.progress(i)
    time.sleep(0.01)

# Spinner
with st.spinner("Loading..."):
    time.sleep(1)
st.success("Done!")

# Empty placeholder
placeholder = st.empty()
placeholder.text("Loading...")
time.sleep(1)
placeholder.text("Complete!")
''', language='python')
st.markdown("---")

# Forms
st.subheader("📋 Forms")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

with st.form("my_form"):
    st.write("Fill out this form:")
    
    name = st.text_input("Name")
    email = st.text_input("Email")
    message = st.text_area("Message")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.success(f"Thank you {name}! Form submitted.")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Forms
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Form components*")
st.code('''
# Form with submit button
with st.form("my_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.success(f"Form submitted by {name}")
''', language='python')
st.markdown("---")

# Charts and Visualizations
st.subheader("📈 Charts & Visualizations")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

# Sample chart data
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

# Different chart types
col1, col2 = st.columns(2)

with col1:
    st.line_chart(chart_data)
    st.bar_chart(chart_data)

with col2:
    st.area_chart(chart_data)
    
    # Plotly chart
    fig = px.scatter(
        chart_data, x='A', y='B', 
        title="Interactive Plotly Chart"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Charts
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Chart and visualization components*")
st.code('''
# Built-in charts
st.line_chart(data)
st.bar_chart(data)
st.area_chart(data)

# Plotly charts
import plotly.express as px
fig = px.scatter(data, x='x', y='y')
st.plotly_chart(fig)

# Matplotlib
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 2])
st.pyplot(fig)
''', language='python')
st.markdown("---")

# Layout Components
st.subheader("🎨 Layout Components")
st.markdown('<div class="feature-card">', unsafe_allow_html=True)

# Columns
st.write("**Columns:**")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("Column 1")
    st.button("Button 1")

with col2:
    st.write("Column 2")
    st.button("Button 2")

with col3:
    st.write("Column 3")
    st.button("Button 3")

# Container
st.write("**Container:**")
with st.container():
    st.write("This is in a container")
    st.write("It groups related elements")

# Tabs
st.write("**Tabs:**")
tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

with tab1:
    st.write("Content for tab 1")
with tab2:
    st.write("Content for tab 2")
with tab3:
    st.write("Content for tab 3")

st.markdown('</div>', unsafe_allow_html=True)

# Code section for Layout
st.markdown("---")
st.markdown("### 💻 COPY THIS CODE:")
st.markdown("*Layout and organization components*")
st.code('''
# Columns
col1, col2 = st.columns(2)
with col1:
    st.write("Left column")
with col2:
    st.write("Right column")

# Container
with st.container():
    st.write("Grouped content")

# Tabs
tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
with tab1:
    st.write("Tab 1 content")
with tab2:
    st.write("Tab 2 content")

# Sidebar
st.sidebar.title("Sidebar")
st.sidebar.slider("Slider", 0, 100, 50)
''', language='python')
st.markdown("---")

# Footer
st.markdown("""
---
## 🎉 Congratulations!

You've just explored the main Streamlit UI components with working code examples! 

**Next Steps:**
- Copy the code snippets above to build your own apps
- Explore the other dashboard examples in the navigation
- Check out the [Streamlit Documentation](https://docs.streamlit.io/) for more features

**Happy Streamlit-ing!** 🚀
""")

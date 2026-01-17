import streamlit as st

st.set_page_config(layout="wide")

st.title("Streamlit Components Demo")

# Basic Widgets
st.header("🎛️ Basic Widgets")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Widgets")
    button = st.button("Click me")
    text_input = st.text_input("Enter text")
    number_input = st.number_input("Enter number", min_value=0, max_value=100, value=25)
    slider = st.slider("Select value", 0, 100, 50)
    selectbox = st.selectbox("Choose option", ["Option 1", "Option 2", "Option 3"])
    multiselect = st.multiselect("Select multiple", ["A", "B", "C", "D"])
    checkbox = st.checkbox("Check me")
    radio = st.radio("Radio buttons", ["Radio 1", "Radio 2", "Radio 3"])
    text_area = st.text_area("Multi-line text")
    date_input = st.date_input("Select date")
    time_input = st.time_input("Select time")
    file_uploader = st.file_uploader("Upload file")
    color_picker = st.color_picker("Pick a color")

with col2:
    st.subheader("Display Results")
    st.write("Button clicked:", button)
    st.write("Text input:", text_input)
    st.write("Number input:", number_input)
    st.write("Slider value:", slider)
    st.write("Selectbox:", selectbox)
    st.write("Multiselect:", multiselect)
    st.write("Checkbox state:", checkbox)
    st.write("Radio selection:", radio)
    st.write("Text area:", text_area)
    st.write("Date:", date_input)
    st.write("Time:", time_input)
    st.write("File:", file_uploader)
    st.write("Color:", color_picker)

# Display Elements
st.header("📊 Display Elements")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Text & Media")
    st.text("Simple text")
    st.markdown("**Markdown** text with *formatting*")
    st.code("print('Hello, World!')", language='python')
    st.latex(r"E = mc^2")
    st.image("https://via.placeholder.com/300x200", caption="Sample Image")
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

with col4:
    st.subheader("Data Display")
    import pandas as pd
    import numpy as np
    
    df = pd.DataFrame({
        'A': np.random.randn(10),
        'B': np.random.randn(10),
        'C': np.random.randn(10)
    })
    
    st.dataframe(df)
    st.table(df.head())
    st.json({"key": "value", "number": 42})
    st.metric("Revenue", "$1.2M", "+12%")
    st.success("Success message!")
    st.info("Info message!")
    st.warning("Warning message!")
    st.error("Error message!")

# Charts
st.header("📈 Charts")
col5, col6 = st.columns(2)

with col5:
    st.subheader("Basic Charts")
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )
    st.line_chart(chart_data)
    st.bar_chart(chart_data)
    st.area_chart(chart_data)

with col6:
    st.subheader("Advanced Charts")
    import plotly.express as px
    import matplotlib.pyplot as plt
    
    # Plotly chart
    fig = px.scatter(chart_data, x='A', y='B', color='C')
    st.plotly_chart(fig, width='stretch')
    
    # Matplotlib chart
    fig, ax = plt.subplots()
    ax.scatter(chart_data['A'], chart_data['B'])
    st.pyplot(fig)

# Layout
st.header("🎨 Layout Elements")
col7, col8 = st.columns([2, 1])

with col7:
    st.subheader("Columns & Containers")
    inner_col1, inner_col2, inner_col3 = st.columns(3)
    with inner_col1:
        st.write("Column 1")
    with inner_col2:
        st.write("Column 2")
    with inner_col3:
        st.write("Column 3")
    
    with st.container():
        st.write("This is in a container")
        st.write("Container can hold multiple elements")

with col8:
    st.subheader("Other Layout")
    st.sidebar.title("Sidebar")
    st.sidebar.write("Sidebar content")
    
    with st.expander("Click to expand"):
        st.write("Hidden content here")
    
    with st.popover("Popover"):
        st.write("Popover content")

# Progress & Status
st.header("⏳ Progress & Status")
progress_bar = st.progress(25)
status_text = st.empty()

# Simulate progress
import time
for i in range(25, 101, 25):
    time.sleep(0.5)
    progress_bar.progress(i)
    status_text.text(f'Progress: {i}%')

# Forms
st.header("📝 Forms")
with st.form("my_form"):
    st.write("Inside a form")
    form_text = st.text_input("Enter text in form")
    form_slider = st.slider("Slider in form", 0, 100, 50)
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        st.write(f"Form submitted with: {form_text}, {form_slider}")

# Session State
st.header("💾 Session State")
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment counter"):
    st.session_state.counter += 1

st.write(f"Counter: {st.session_state.counter}")

# Navigation
st.header("🧭 Navigation")
page = st.sidebar.selectbox("Choose page", ["Home", "Data", "Settings"])

if page == "Home":
    st.write("Welcome to Home page")
elif page == "Data":
    st.write("This is the Data page")
else:
    st.write("Settings page")

st.write("---")
st.write("💡 **Tip**: Check [Streamlit documentation](https://docs.streamlit.io/library/api-reference) for all available components!")

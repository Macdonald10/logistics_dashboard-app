import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# MUST BE FIRST COMMAND
st.set_page_config(
    page_title="Logistics Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .header {
        color: white;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        background: white;
    }
    .stButton>button {
        width: 100%;
        padding: 1rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>Logistics Intelligence Platform</h1>
    <p>Data-Driven Supply Chain Optimization</p>
</div>
""", unsafe_allow_html=True)

# Navigation Cards
st.markdown("## Explore Dashboard Sections")
cols = st.columns(4)
nav_items = [
    ("📊 Overview", "Key metrics and trends", "1_🏠_Overview"),
    ("📈 Deep Analysis", "Detailed performance breakdown", "2_📊_Analysis"),
    ("🔍 Root Causes", "Identify bottlenecks", "3_🔍_Root_Cause"),
    ("🎛️ Data Explorer", "Interactive investigation", "5_🎛️_Interactive")
]

for col, (title, desc, target) in zip(cols, nav_items):
    with col:
        with st.container(border=True, height=200):
            if st.button(title):
                switch_page(target)
            st.caption(desc)

# Footer
st.markdown("---")
st.markdown("""
<center>
    <p>Powered by Streamlit | Logistics Analytics Suite v2.0</p>
</center>
""", unsafe_allow_html=True)

 import streamlit as st

# MUST BE FIRST COMMAND
st.set_page_config(
    page_title="Logistics Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (now comes after set_page_config)
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
    .nav-card {
        transition: transform 0.3s;
        cursor: pointer;
        height: 100%;
        padding: 1rem;
    }
    .nav-card:hover {
        transform: translateY(-5px);
    }
    /* Hide Streamlit's default menu and footer */
    header { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .stDeployButton { display:none; }
</style>
""", unsafe_allow_html=True)

# Page Content
st.markdown("""
<div class="header">
    <h1>Logistics Intelligence Platform</h1>
    <p>Data-Driven Supply Chain Optimization</p>
</div>
""", unsafe_allow_html=True)

# Navigation Cards using Streamlit's native navigation
st.markdown("## Explore Dashboard Sections")
cols = st.columns(4)
nav_items = [
    ("📊 Overview", "Key metrics and trends", "Overview"),
    ("📈 Deep Analysis", "Detailed performance breakdown", "Analysis"),
    ("🔍 Root Causes", "Identify bottlenecks", "Root_Cause"),
    ("🎛️ Data Explorer", "Interactive investigation", "Interactive")
]

for col, (title, desc, target) in zip(cols, nav_items):
    with col:
        with st.container(border=True, height=200):
            st.markdown(f"""
            <div class="nav-card">
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)
            st.page_link(f"pages/{target}.py", label="Navigate →", use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<center>
    <p>Powered by Streamlit | Logistics Analytics Suite v2.0</p>
</center>
""", unsafe_allow_html=True)

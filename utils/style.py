import streamlit as st
import os

CSS = """
<style>
/* ── Main background — white throughout ─────────────────────────────────── */
[data-testid="stAppViewContainer"] { background: #FFFFFF !important; }
[data-testid="stMain"]             { background: #FFFFFF !important; }
[data-testid="stHeader"]           { background: #FFFFFF !important; }

/* ── Sidebar — green ────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%) !important;
}
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebarNav"] a {
    color: white !important;
    font-weight: 500;
}
[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.15) !important;
    border-radius: 6px;
}
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(255,255,255,0.25) !important;
    border-radius: 6px;
    font-weight: 700;
}

/* ── Metric cards ───────────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background-color: #F1F8E9;
    border-left: 5px solid #2E7D32;
    border-radius: 8px;
    padding: 12px 16px;
}
[data-testid="stMetricValue"] { color: #1B5E20 !important; font-weight: 700; }

/* ── Buttons ────────────────────────────────────────────────────────────── */
div.stButton > button {
    background-color: #2E7D32 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
div.stButton > button:hover { background-color: #1B5E20 !important; }
div.stButton > button[kind="secondary"] { background-color: #C62828 !important; }

/* ── Download buttons ───────────────────────────────────────────────────── */
div.stDownloadButton > button {
    background-color: #C62828 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* ── Headings ───────────────────────────────────────────────────────────── */
h1 {
    border-bottom: 3px solid #2E7D32;
    padding-bottom: 8px;
    color: #1B5E20 !important;
}
h2 { color: #2E7D32 !important; }
h3 { color: #C62828 !important; }

/* ── Forms ──────────────────────────────────────────────────────────────── */
[data-testid="stForm"] {
    border: 1px solid #C8E6C9;
    border-radius: 10px;
    padding: 16px;
    background: #FAFAFA;
}

/* ── Tabs ───────────────────────────────────────────────────────────────── */
[data-testid="stTabs"] button[aria-selected="true"] {
    border-bottom: 3px solid #2E7D32 !important;
    color: #2E7D32 !important;
    font-weight: 700;
}
</style>
"""

def inject_style():
    st.markdown(CSS, unsafe_allow_html=True)

def sidebar_logo():
    if os.path.exists("assets/logo.png"):
        st.sidebar.image("assets/logo.png", use_container_width=True)
    st.sidebar.markdown(
        "<h3 style='text-align:center;color:white;margin-top:-10px;'>"
        "Smart Seed Warehouse</h3>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown("---")

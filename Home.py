import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils.auth  import require_login, logout_button
from utils.style import inject_style, sidebar_logo

st.set_page_config(
    page_title="Smart Seed Warehouse",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

require_login()
inject_style()
sidebar_logo()
logout_button()

# ── Hero banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(90deg,#1B5E20,#2E7D32);
            border-radius:12px;padding:32px 40px;margin-bottom:24px;">
  <h1 style="color:white;border:none;margin:0;font-size:2.2rem;">
    🌱 Smart Seed Warehouse Management System
  </h1>
  <p style="color:#C8E6C9;margin:8px 0 0;font-size:1.05rem;">
    Intelligent stock monitoring · ML-powered predictions · Full operational management
  </p>
</div>
""", unsafe_allow_html=True)

# ── Module cards ────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div style="background:#F1F8E9;border-left:5px solid #2E7D32;
                border-radius:10px;padding:20px;height:140px;">
      <h3 style="color:#2E7D32;margin-top:0;">📊 Dashboard</h3>
      <p style="color:#333;font-size:0.9rem;">
        Live KPIs, stock level charts, alert heatmaps, and expiry warnings.
      </p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#FFF8F8;border-left:5px solid #C62828;
                border-radius:10px;padding:20px;height:140px;">
      <h3 style="color:#C62828;margin-top:0;">🔮 Predictions</h3>
      <p style="color:#333;font-size:0.9rem;">
        ML models predict stock status, alert levels and germination rates.
      </p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background:#F1F8E9;border-left:5px solid #2E7D32;
                border-radius:10px;padding:20px;height:140px;">
      <h3 style="color:#2E7D32;margin-top:0;">➕ Data Entry</h3>
      <p style="color:#333;font-size:0.9rem;">
        Record incoming seed stock with full sensor and lot details.
      </p>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("""
    <div style="background:#FFF8F8;border-left:5px solid #C62828;
                border-radius:10px;padding:20px;height:140px;">
      <h3 style="color:#C62828;margin-top:0;">🚚 Dispatch</h3>
      <p style="color:#333;font-size:0.9rem;">
        Create outgoing orders and track dispatch status end-to-end.
      </p>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div style="background:#F1F8E9;border-left:5px solid #2E7D32;
                border-radius:10px;padding:20px;height:140px;">
      <h3 style="color:#2E7D32;margin-top:0;">📦 Stock Take</h3>
      <p style="color:#333;font-size:0.9rem;">
        Physical count entry with automatic discrepancy detection.
      </p>
    </div>""", unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div style="background:#FFF8F8;border-left:5px solid #C62828;
                border-radius:10px;padding:20px;height:140px;">
      <h3 style="color:#C62828;margin-top:0;">📋 Records</h3>
      <p style="color:#333;font-size:0.9rem;">
        Search, filter, edit and export full transaction history.
      </p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")
st.caption(f"Logged in as: {st.session_state.get('username','user')}  |  Data: data/warehouse.csv")

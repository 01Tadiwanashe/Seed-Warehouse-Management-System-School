import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from utils.auth  import require_login, logout_button
from utils.style import inject_style, sidebar_logo
from utils.db    import load_data, summary_kpis

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
require_login()
inject_style()
sidebar_logo()
logout_button()
st.title("Dashboard")

df   = load_data()
kpis = summary_kpis(df)

st.markdown("### Key Performance Indicators")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Records",         f"{kpis['total_records']:,}")
c2.metric("Total Seed Stock (kg)", f"{kpis['total_seeds_kg']:,.0f}")
c3.metric("Critical Low Stock",    kpis["critical_low"])
c4.metric("Critical Alerts",       kpis["critical_alerts"])
c5.metric("Avg Germination Rate",  f"{kpis['avg_germination']:.1f}%")
c6, c7, c8, c9, c10 = st.columns(5)
c6.metric("Low Stock Items",       kpis["low_stock"])
c7.metric("Warning Alerts",        kpis["warning_alerts"])
c8.metric("Pending Dispatches",    kpis["pending_dispatches"])
c9.metric("Total Order Value",     f"${kpis['total_order_value']:,.0f}")
c10.metric("Seed Varieties",       df["seed_name"].nunique())
st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Stock Status")
    vc = df["stock_status"].value_counts().reset_index()
    vc.columns = ["Status", "Count"]
    fig = px.bar(vc, x="Status", y="Count", color="Status", text="Count",
                 color_discrete_map={"Optimal":"#2E7D32","Low":"#FF8F00",
                                     "Critical Low":"#C62828","Overstocked":"#1565C0"})
    fig.update_layout(showlegend=False, height=320, margin=dict(t=10),
                      plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Alert Level")
    vc2 = df["overall_alert"].value_counts().reset_index()
    vc2.columns = ["Alert", "Count"]
    fig2 = px.pie(vc2, names="Alert", values="Count", hole=0.45,
                  color="Alert",
                  color_discrete_map={"Normal":"#2E7D32","Warning":"#FF8F00","Critical":"#C62828"})
    fig2.update_layout(height=320, margin=dict(t=10), paper_bgcolor="white")
    st.plotly_chart(fig2, use_container_width=True)

with col3:
    st.subheader("Stock by Seed (kg)")
    ss = df.groupby("seed_name")["quantity_kg"].sum().sort_values(ascending=True).reset_index()
    ss.columns = ["Seed", "kg"]
    fig3 = px.bar(ss, x="kg", y="Seed", orientation="h",
                  color_discrete_sequence=["#2E7D32"])
    fig3.update_layout(showlegend=False, height=320, margin=dict(t=10),
                       plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig3, use_container_width=True)

col4, col5 = st.columns(2)
with col4:
    st.subheader("Alert Heatmap - Seed x Zone")
    alert_map = {"Normal": 0, "Warning": 1, "Critical": 2}
    df["alert_num"] = df["overall_alert"].map(alert_map)
    pivot = df.pivot_table(values="alert_num", index="seed_name",
                           columns="warehouse_zone", aggfunc="mean")
    fig4 = px.imshow(pivot, color_continuous_scale=["#2E7D32","#FF8F00","#C62828"],
                     zmin=0, zmax=2, text_auto=".2f",
                     labels=dict(color="Alert Score"))
    fig4.update_layout(height=340, margin=dict(t=10), paper_bgcolor="white")
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    st.subheader("Germination Rate by Seed")
    fig5 = px.box(df, x="seed_name", y="germination_rate_pct", color="seed_name",
                  color_discrete_sequence=["#2E7D32","#C62828","#FF8F00","#1565C0","#6A1B9A"],
                  labels={"germination_rate_pct": "Rate (%)", "seed_name": "Seed"})
    fig5.update_layout(showlegend=False, height=340, margin=dict(t=10),
                       plot_bgcolor="white", paper_bgcolor="white")
    st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.subheader("Recent Records")
cols_show = ["record_id","seed_name","warehouse_zone","bin_id","quantity_kg",
             "stock_status","overall_alert","germination_rate_pct","dispatch_status","timestamp"]
st.dataframe(df[cols_show].sort_values("timestamp", ascending=False).head(20),
             use_container_width=True)

st.markdown("---")
st.subheader("Expiring Within 90 Days")
df["days_to_expiry"] = (pd.to_datetime(df["expiry_date"]) - pd.Timestamp.now()).dt.days
expiring = df[df["days_to_expiry"].between(0, 90)][
    ["seed_name","lot_number","bin_id","quantity_kg","expiry_date","days_to_expiry"]
].sort_values("days_to_expiry")
if len(expiring):
    st.dataframe(expiring, use_container_width=True)
else:
    st.success("No lots expiring within 90 days.")

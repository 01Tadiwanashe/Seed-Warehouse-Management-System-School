import streamlit as st
import pandas as pd
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from utils.auth  import require_login, logout_button
from utils.style import inject_style, sidebar_logo
from utils.db    import load_data, save_data, compute_stock_status

st.set_page_config(page_title="Stock Take", page_icon="📦", layout="wide")
require_login()
inject_style()
sidebar_logo()
logout_button()
st.title("Stock Take")
st.info("Conduct a physical count and reconcile against system records.")

df          = load_data()
zone        = st.selectbox("Warehouse zone", ["All","A","B","C","D"])
seed_filter = st.multiselect("Filter by seed", df["seed_name"].unique().tolist())
filtered    = df.copy()
if zone != "All":
    filtered = filtered[filtered["warehouse_zone"] == zone]
if seed_filter:
    filtered = filtered[filtered["seed_name"].isin(seed_filter)]

st.subheader("Current Stock by Bin")
bin_summary = filtered.groupby(["warehouse_zone","bin_id","seed_name","lot_number"]).agg(
    System_qty_kg=("quantity_kg","last"),
    Reorder_level=("reorder_level_kg","last"),
    Max_capacity =("max_capacity_kg","last"),
    Stock_status =("stock_status","last"),
    Expiry       =("expiry_date","last"),
).reset_index()
st.dataframe(bin_summary, use_container_width=True)

st.markdown("---")
st.subheader("Record Physical Count")
with st.form("stocktake_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        zones    = filtered["warehouse_zone"].unique().tolist()
        sel_zone = st.selectbox("Zone", zones if zones else ["A"])
    with col2:
        bins     = filtered[filtered["warehouse_zone"] == sel_zone]["bin_id"].unique().tolist() if zones else []
        sel_bin  = st.selectbox("Bin ID", bins if bins else [""])
    with col3:
        actual_qty = st.number_input("Actual physical count (kg)", 0.0, 20000.0, 0.0, 1.0)
    notes  = st.text_area("Notes", placeholder="Optional")
    submit = st.form_submit_button("Submit Count", use_container_width=True)

if submit:
    mask = (df["warehouse_zone"] == sel_zone) & (df["bin_id"] == sel_bin)
    if mask.sum() == 0:
        st.error("No record found for that zone and bin.")
    else:
        last_idx    = df[mask].index[-1]
        system_qty  = df.loc[last_idx, "quantity_kg"]
        discrepancy = actual_qty - system_qty
        new_status  = compute_stock_status(
            actual_qty,
            df.loc[last_idx, "reorder_level_kg"],
            df.loc[last_idx, "max_capacity_kg"]
        )
        df.loc[last_idx, "quantity_kg"]  = actual_qty
        df.loc[last_idx, "stock_status"] = new_status
        save_data(df)
        ca, cb, cc = st.columns(3)
        ca.metric("System quantity", f"{system_qty:,.1f} kg")
        cb.metric("Actual count",    f"{actual_qty:,.1f} kg")
        cc.metric("Discrepancy",     f"{discrepancy:+,.1f} kg",
                  delta=f"{discrepancy:+,.1f}", delta_color="inverse")
        if abs(discrepancy) < 1:
            st.success("Count matches system record.")
        elif discrepancy < 0:
            st.warning(f"{abs(discrepancy):.1f} kg LESS than system — possible loss or unrecorded dispatch.")
        else:
            st.info(f"{discrepancy:.1f} kg MORE than system — possible unrecorded receipt.")
        st.success(f"Stock status updated to {new_status}")

st.markdown("---")
st.subheader("Zone Stock Summary")
st.dataframe(
    df.groupby(["warehouse_zone","stock_status"]).size().unstack(fill_value=0),
    use_container_width=True
)

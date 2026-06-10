import streamlit as st
import pandas as pd
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from utils.auth  import require_login, logout_button
from utils.style import inject_style, sidebar_logo
from utils.db    import load_data, save_data

st.set_page_config(page_title="Dispatch", page_icon="🚚", layout="wide")
require_login()
inject_style()
sidebar_logo()
logout_button()
st.title("Dispatch Management")

df = load_data()
tab1, tab2 = st.tabs(["Manage Existing Orders", "Create New Dispatch"])

with tab1:
    st.subheader("Outgoing Orders")
    outgoing = df[df["order_type"] == "Outgoing"].copy()
    status_filter = st.multiselect(
        "Filter by status",
        ["Pending","Dispatched","Delivered","Cancelled"],
        default=["Pending","Dispatched"]
    )
    filtered = outgoing[outgoing["dispatch_status"].isin(status_filter)] if status_filter else outgoing
    cols = ["record_id","order_id","seed_name","lot_number","quantity_ordered_kg",
            "supplier_or_customer","price_per_kg_usd","total_order_value_usd",
            "dispatch_status","timestamp"]
    st.dataframe(filtered[cols].sort_values("timestamp", ascending=False), use_container_width=True)

    st.subheader("Update Dispatch Status")
    pending_ids = outgoing[outgoing["dispatch_status"].isin(["Pending","Dispatched"])]["order_id"].tolist()
    if pending_ids:
        sel   = st.selectbox("Select order ID", pending_ids)
        nstat = st.selectbox("New status", ["Dispatched","Delivered","Cancelled"])
        if st.button("Update Status"):
            df.loc[df["order_id"] == sel, "dispatch_status"] = nstat
            save_data(df)
            st.success(f"Order {sel} updated to {nstat}")
            st.rerun()
    else:
        st.info("No pending orders.")

    st.subheader("Dispatch Summary")
    summary = df[df["order_type"] == "Outgoing"].groupby("dispatch_status").agg(
        Orders=("order_id","count"),
        Total_kg=("quantity_ordered_kg","sum"),
        Total_USD=("total_order_value_usd","sum"),
    ).reset_index()
    st.dataframe(summary, use_container_width=True)

with tab2:
    st.subheader("Create New Outgoing Order")
    with st.form("dispatch_form", clear_on_submit=True):
        d1, d2 = st.columns(2)
        with d1:
            seed_name    = st.selectbox("Seed name",             df["seed_name"].unique().tolist())
            lot_number   = st.text_input("Lot number",           placeholder="Enter lot number")
            customer     = st.text_input("Customer / recipient *")
        with d2:
            qty_ordered  = st.number_input("Quantity to dispatch (kg)", 0.0, 20000.0, 200.0, 10.0)
            price_per_kg = st.number_input("Price per kg (USD)",         0.0,   200.0,  15.0,  0.5)
            wzone        = st.selectbox("From warehouse zone",           ["A","B","C","D"])
        sub = st.form_submit_button("Create Dispatch Order", use_container_width=True)

    if sub:
        if not customer:
            st.error("Customer name is required.")
        else:
            matching = df[(df["seed_name"] == seed_name) & (df["warehouse_zone"] == wzone)]
            if len(matching) == 0:
                st.error("No stock found for that seed and zone.")
            else:
                new_id   = len(df) + 1
                order_id = f"ORD-{new_id + 1000}"
                base     = matching.iloc[-1].to_dict()
                base.update({
                    "record_id": new_id, "timestamp": pd.Timestamp.now(),
                    "order_id": order_id, "order_type": "Outgoing",
                    "quantity_ordered_kg": qty_ordered,
                    "supplier_or_customer": customer,
                    "price_per_kg_usd": price_per_kg,
                    "total_order_value_usd": qty_ordered * price_per_kg,
                    "dispatch_status": "Pending",
                })
                df = pd.concat([df, pd.DataFrame([base])], ignore_index=True)
                save_data(df)
                st.success(f"Dispatch order {order_id} created — {qty_ordered}kg of {seed_name} to {customer}")

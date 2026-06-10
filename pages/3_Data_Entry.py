import streamlit as st
import pandas as pd
from datetime import date
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from utils.auth  import require_login, logout_button
from utils.style import inject_style, sidebar_logo
from utils.db    import load_data, save_data, get_next_record_id, compute_stock_status, compute_alerts

st.set_page_config(page_title="Data Entry", page_icon="➕", layout="wide")
require_login()
inject_style()
sidebar_logo()
logout_button()
st.title("New Seed Stock Entry")
st.info("Record new incoming seed stock with full sensor and lot details.")

with st.form("entry_form", clear_on_submit=True):
    st.subheader("Seed Information")
    c1, c2, c3 = st.columns(3)
    with c1:
        seed_name      = st.selectbox("Seed name *",      ["Maize","Wheat","Beans","Soyabeans","Yellow Maize"])
        category       = st.selectbox("Category *",       ["Cereal","Legume"])
        variety        = st.text_input("Variety",         placeholder="e.g. SC301")
    with c2:
        warehouse_zone = st.selectbox("Warehouse zone *", ["A","B","C","D"])
        bin_id         = st.text_input("Bin ID *",        placeholder="e.g. A-01-03")
        lot_number     = st.text_input("Lot number *",    placeholder="e.g. 0124-01-BNT")
    with c3:
        grower_number  = st.number_input("Grower number", 100, 999, 110)
        received_from  = st.text_input("Received from",   placeholder="Supplier name")
        date_received  = st.date_input("Date received",   value=date.today())

    st.subheader("Quantity & Capacity")
    q1, q2, q3 = st.columns(3)
    with q1:
        quantity_kg      = st.number_input("Quantity received (kg) *", 0.0, 20000.0, 500.0, 10.0)
    with q2:
        reorder_level_kg = st.number_input("Reorder level (kg)",       0.0,  5000.0, 300.0, 10.0)
    with q3:
        max_capacity_kg  = st.number_input("Max capacity (kg)",      100.0, 20000.0, 5000.0, 100.0)

    st.subheader("Sensor Readings")
    s1, s2, s3, s4, s5 = st.columns(5)
    with s1:
        temperature_c        = st.number_input("Temperature (C)",     -10.0,  50.0, 18.0, 0.5)
    with s2:
        humidity_pct         = st.number_input("Humidity (%)",          0.0, 100.0, 55.0, 1.0)
    with s3:
        moisture_content_pct = st.number_input("Moisture content (%)",  0.0,  30.0, 12.0, 0.5)
    with s4:
        co2_level_ppm        = st.number_input("CO2 level (ppm)",     300.0, 2000.0, 450.0, 10.0)
    with s5:
        germination_rate_pct = st.number_input("Germination rate (%)",  0.0, 100.0, 85.0, 1.0)

    st.subheader("Order Details")
    o1, o2, o3, o4, o5 = st.columns(5)
    with o1:
        order_type           = st.selectbox("Order type",          ["Incoming","Outgoing"])
    with o2:
        quantity_ordered_kg  = st.number_input("Qty ordered (kg)",  0.0, 20000.0, 500.0, 10.0)
    with o3:
        supplier_or_customer = st.text_input("Supplier / Customer")
    with o4:
        price_per_kg_usd     = st.number_input("Price per kg (USD)", 0.0, 200.0, 15.0, 0.5)
    with o5:
        expiry_date          = st.date_input("Expiry date", value=date(date.today().year + 2, 1, 1))

    submitted = st.form_submit_button("Save Record", use_container_width=True)

if submitted:
    if not bin_id or not lot_number:
        st.error("Bin ID and Lot Number are required.")
    else:
        df = load_data()
        stock_status = compute_stock_status(quantity_kg, reorder_level_kg, max_capacity_kg)
        temp_alert, humidity_alert, overall_alert = compute_alerts(temperature_c, humidity_pct)
        new_row = {
            "record_id": get_next_record_id(df), "timestamp": pd.Timestamp.now(),
            "seed_name": seed_name, "category": category, "variety": variety,
            "warehouse_zone": warehouse_zone, "bin_id": bin_id, "lot_number": lot_number,
            "grower_number": grower_number, "received_from": received_from,
            "quantity_kg": quantity_kg, "reorder_level_kg": reorder_level_kg,
            "max_capacity_kg": max_capacity_kg, "stock_status": stock_status,
            "date_received": str(date_received), "expiry_date": str(expiry_date),
            "temperature_c": temperature_c, "humidity_pct": humidity_pct,
            "moisture_content_pct": moisture_content_pct, "co2_level_ppm": co2_level_ppm,
            "germination_rate_pct": germination_rate_pct,
            "temp_alert": temp_alert, "humidity_alert": humidity_alert, "overall_alert": overall_alert,
            "order_id": f"ORD-{get_next_record_id(df) + 1000}",
            "order_type": order_type, "quantity_ordered_kg": quantity_ordered_kg,
            "supplier_or_customer": supplier_or_customer, "dispatch_status": "Pending",
            "price_per_kg_usd": price_per_kg_usd,
            "total_order_value_usd": quantity_ordered_kg * price_per_kg_usd,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success(f"Record {new_row['record_id']} saved! Status: {stock_status} | Alert: {overall_alert}")
        if overall_alert == "Critical":
            st.error("CRITICAL ALERT: Temperature and humidity are both out of range!")
        elif overall_alert == "Warning":
            st.warning("WARNING: Storage conditions need attention.")

import streamlit as st
import pandas as pd
import numpy as np
import joblib, os, sys
from datetime import date
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from utils.auth     import require_login, logout_button
from utils.style    import inject_style, sidebar_logo
from utils.features import engineer_features, NUMERIC_FEATURES, CATEGORICAL_FEATURES

st.set_page_config(page_title="Predictions", page_icon="🔮", layout="wide")
require_login()
inject_style()
sidebar_logo()
logout_button()
st.title("ML Predictions")

@st.cache_resource
def load_models():
    models = {}
    for name, fname in [("stock","stock_model.pkl"),
                        ("alert","alert_model.pkl"),
                        ("germ", "germ_model.pkl")]:
        path = f"models/{fname}"
        if os.path.exists(path):
            models[name] = joblib.load(path)
    return models

models = load_models()
if not models:
    st.error("No trained models found in the models/ folder. Run the Jupyter notebook first.")
    st.code("""
import joblib, os
os.makedirs('models', exist_ok=True)
joblib.dump(best_stock_pipe, 'models/stock_model.pkl')
joblib.dump(best_alert_pipe, 'models/alert_model.pkl')
joblib.dump(best_reg_pipe,   'models/germ_model.pkl')
print("Models saved!")""")
    st.stop()

st.info("Fill in the details below and click Run Predictions.")

with st.form("predict_form"):
    st.subheader("Seed & Storage Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        seed_name      = st.selectbox("Seed name",      ["Maize","Wheat","Beans","Soyabeans","Yellow Maize"])
        category       = st.selectbox("Category",       ["Cereal","Legume"])
        warehouse_zone = st.selectbox("Warehouse zone", ["A","B","C","D"])
        order_type     = st.selectbox("Order type",     ["Incoming","Outgoing"])
    with col2:
        quantity_kg         = st.number_input("Quantity (kg)",         0.0, 10000.0, 1000.0, 50.0)
        reorder_level_kg    = st.number_input("Reorder level (kg)",    0.0,  5000.0,  300.0, 50.0)
        max_capacity_kg     = st.number_input("Max capacity (kg)",   100.0, 20000.0, 5000.0, 100.0)
        quantity_ordered_kg = st.number_input("Qty ordered (kg)",      0.0, 10000.0,  500.0, 50.0)
        price_per_kg_usd    = st.number_input("Price per kg (USD)",    0.0,   100.0,   15.0,  0.5)
    with col3:
        temperature_c        = st.slider("Temperature (C)",      0.0,  40.0, 18.0, 0.5)
        humidity_pct         = st.slider("Humidity (%)",         20.0, 100.0, 55.0, 1.0)
        moisture_content_pct = st.slider("Moisture content (%)",  1.0,  25.0, 12.0, 0.5)
        co2_level_ppm        = st.slider("CO2 level (ppm)",     300.0, 1000.0, 450.0, 10.0)
        germination_rate_pct = st.slider("Germination rate (%)",  0.0,  100.0, 80.0,  1.0)
    date_received = st.date_input("Date received", value=date.today())
    expiry_date   = st.date_input("Expiry date",   value=date(date.today().year + 2, 1, 1))
    submitted     = st.form_submit_button("Run Predictions", use_container_width=True)

if submitted:
    row = pd.DataFrame([{
        "record_id": 0, "timestamp": pd.Timestamp.now(),
        "seed_name": seed_name, "category": category, "variety": "Unknown",
        "warehouse_zone": warehouse_zone, "bin_id": "A-01-01", "lot_number": "PRED-001",
        "grower_number": 100, "received_from": "Manual",
        "quantity_kg": quantity_kg, "reorder_level_kg": reorder_level_kg,
        "max_capacity_kg": max_capacity_kg, "stock_status": "Optimal",
        "date_received": pd.Timestamp(date_received), "expiry_date": pd.Timestamp(expiry_date),
        "temperature_c": temperature_c, "humidity_pct": humidity_pct,
        "moisture_content_pct": moisture_content_pct, "co2_level_ppm": co2_level_ppm,
        "germination_rate_pct": germination_rate_pct,
        "temp_alert": "Normal", "humidity_alert": "Normal", "overall_alert": "Normal",
        "order_id": "PRED", "order_type": order_type,
        "quantity_ordered_kg": quantity_ordered_kg, "supplier_or_customer": "Manual",
        "dispatch_status": "Pending", "price_per_kg_usd": price_per_kg_usd,
        "total_order_value_usd": price_per_kg_usd * quantity_ordered_kg,
    }])
    row = engineer_features(row)
    X   = row[NUMERIC_FEATURES + CATEGORICAL_FEATURES].copy()

    st.markdown("---")
    st.subheader("Prediction Results")
    r1, r2, r3 = st.columns(3)

    with r1:
        if "stock" in models:
            pred  = models["stock"].predict(X)[0]
            color = {"Optimal":"#2E7D32","Low":"#FF8F00","Critical Low":"#C62828","Overstocked":"#1565C0"}.get(pred, "gray")
            st.markdown(f"""<div style="background:#F1F8E9;border-left:6px solid {color};
                border-radius:10px;padding:20px;text-align:center;">
              <p style="margin:0;color:#555;">Stock Status</p>
              <h2 style="color:{color};margin:6px 0;">{pred}</h2></div>""", unsafe_allow_html=True)
            if hasattr(models["stock"], "predict_proba"):
                proba = models["stock"].predict_proba(X)[0]
                st.dataframe(
                    pd.DataFrame({"Status": models["stock"].classes_, "Probability": proba})
                    .sort_values("Probability", ascending=False),
                    hide_index=True
                )

    with r2:
        if "alert" in models:
            pred_a  = models["alert"].predict(X)[0]
            color_a = {"Normal":"#2E7D32","Warning":"#FF8F00","Critical":"#C62828"}.get(pred_a, "gray")
            st.markdown(f"""<div style="background:#FFF8F8;border-left:6px solid {color_a};
                border-radius:10px;padding:20px;text-align:center;">
              <p style="margin:0;color:#555;">Alert Level</p>
              <h2 style="color:{color_a};margin:6px 0;">{pred_a}</h2></div>""", unsafe_allow_html=True)
            if hasattr(models["alert"], "predict_proba"):
                proba_a = models["alert"].predict_proba(X)[0]
                st.dataframe(
                    pd.DataFrame({"Alert": models["alert"].classes_, "Probability": proba_a})
                    .sort_values("Probability", ascending=False),
                    hide_index=True
                )

    with r3:
        if "germ" in models:
            X_g    = row[[c for c in NUMERIC_FEATURES if c != "germination_rate_pct"] + CATEGORICAL_FEATURES].copy()
            pred_g = models["germ"].predict(X_g)[0]
            color_g = "#2E7D32" if pred_g >= 70 else "#FF8F00" if pred_g >= 50 else "#C62828"
            st.markdown(f"""<div style="background:#F1F8E9;border-left:6px solid {color_g};
                border-radius:10px;padding:20px;text-align:center;">
              <p style="margin:0;color:#555;">Germination Rate</p>
              <h2 style="color:{color_g};margin:6px 0;">{pred_g:.1f}%</h2></div>""", unsafe_allow_html=True)
            st.progress(min(int(pred_g), 100))

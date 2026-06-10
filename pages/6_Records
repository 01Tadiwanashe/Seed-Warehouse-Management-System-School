import streamlit as st
import pandas as pd
import plotly.express as px
import io
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from utils.auth  import require_login, logout_button
from utils.style import inject_style, sidebar_logo
from utils.db    import load_data, save_data

st.set_page_config(page_title="Records", page_icon="📋", layout="wide")
require_login()
inject_style()
sidebar_logo()
logout_button()
st.title("Records and Export")

df = load_data()

st.subheader("Search and Filter")
col1, col2, col3, col4 = st.columns(4)
with col1:
    seed_filter   = st.multiselect("Seed name",    ["All"] + df["seed_name"].unique().tolist(),     default=["All"])
with col2:
    zone_filter   = st.multiselect("Zone",         ["All"] + df["warehouse_zone"].unique().tolist(), default=["All"])
with col3:
    status_filter = st.multiselect("Stock status", ["All"] + df["stock_status"].unique().tolist(),   default=["All"])
with col4:
    alert_filter  = st.multiselect("Alert level",  ["All","Normal","Warning","Critical"],            default=["All"])

col5, col6 = st.columns(2)
with col5:
    date_from = st.date_input("From date", value=pd.to_datetime(df["timestamp"]).min().date())
with col6:
    date_to   = st.date_input("To date",   value=pd.to_datetime(df["timestamp"]).max().date())

search_text = st.text_input("Search lot number, bin ID or supplier", "")

filtered = df.copy()
filtered["timestamp"] = pd.to_datetime(filtered["timestamp"])
filtered = filtered[
    (filtered["timestamp"].dt.date >= date_from) &
    (filtered["timestamp"].dt.date <= date_to)
]
if "All" not in seed_filter and seed_filter:
    filtered = filtered[filtered["seed_name"].isin(seed_filter)]
if "All" not in zone_filter and zone_filter:
    filtered = filtered[filtered["warehouse_zone"].isin(zone_filter)]
if "All" not in status_filter and status_filter:
    filtered = filtered[filtered["stock_status"].isin(status_filter)]
if "All" not in alert_filter and alert_filter:
    filtered = filtered[filtered["overall_alert"].isin(alert_filter)]
if search_text:
    mask = (
        filtered["lot_number"].astype(str).str.contains(search_text, case=False, na=False) |
        filtered["bin_id"].astype(str).str.contains(search_text, case=False, na=False) |
        filtered["supplier_or_customer"].astype(str).str.contains(search_text, case=False, na=False)
    )
    filtered = filtered[mask]

st.markdown(f"**{len(filtered):,} records** match your filters.")

display_cols = [
    "record_id", "timestamp", "seed_name", "variety", "category",
    "warehouse_zone", "bin_id", "lot_number", "quantity_kg", "stock_status",
    "overall_alert", "temperature_c", "humidity_pct", "germination_rate_pct",
    "order_id", "order_type", "quantity_ordered_kg", "supplier_or_customer",
    "dispatch_status", "price_per_kg_usd", "total_order_value_usd",
    "date_received", "expiry_date",
]
st.dataframe(
    filtered[display_cols].sort_values("timestamp", ascending=False),
    use_container_width=True,
    height=380
)

st.markdown("---")
st.subheader("Export Data")
e1, e2, e3 = st.columns(3)
with e1:
    st.download_button(
        "Download Filtered CSV",
        data=filtered[display_cols].to_csv(index=False).encode("utf-8"),
        file_name="warehouse_records.csv",
        mime="text/csv",
        use_container_width=True
    )
with e2:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        filtered[display_cols].to_excel(w, index=False, sheet_name="Records")
        df.groupby("seed_name").agg(
            Total_kg=("quantity_kg", "sum"),
            Avg_germ=("germination_rate_pct", "mean"),
            Records=("record_id", "count")
        ).reset_index().to_excel(w, index=False, sheet_name="Summary")
    st.download_button(
        "Download Filtered Excel",
        data=buf.getvalue(),
        file_name="warehouse_records.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
with e3:
    st.download_button(
        "Download ALL Data CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="warehouse_full_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

st.markdown("---")
st.subheader("Quick Analytics")
if len(filtered) == 0:
    st.warning("No data matches your filters.")
else:
    a1, a2 = st.columns(2)
    with a1:
        vc = filtered["stock_status"].value_counts().reset_index()
        vc.columns = ["Status", "Count"]
        fig = px.bar(vc, x="Status", y="Count", color="Status", text="Count",
                     color_discrete_map={"Optimal":"#2E7D32","Low":"#FF8F00",
                                         "Critical Low":"#C62828","Overstocked":"#1565C0"})
        fig.update_layout(showlegend=False, height=280, margin=dict(t=5),
                          plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig, use_container_width=True)
    with a2:
        st_tots = filtered.groupby("seed_name")["quantity_kg"].sum().reset_index()
        st_tots.columns = ["Seed", "Total kg"]
        fig2 = px.pie(st_tots, names="Seed", values="Total kg", hole=0.35,
                      color_discrete_sequence=["#2E7D32","#C62828","#FF8F00","#1565C0","#6A1B9A"])
        fig2.update_layout(height=280, margin=dict(t=5), paper_bgcolor="white")
        st.plotly_chart(fig2, use_container_width=True)

    a3, a4 = st.columns(2)
    with a3:
        filtered2 = filtered.copy()
        filtered2["month"] = pd.to_datetime(filtered2["timestamp"]).dt.to_period("M").astype(str)
        monthly = filtered2.groupby("month")["total_order_value_usd"].sum().reset_index()
        fig3 = px.line(monthly, x="month", y="total_order_value_usd", markers=True,
                       color_discrete_sequence=["#2E7D32"],
                       labels={"total_order_value_usd": "USD", "month": "Month"})
        fig3.update_layout(height=260, margin=dict(t=5),
                           plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig3, use_container_width=True)
    with a4:
        fig4 = px.histogram(filtered, x="germination_rate_pct", nbins=20, color="seed_name",
                            color_discrete_sequence=["#2E7D32","#C62828","#FF8F00","#1565C0","#6A1B9A"],
                            labels={"germination_rate_pct": "Rate (%)"})
        fig4.update_layout(height=260, margin=dict(t=5),
                           plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("Edit or Delete a Record")
record_ids = filtered["record_id"].tolist()
if record_ids:
    sel_id = st.selectbox("Select record ID", record_ids)
    record = df[df["record_id"] == sel_id].iloc[0]
    with st.expander("Edit selected record"):
        with st.form("edit_form"):
            new_qty   = st.number_input("Quantity (kg)",        value=float(record["quantity_kg"]))
            new_temp  = st.number_input("Temperature (C)",      value=float(record["temperature_c"]))
            new_humid = st.number_input("Humidity (%)",         value=float(record["humidity_pct"]))
            new_germ  = st.number_input("Germination rate (%)", value=float(record["germination_rate_pct"]))
            statuses  = ["Pending","Dispatched","Delivered","Cancelled"]
            cur_s     = record["dispatch_status"] if record["dispatch_status"] in statuses else "Pending"
            new_stat  = st.selectbox("Dispatch status", statuses, index=statuses.index(cur_s))
            save_edit = st.form_submit_button("Save Changes")
            del_btn   = st.form_submit_button("Delete Record", type="secondary")

        if save_edit:
            idx = df[df["record_id"] == sel_id].index[0]
            df.loc[idx, "quantity_kg"]          = new_qty
            df.loc[idx, "temperature_c"]        = new_temp
            df.loc[idx, "humidity_pct"]         = new_humid
            df.loc[idx, "germination_rate_pct"] = new_germ
            df.loc[idx, "dispatch_status"]      = new_stat
            save_data(df)
            st.success(f"Record {sel_id} updated.")
            st.rerun()

        if del_btn:
            df = df[df["record_id"] != sel_id]
            save_data(df)
            st.success(f"Record {sel_id} deleted.")
            st.rerun()

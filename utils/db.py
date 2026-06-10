import pandas as pd
import numpy as np
import os

DATA_PATH     = "data/warehouse.csv"
ORIGINAL_PATH = "data/smart_seed_warehouse_dataset.csv"

def load_data() -> pd.DataFrame:
    path = DATA_PATH if os.path.exists(DATA_PATH) else ORIGINAL_PATH
    df = pd.read_csv(path, parse_dates=["timestamp", "date_received", "expiry_date"])
    return df

def save_data(df: pd.DataFrame):
    os.makedirs("data", exist_ok=True)
    df.to_csv(DATA_PATH, index=False)

def get_next_record_id(df: pd.DataFrame) -> int:
    return int(df["record_id"].max()) + 1 if len(df) > 0 else 1

def compute_stock_status(qty: float, reorder: float, max_cap: float) -> str:
    ratio = qty / max_cap if max_cap > 0 else 0
    if qty <= reorder * 0.5:
        return "Critical Low"
    elif qty <= reorder:
        return "Low"
    elif ratio > 0.95:
        return "Overstocked"
    else:
        return "Optimal"

def compute_alerts(temp: float, humidity: float) -> tuple:
    temp_alert     = "Warning" if temp > 25 or temp < 10 else "Normal"
    humidity_alert = "Warning" if humidity > 70 or humidity < 40 else "Normal"
    if temp_alert == "Warning" and humidity_alert == "Warning":
        overall = "Critical"
    elif temp_alert == "Warning" or humidity_alert == "Warning":
        overall = "Warning"
    else:
        overall = "Normal"
    return temp_alert, humidity_alert, overall

def summary_kpis(df: pd.DataFrame) -> dict:
    return {
        "total_records":      len(df),
        "total_seeds_kg":     df["quantity_kg"].sum(),
        "critical_low":       (df["stock_status"] == "Critical Low").sum(),
        "low_stock":          (df["stock_status"] == "Low").sum(),
        "critical_alerts":    (df["overall_alert"] == "Critical").sum(),
        "warning_alerts":     (df["overall_alert"] == "Warning").sum(),
        "avg_germination":    df["germination_rate_pct"].mean(),
        "pending_dispatches": (df["dispatch_status"] == "Pending").sum(),
        "total_order_value":  df["total_order_value_usd"].sum(),
    }

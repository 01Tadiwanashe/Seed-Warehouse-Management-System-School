import pandas as pd
import numpy as np

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.copy()
    df2["days_to_expiry"]     = (df2["expiry_date"] - df2["timestamp"]).dt.days
    df2["storage_days"]       = (df2["timestamp"] - df2["date_received"]).dt.days
    df2["record_month"]       = df2["timestamp"].dt.month
    df2["record_quarter"]     = df2["timestamp"].dt.quarter
    df2["stock_util_ratio"]   = df2["quantity_kg"] / df2["max_capacity_kg"].replace(0, np.nan)
    df2["reorder_gap"]        = df2["quantity_kg"] - df2["reorder_level_kg"]
    df2["temp_humidity_idx"]  = df2["temperature_c"] * df2["humidity_pct"] / 100
    df2["moisture_co2_ratio"] = df2["moisture_content_pct"] / df2["co2_level_ppm"].replace(0, np.nan)
    df2["order_fill_rate"]    = df2["quantity_ordered_kg"] / df2["quantity_kg"].replace(0, np.nan)
    df2["is_temp_alert"]      = (df2["temp_alert"] == "Warning").astype(int)
    df2["is_humidity_alert"]  = (df2["humidity_alert"] == "Warning").astype(int)
    return df2

# These must match EXACTLY what your notebook trained on
NUMERIC_FEATURES = [
    "quantity_kg", "reorder_level_kg", "max_capacity_kg",
    "temperature_c", "humidity_pct", "moisture_content_pct", "co2_level_ppm",
    "germination_rate_pct", "price_per_kg_usd", "total_order_value_usd",
    "quantity_ordered_kg", "days_to_expiry", "storage_days",
    "record_month", "record_quarter", "stock_util_ratio", "reorder_gap",
    "temp_humidity_idx", "moisture_co2_ratio", "order_fill_rate",
    "is_temp_alert", "is_humidity_alert",
]

CATEGORICAL_FEATURES = ["seed_name", "category", "warehouse_zone", "order_type"]
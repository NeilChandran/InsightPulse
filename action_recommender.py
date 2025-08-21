# action_recommender.py

import pandas as pd
import numpy as np
import re

def recommend_actions(df, query=""):
    """Suggest business actions based on detected patterns in data."""
    recs = []
    # Detect trends in sales, usage, etc.
    num_cols = df.select_dtypes(include="number").columns
    if len(num_cols) == 0:
        return ["Add numeric columns for automated insights."]
    primary = num_cols[0]

    # Trend detection if time column exists
    time_cols = [col for col in df.columns if "date" in col.lower() or "time" in col.lower()]
    if time_cols:
        tcol = time_cols
        try:
            df[tcol] = pd.to_datetime(df[tcol], errors='coerce')
            grouped = df.groupby(df[tcol].dt.to_period('M'))[primary].sum()
            if grouped.iloc[-4:].is_monotonic_increasing and len(grouped.index) > 4:
                recs.append(f"Upsurge detected in {primary}- consider scaling related operations or marketing.")
            elif grouped.iloc[-4:].is_monotonic_decreasing:
                recs.append(f"Recent decline in {primary} - investigate causes, boost demand.")
        except Exception:
            pass

    # Outliers/standout category detection
    obj_cols = df.select_dtypes(include="object").columns
    if obj_cols.any():
        cat = obj_cols[0]
        mode = df[cat].mode() if len(df[cat])>0 else ""
        recs.append(f"Top category for {cat}: {mode}.")

    # Ratio or target alerts
    if primary in df.columns and df[primary].mean() < df[primary].median():
        recs.append(f"Consider adjusting pricing/promotions to increase average {primary}.")

    # Custom queries
    if "inventory" in query.lower():
        if df[primary].min() < 10:
            recs.append("Restock inventory items below 10 units.")
    if not recs:
        recs.append("Upload more data for advanced recommendations.")
    return recs


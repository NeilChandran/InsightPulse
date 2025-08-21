# data_visualizer.py

import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns
import re
import uuid

STATIC_DIR = "static"

def pick_chart_type(query, df):
    # Crude chart type inference
    if 'trend' in query or 'over time' in query or 'date' in ' '.join(df.columns).lower():
        return 'line'
    if 'share' in query or 'proportion' in query or 'distribution' in query:
        return 'pie'
    return 'bar'

def get_chart_columns(query, df):
    # Try to extract two relevant columns: x/category and y/numeric
    numeric_cols = df.select_dtypes(include="number").columns
    other_cols = [c for c in df.columns if c not in numeric_cols and "id" not in c.lower()]
    x = other_cols[0] if other_cols else df.columns
    y = numeric_cols if len(numeric_cols) > 0 else df.columns if len(df.columns) > 1 else df.columns
    return x, y

def generate_visual(df, query):
    chart_type = pick_chart_type(query, df)
    x_col, y_col = get_chart_columns(query, df)
    plt.figure(figsize=(10,6))
    chart_path = os.path.join(STATIC_DIR, f"insightpulse_vis_{uuid.uuid4().hex[:8]}.png")

    try:
        if chart_type == 'bar':
            agg = df.groupby(x_col)[y_col].sum().sort_values(ascending=False).head(8)
            sns.barplot(x=agg.index, y=agg.values)
            plt.title(f"{y_col} by {x_col}")
            plt.xlabel(x_col)
            plt.ylabel(y_col)
        elif chart_type == 'pie':
            agg = df.groupby(x_col)[y_col].sum().sort_values(ascending=False).head(6)
            agg.plot.pie(autopct='%1.1f%%')
            plt.title(f"{y_col} share by {x_col}")
        elif chart_type == 'line':
            if "date" in x_col.lower():
                df[x_col] = pd.to_datetime(df[x_col])
                grouped = df.groupby(x_col)[y_col].sum()
                grouped.sort_index().plot()
                plt.xlabel(x_col)
            else:
                df.iloc[:50].plot(x=x_col, y=y_col)
            plt.title(f"{y_col} trend by {x_col}")
        else:
            df[[x_col,y_col]].head(20).plot(kind='bar', x=x_col, y=y_col)
            plt.title(f"{y_col} by {x_col}")
        plt.tight_layout()
        plt.savefig(chart_path)
        plt.close()
        return chart_path
    except Exception as e:
        return None


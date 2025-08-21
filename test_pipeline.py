# test_pipeline.py

import pandas as pd
from nlp_query_engine import process_query
from data_visualizer import generate_visual
from report_generator import generate_report
from action_recommender import recommend_actions

def run_demo():
    print("==[InsightPulse Test Pipeline]==")
    # Prepare dummy data
    data = {
        'date': pd.date_range("2024-01-01", periods=10, freq='D'),
        'region': ['East', 'West', 'North', 'South', 'East', 'West', 'North', 'South', 'East', 'West'],
        'sales': [100,140,120,90,160,130,115,99,160,140],
        'inventory': [50,60,45,40,99,38,55,70,10,8],
    }
    df = pd.DataFrame(data)
    # Test query
    query = "What is the average sales over time?"
    res, err = process_query(df, query)
    print("Query:", query)
    print("Insight:", res)
    viz_path = generate_visual(df, query)
    print("Chart saved:", viz_path)
    actions = recommend_actions(df, query)
    print("Recommended actions:", actions)
    rpt_path = generate_report(df, query)
    print("PDF report generated:", rpt_path)

if __name__ == "__main__":
    run_demo()


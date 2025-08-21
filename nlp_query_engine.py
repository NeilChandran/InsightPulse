# nlp_query_engine.py

import spacy
import pandas as pd
import re

nlp = spacy.load("en_core_web_sm")

def extract_entities(question):
    """Extract entities (like columns, numbers) from a natural language query."""
    doc = nlp(question)
    entities = [ent.text for ent in doc.ents]
    return entities

def infer_action(question):
    """Basic mapping of question verbs to pandas/statistics actions."""
    if 'average' in question or 'mean' in question:
        return 'mean'
    if 'sum' in question or 'total' in question:
        return 'sum'
    if 'max' in question or 'highest' in question or 'most' in question:
        return 'max'
    if 'min' in question or 'least' in question or 'lowest' in question:
        return 'min'
    if 'count' in question or 'number of' in question:
        return 'count'
    if 'list' in question or 'show' in question:
        return 'show'
    return 'describe'

def get_target_column(query, df):
    # Very simple regex matcher for columns
    colnames = list(df.columns)
    for col in colnames:
        if re.search(col, query, re.IGNORECASE):
            return col
    # Fallback: just pick the first number-like column for demo
    numeric_cols = df.select_dtypes(include="number").columns
    return numeric_cols[0] if len(numeric_cols) > 0 else colnames

def process_query(df, query):
    """Parse the query and run the matching logic on DataFrame"""
    try:
        action = infer_action(query)
        entities = extract_entities(query)
        col = get_target_column(query, df)
        if action == 'mean':
            value = df[col].mean()
            result = f"The average of {col} is {round(value,2)}"
        elif action == 'sum':
            value = df[col].sum()
            result = f"The sum of {col} is {round(value,2)}"
        elif action == 'min':
            value = df[col].min()
            result = f"The minimum of {col} is {round(value,2)}"
        elif action == 'max':
            value = df[col].max()
            result = f"The maximum of {col} is {round(value,2)}"
        elif action == 'count':
            value = df[col].count()
            result = f"The count of {col} is {int(value)}"
        elif action == 'describe':
            stats = df.describe().to_dict()
            result = f"Descriptive stats:\n{stats}"
        elif action == 'show':
            result = df.head(10).to_string(index=False)
        else:
            result = "Query understood, but action not recognized."
        return result, None
    except Exception as e:
        return None, str(e)

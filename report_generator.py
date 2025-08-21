# report_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os
import uuid
from datetime import datetime
from data_visualizer import generate_visual
from action_recommender import recommend_actions
from nlp_query_engine import process_query

REPORT_DIR = "static"

def generate_report(df, query):
    fname = f"insightpulse_report_{uuid.uuid4().hex[:6]}.pdf"
    fpath = os.path.join(REPORT_DIR, fname)
    c = canvas.Canvas(fpath, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1*inch, height-1*inch, "InsightPulse Data Report")
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height-1.3*inch, f"Query: {query}")
    c.drawString(1*inch, height-1.6*inch, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    result, _ = process_query(df, query)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height-2.2*inch, "Summary Insight")
    c.setFont("Helvetica", 11)
    text = c.beginText(1*inch, height-2.6*inch)
    for line in str(result).split("\n"):
        text.textLine(line)
    c.drawText(text)
    
    img_path = generate_visual(df, query)
    if img_path and os.path.isfile(img_path):
        c.drawImage(img_path, 1*inch, height-5.5*inch, width=4.5*inch, height=3*inch, preserveAspectRatio=True)
    
    actions = recommend_actions(df, query)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height-6*inch, "Recommended Actions")
    c.setFont("Helvetica", 11)
    text2 = c.beginText(1*inch, height-6.3*inch)
    for act in (actions if isinstance(actions, list) else [actions]):
        text2.textLine(f"- {act}")
    c.drawText(text2)
    c.showPage()
    c.save()
    return fpath



# main.py

import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import shutil
import uvicorn
import pandas as pd
from nlp_query_engine import process_query
from data_visualizer import generate_visual
from report_generator import generate_report
from action_recommender import recommend_actions

app = FastAPI(title="InsightPulse")

UPLOAD_DIR = "uploaded_data"
STATIC_DIR = "static"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Allow CORS for local testing/dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple homepage with upload form
@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <html>
    <body>
    <h2>InsightPulse: Upload Your CSV File</h2>
    <form action="/upload" enctype="multipart/form-data" method="post">
      <input type="file" name="datafile"/>
      <input type="submit"/>
    </form>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Upload endpoint for CSV files
@app.post("/upload")
async def upload_datafile(datafile: UploadFile = File(...)):
    if not datafile.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")
    file_path = os.path.join(UPLOAD_DIR, datafile.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(datafile.file, buffer)
    return {"message": "File uploaded successfully.", "filename": datafile.filename}

# Endpoint for running queries
@app.post("/query")
async def query_data(filename: str = Form(...), query: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    df = pd.read_csv(file_path)
    result, error = process_query(df, query)
    if error:
        return {"error": error}
    chart_path = generate_visual(df, query)
    actions = recommend_actions(df, query)
    return {
        "result": result,
        "visual": chart_path,
        "recommended_actions": actions
    }

# Download latest report for analysis
@app.get("/download_report")
async def download_report(filename: str, query: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    df = pd.read_csv(file_path)
    report_path = generate_report(df, query)
    return FileResponse(report_path, filename=os.path.basename(report_path), media_type="application/pdf")

# Serve static files (e.g., generated plots)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

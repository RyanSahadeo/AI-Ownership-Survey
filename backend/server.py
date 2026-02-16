"""
FastAPI Server Wrapper for Streamlit Application
This serves as a proxy to run Streamlit on port 8001
"""
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
import os
import subprocess
import threading
import time

app = FastAPI(title="POQ Survey Platform")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start Streamlit in background
def start_streamlit():
    """Start Streamlit application on port 8501"""
    subprocess.run([
        "/root/.venv/bin/streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--browser.gatherUsageStats", "false"
    ], cwd="/app/backend")

# Start Streamlit in a background thread
streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
streamlit_thread.start()

@app.get("/")
async def root():
    """Redirect to Streamlit application"""
    return RedirectResponse(url="http://localhost:8501")

@app.get("/api")
async def api_root():
    return {"message": "POQ Survey Platform API", "status": "running", "streamlit_port": 8501}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "application": "POQ Survey Platform"}

"""
FastAPI wrapper that proxies to Streamlit
POQ Survey Platform - Capitol Technology University
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.background import BackgroundTask
import httpx
import os
import subprocess
import threading
import time
import asyncio

app = FastAPI(title="POQ Survey Platform")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STREAMLIT_URL = "http://127.0.0.1:8501"

# HTTP client for proxying
client = httpx.AsyncClient(timeout=300.0)

@app.on_event("startup")
async def startup_event():
    """Start Streamlit on startup"""
    def run_streamlit():
        subprocess.Popen([
            "/root/.venv/bin/streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "127.0.0.1",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ], cwd="/app/backend", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Check if Streamlit is already running
    try:
        response = httpx.get(f"{STREAMLIT_URL}/healthz", timeout=2.0)
        if response.status_code == 200:
            print("Streamlit already running")
            return
    except:
        pass
    
    thread = threading.Thread(target=run_streamlit, daemon=True)
    thread.start()
    
    # Wait for Streamlit to start
    for _ in range(30):
        try:
            response = httpx.get(f"{STREAMLIT_URL}/healthz", timeout=2.0)
            if response.status_code == 200:
                print("Streamlit started successfully")
                return
        except:
            pass
        time.sleep(1)
    print("Warning: Streamlit may not have started properly")

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy(request: Request, path: str):
    """Proxy all requests to Streamlit"""
    url = f"{STREAMLIT_URL}/{path}"
    
    # Add query parameters
    if request.query_params:
        url = f"{url}?{request.query_params}"
    
    headers = dict(request.headers)
    headers.pop("host", None)
    
    # Handle WebSocket upgrade for Streamlit
    if "upgrade" in headers.get("connection", "").lower():
        return RedirectResponse(url=url)
    
    try:
        body = await request.body()
        
        response = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
            follow_redirects=True
        )
        
        # Filter response headers
        response_headers = dict(response.headers)
        response_headers.pop("transfer-encoding", None)
        response_headers.pop("content-encoding", None)
        
        return StreamingResponse(
            iter([response.content]),
            status_code=response.status_code,
            headers=response_headers,
            media_type=response.headers.get("content-type")
        )
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <html>
            <head><title>POQ Survey Loading...</title></head>
            <body style="font-family: Arial; text-align: center; padding-top: 50px;">
                <h2>Loading POQ Survey Platform...</h2>
                <p>Please wait while the application starts.</p>
                <p><a href="/" onclick="setTimeout(function(){{location.reload()}}, 2000)">Click here to refresh</a></p>
            </body>
            </html>
            """,
            status_code=503
        )

@app.get("/api/health")
async def health():
    return {"status": "healthy", "app": "POQ Survey Platform"}

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.api.v1.router import api_router

app = FastAPI(title="Study Space Booking API")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root(request: Request):
    accept = request.headers.get("accept", "")
    if "text/html" in accept:
        html = """
        <!doctype html>
        <html>
        <head><title>Study Space Booking API</title></head>
        <body>
          <h1>Study Space Booking API</h1>
          <p>Backend is running.</p>
          <ul>
            <li><a href="/docs">API docs</a></li>
            <li><a href="/openapi.json">OpenAPI JSON</a></li>
            <li><a href="/api/v1">API v1 root</a></li>
          </ul>
        </body>
        </html>
        """
        return HTMLResponse(content=html, status_code=200)
    return JSONResponse({"message": "Backend is running."})
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.api.routes import router as api_router
import os

app = FastAPI(
    title="Digital Twin & RAG Agent",
    description="AI-powered Digital Twin for Electricity Assets",
    version="1.0.0"
)

# Mount API routes
app.include_router(api_router, prefix="/api")

# Setup UI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


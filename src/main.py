from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.api.routes import router as api_router
from src.ingestion.stream_processor import stream_processor
from contextlib import asynccontextmanager
import asyncio
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Run Stream Processor in background
    task = asyncio.create_task(stream_processor.start_stream())
    print("System: Live Data Stream Started.")
    yield
    # Shutdown
    stream_processor.stop()
    print("System: Stream Stopped.")

app = FastAPI(
    title="Digital Twin & RAG Agent",
    description="AI-powered Digital Twin for Electricity Assets",
    version="1.0.0",
    lifespan=lifespan
)


# Mount API routes
app.include_router(api_router, prefix="/api")

# Setup UI
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")



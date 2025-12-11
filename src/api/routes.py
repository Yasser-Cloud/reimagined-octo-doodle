from fastapi import APIRouter, Request, WebSocket
from src.rag.engine import rag_engine
from src.digital_twin.grid_model import grid_twin
from src.ingestion.stream_processor import stream_processor
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Main Chat Interface.
    """
    result = rag_engine.process_query(request.query)
    return result

@router.get("/grid/status")
async def get_grid_status():
    """
    Returns the current snapshot of the Digital Twin.
    """
    return grid_twin.get_system_status()

@router.post("/grid/simulate")
async def trigger_simulation(scenario: str = "overload"):
    """
    Injects a fault/scenario into the twin.
    """
    grid_twin.inject_anomaly(scenario)
    return {"status": "Anomaly Injected", "scenario": scenario}

# Websocket for Live Data Streaming
@router.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        # Define a callback to push data to this socket
        async def send_data(data):
            await websocket.send_json(data)
            
        # Start the stream processor if not running (Simulation)
        # In a real app, this would be a broadcast manager
        if not stream_processor.running:
           # We run the stream as a background task handled by Main, 
           # but for this demo, we'll just hook into the loop or rely on a shared state.
           # To keep it simple, the stream runs globally, and we subscribe.
           pass 
           
        # For this MVP, we'll just loop here sending data from the source
        while True:
            import asyncio
            # Get latest from the singleton
            status = grid_twin.get_system_status()
            await websocket.send_json(status)
            await asyncio.sleep(1)
            
    except Exception as e:
        print(f"WS Error: {e}")
    finally:
        pass


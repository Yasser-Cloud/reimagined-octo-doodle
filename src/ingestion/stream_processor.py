import asyncio
import random
import json
from datetime import datetime
from src.digital_twin.grid_model import grid_twin
from src.digital_twin.asset_models import asset_manager

class StreamMock:
    """
    Simulates a Real-Time Data Stream (e.g. from Kafka/MQTT).
    Generates 1-second interval telemetry for the Station.
    """
    def __init__(self):
        self.running = False

    async def start_stream(self, callback_ws=None):
        self.running = True
        print("Data Stream Started...")
        while self.running:
            # 1. Generate Telemetry
            telemetry = self._generate_data()
            
            # 2. Feed Digital Twin (Network)
            # In a real app, this would be `grid_twin.update_state(telemetry)`
            # Here we just tick the simulation
            grid_twin.tick()
            network_status = grid_twin.get_system_status()
            
            # 3. Feed Asset Twins (Physical)
            # Use data from the Network Twin (Load) + Simulated Asset Sensors (Temp)
            t1_load = network_status["transformer_loading_percent"]
            
            # Simulate Oil Temp correlation with Load
            sim_oil_temp = 40 + (t1_load * 0.5) + random.uniform(-2, 2)
            
            asset_data = {
                "load_percent": t1_load,
                "oil_temp": sim_oil_temp,
                "vibration": random.uniform(0.1, 1.2),
                "h2_ppm": random.uniform(5, 15)
            }
            
            health_status = asset_manager.process_telemetry("T1_Transformer", asset_data)
            
            # 4. Push to UI/Websocket
            payload = {
                "timestamp": datetime.now().isoformat(),
                "grid": network_status,
                "assets": {"T1_Transformer": {**asset_data, **health_status}}
            }
            
            if callback_ws:
                await callback_ws(payload)
                
            await asyncio.sleep(1) # 1Hz Data Rate

    def _generate_data(self):
        return {} # Placeholder for raw SCADA frames

    def stop(self):
        self.running = False

stream_processor = StreamMock()

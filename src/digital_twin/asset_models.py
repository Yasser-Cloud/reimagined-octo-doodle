from datetime import datetime
import random

class AssetHealthModel:
    def __init__(self, asset_id: str):
        self.asset_id = asset_id
        self.health_score = 100.0 # 0-100%
        self.last_update = datetime.now()

    def update(self, sensor_data: dict):
        pass

class TransformerHealth(AssetHealthModel):
    """
    Detailed physical model for a High Voltage Transformer.
    Inputs: Load, Oil Temperature, Vibration, Dissolved Gas (Hydrogen - H2).
    Outputs: Health Score, Estimated Remaining Life.
    """
    def __init__(self, asset_id: str):
        super().__init__(asset_id)
        # Baseline physical parameters
        self.max_oil_temp = 90.0 # Celsius
        self.max_vib = 5.0 # mm/s
        self.max_h2 = 100 # ppm

    def update(self, sensor_data: dict):
        """
        Calculates health based on weighted sensor inputs.
        Real world: This would be the "DGA" (Dissolved Gas Analysis) algorithm.
        """
        self.last_update = datetime.now()
        
        # Unpack data
        load = sensor_data.get("load_percent", 0.0)
        temp = sensor_data.get("oil_temp", 40.0)
        vib = sensor_data.get("vibration", 0.5)
        h2 = sensor_data.get("h2_ppm", 10.0)

        # 1. Temperature Impact (Arrhenius equation simplified)
        # Every 10C rise above max halves life (simulated as score drop)
        temp_factor = 1.0
        if temp > self.max_oil_temp:
            temp_factor = 0.95 # Rapid degradation
        elif temp > 80:
            temp_factor = 0.99
            
        # 2. Vibration Impact (Mechanical looseness)
        vib_factor = 1.0
        if vib > self.max_vib:
            vib_factor = 0.9
            
        # 3. Electrical/Chemical Impact (Gases)
        gas_factor = 1.0
        if h2 > self.max_h2:
            gas_factor = 0.8
            
        # Composite Update
        # Decay health if stressed, recover slightly if rested (simulating maintenance? No, health usually only goes down unless fixed)
        # For this demo, we make it dynamic (it's a score of Current Condition)
        
        current_condition = 100.0
        if temp > 85 or h2 > 50:
            current_condition -= 20
        if temp > 95 or h2 > 100:
            current_condition -= 40
            
        self.health_score = max(0.0, current_condition)
        
        return {
            "asset_id": self.asset_id,
            "health_score": self.health_score,
            "status": "Critical" if self.health_score < 40 else "Good"
        }

# Factory
class AssetManager:
    def __init__(self):
        self.assets = {
            "T1_Transformer": TransformerHealth("T1_Transformer")
        }
        
    def process_telemetry(self, asset_id, data):
        if asset_id in self.assets:
            return self.assets[asset_id].update(data)
        return None

asset_manager = AssetManager()

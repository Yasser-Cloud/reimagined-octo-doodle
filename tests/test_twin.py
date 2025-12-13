from src.digital_twin.grid_model import NetworkTwin
from src.digital_twin.asset_models import TransformerHealth

def test_network_twin_initialization():
    twin = NetworkTwin()
    assert twin.network is not None
    # Check if we have our specific assets
    assert "T1_Transformer" in twin.network.transformers.index
    assert "HV_Grid_Bus" in twin.network.buses.index

def test_network_power_flow():
    twin = NetworkTwin()
    status_initial = twin.get_system_status()
    # It should have some load
    assert status_initial["total_load_mw"] > 0
    
    # Tick should change values (random noise)
    twin.tick()
    status_next = twin.get_system_status()
    assert status_next["timestamp"] > status_initial["timestamp"]

def test_transformer_health_model():
    # Good condition
    t1 = TransformerHealth("Test_T1")
    health = t1.update({"load_percent": 50, "oil_temp": 60, "h2_ppm": 10})
    assert health["health_score"] == 100.0
    assert health["status"] == "Good"

    # Critical condition
    health_crit = t1.update({"load_percent": 120, "oil_temp": 110, "h2_ppm": 200})
    assert health_crit["health_score"] < 50.0

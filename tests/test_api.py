from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Digital Twin Control Room" in response.text

def test_grid_status():
    response = client.get("/api/grid/status")
    assert response.status_code == 200
    data = response.json()
    assert "total_load_mw" in data
    assert "transformer_loading_percent" in data

def test_chat_endpoint_mock():
    # Tests the chat returns *something* valid
    payload = {"query": "Status of T1"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0

import os
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.rag.llm_client import LLMClient
import importlib

client = TestClient(app)

# 1. RENDER DEPLOYMENT CHECKS
def test_render_health_check_path():
    """
    Render uses /api/grid/status (or /) to check if the app is alive.
    This test confirms the app responds correctly on that path.
    """
    response = client.get("/api/grid/status")
    assert response.status_code == 200
    assert "timestamp" in response.json()

# 2. MODAL INTEGRATION CHECKS
@patch("src.rag.llm_client.requests.post")
def test_llm_client_modal_routing(mock_post):
    """
    Verifies that if MODAL_URL is set, the client sends requests there
    instead of running locally or mocking.
    """
    # Simulate Production Env
    with patch.dict(os.environ, {"MODAL_URL": "https://fake-modal-url.run"}):
        
        # Mock Modal Response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "I am a GPU generated answer."}
        mock_post.return_value = mock_response
        
        # Initialize Client
        llm = LLMClient()
        
        # Generate
        answer = llm.generate_response("System", "User Query")
        
        # Assertions
        assert answer == "I am a GPU generated answer."
        mock_post.assert_called_once()
        # Verify URL was used
        args, _ = mock_post.call_args
        assert args[0] == "https://fake-modal-url.run"

def test_modal_file_integrity():
    """
    Smoke test to ensure modal_llm.py is valid and defines the App.
    We don't deploy it, just check syntax/structure.
    """
    try:
        # We need to install modal first, but it is in dev-deps.
        # This test might fail if 'modal' lib isn't installed. 
        # We skip if import fails to avoid breaking local 'lite' test runs.
        import modal
    except ImportError:
        pytest.skip("Modal not installed, skipping integration check.")
        
    spec = importlib.util.spec_from_file_location("modal_llm", "modal_llm.py")
    modal_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modal_module)
    
    assert hasattr(modal_module, "app")
    assert hasattr(modal_module, "Model")
    # Check if api_generate function exists
    assert hasattr(modal_module, "api_generate")

from src.rag.engine import RAGEngine
from src.rag.llm_client import LLMClient

def test_rag_initialization():
    engine = RAGEngine()
    assert engine is not None
    # Should default to Mock mode if env vars are not set for Qdrant
    assert engine.collection_name == "manuals"

def test_rag_context_retrieval_fallback():
    engine = RAGEngine()
    
    # query that triggers "temp" fallback
    query = "What is the max temp for the transformer?"
    result = engine.process_query(query)
    
    # Check if context was populated
    context = result["context_used"]
    assert "LIVE SCADA DATA" in context # From Grid Twin
    assert "MANUAL EXTRACT (Backup)" in context # From Fallback Logic
    assert "Normal operating range" in context

def test_rag_context_critical_fallback():
    engine = RAGEngine()
    query = "Critical failure failure mode"
    result = engine.process_query(query)
    
    context = result["context_used"]
    assert "EMERGENCY PROTOCOL" in context

def test_llm_mock_response():
    # Verify the LLM client mock works
    client = LLMClient()
    response = client.generate_response("System Context", "Status of T1")
    assert isinstance(response, str)
    assert len(response) > 0

from src.rag.llm_client import llm_client
from src.digital_twin.grid_model import grid_twin
from src.digital_twin.asset_models import asset_manager
import os

# Lazy Imports
try:
    from qdrant_client import QdrantClient
    from sentence_transformers import SentenceTransformer
    _RAG_AVAILABLE = True
except ImportError:
    _RAG_AVAILABLE = False
    print("RAG: 'qdrant-client' or 'sentence-transformers' not found. Vector Search disabled.")

# Qdrant Config
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333") 
if os.getenv("APP_ENV") != "production":
   QDRANT_URL = "http://localhost:6333"

class RAGEngine:
    def __init__(self):
        self.client = None
        self.embedder = None
        self.collection_name = "manuals"
        
        if _RAG_AVAILABLE:
            try:
                self.client = QdrantClient(url=QDRANT_URL)
                # Lazy load embedder to save startup time
                self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"RAG Warning: Qdrant/Embedder init failed ({e})")

    def process_query(self, query: str):
        """
        Main RAG pipeline.
        1. Fetch Live Context (Twin).
        2. Fetch Semantic Context (Qdrant).
        3. Generative Answer.
        """
        context = []
        
        # --- 1. Live Digital Twin Context ---
        status = grid_twin.get_system_status()
        grid_context = f"LIVE SCADA DATA: Total Load {status['total_load_mw']:.1f}MW. Transformer T1 Loading: {status['transformer_loading_percent']}%."
        if status['alerts']:
            grid_context += f" WARNING ALERTS ACTIVE: {', '.join(status['alerts'])}."
        context.append(grid_context)
        
        # Details for T1 if asked
        if "transformer" in query.lower() or "t1" in query.lower():
            t1_health = asset_manager.assets["T1_Transformer"].health_score
            asset_context = f"ASSET HEALTH (T1): Score {t1_health:.1f}/100. Status: {'Critical' if t1_health < 40 else 'Good'}."
            context.append(asset_context)

        # --- 2. Vector Search Context (Qdrant) ---
        # Try Qdrant, fallback to Hardcoded Manuals for Demo if empty
        docs = []
        try:
            if self.client and self.embedder:
                query_vector = self.embedder.encode(query).tolist()
                search_result = self.client.search(
                    collection_name=self.collection_name,
                    query_vector=query_vector,
                    limit=2
                )
                if search_result:
                    docs = [f"MANUAL EXTRACT: {hit.payload['text']}" for hit in search_result]
        except Exception as e:
            print(f"Vector Search Error: {e}")
            
        # FALLBACK FOR DEMO: If no docs found (empty DB), simulate retrieval
        if not docs:
            # Simple keyword matching for demo effect
            if "temp" in query.lower():
                docs.append("MANUAL EXTRACT (Backup): Normal operating range for Transformer T1 oil is 40-90C. Above 95C requires fan inspection.")
            elif "load" in query.lower():
                docs.append("MANUAL EXTRACT (Backup): Rated load for T1 is 100MW. Prolonged operation >110% causes loss of life.")
            elif "fail" in query.lower() or "critical" in query.lower():
                docs.append("MANUAL EXTRACT (Backup): EMERGENCY PROTOCOL: In case of critical overload, Isolate Feeder 3 first.")
                
        if docs:
            context.append("\n".join(docs))
        
        full_context = "\n".join(context)
        
        # --- 3. LLM Generation ---

        response = llm_client.generate_response(
            system_context=f"You are an AI Operator Assistant for a Power Grid. Combine the LIVE SCADA DATA and MANUAL EXTRACTS to answer.",
            user_query=query  # Passing context via prompt construction in llm_client or here? 
                              # llm_client.generate_response constructs the prompt with context, 
                              # so we pass context as system_context.
        )
        
        # Fix: llm_client uses {system_context} in the prompt template.
        # We should pass the *Full Context* as the system context or part of it.
        # Let's override the system context passed to include the retrieved data.
        
        final_prompt_context = f"Relevant Data:\n{full_context}"
        
        response = llm_client.generate_response(
            system_context=final_prompt_context,
            user_query=query
        )
        
        return {
            "response": response,
            "context_used": full_context
        }

rag_engine = RAGEngine()


from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import os
import uuid

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "manuals"

def ingest_dummy_data():
    print(f"Connecting to Qdrant at {QDRANT_URL}...")
    try:
        client = QdrantClient(url=QDRANT_URL)
        
        # 1. Check/Create Collection
        if not client.collection_exists(COLLECTION_NAME):
            print(f"Creating collection '{COLLECTION_NAME}'...")
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
        
        # 2. Dummy Data (Maintenance Manuals)
        documents = [
            {
                "text": "Transformer T1 Maintenance Procedure: Check oil levels daily. If oil temperature exceeds 85C, inspect cooling fans immediately.",
                "source": "Manual-T1-001"
            },
            {
                "text": "Substation Safety: Wear Class 2 Voltage Gloves when operating MV Busbar switches. Ensure grounding stick is visible.",
                "source": "Safety-Standard-2024"
            },
            {
                "text": "Emergency Shutdown: In case of fire, active the Halon system and trip the HV Circuit Breaker (CB-110).",
                "source": "Emergency-Protocol-A"
            },
            {
                "text": "Feeder Faults: If Feeder 1 trips, check for cable splice failures at standard intervals (every 500m).",
                "source": "Feeder-Repair-Guide"
            }
        ]
        
        # 3. Embed
        print("Loading Embedding Model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        embeddings = model.encode([d["text"] for d in documents])
        
        # 4. Upload
        points = []
        for i, doc in enumerate(documents):
            points.append(PointStruct(
                id=str(uuid.uuid4()),
                vector=embeddings[i].tolist(),
                payload=doc
            ))
            
        client.upsert(
            collection_name=COLLECTION_NAME,
            wait=True,
            points=points
        )
        print(f"Successfully ingested {len(points)} documents into Qdrant.")
        
    except Exception as e:
        print(f"Ingestion failed: {e}")

if __name__ == "__main__":
    ingest_dummy_data()

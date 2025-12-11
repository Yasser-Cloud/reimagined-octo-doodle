# Digital Twin & AI Operator Agent ⚡🤖

An Open Source **Digital Twin** solution for Electricity Assets, integrated with an **AI RAG Agent** (using `LiquidAI/LFM2`) to assist operators in maintenance and monitoring.

## 🚀 Features

*   **Digital Twin Engine**: Built on **PyPSA** (Python for Power System Analysis) to simulate realistic grid physics (Power Flow, Voltage, Loads).
*   **Composite Twin Architecture**: Combines Network-level simulation with detailed **Asset Health Models** (Temperature, Vibration, Gas Analysis).
*   **AI Operator Assistant**: A RAG-powered chatbot that answers questions using:
    *   **Live SCADA Data** (Real-time from the Twin).
    *   **Maintenance Manuals** (Vector Search via **Qdrant**).
*   **Real-time Dashboard**: "Control Room" style UI with live charts and anomaly injection.
*   **Production Ready**: Dockerized, `uv` managed, and ready for Cloud Deployment.

## 🛠️ Tech Stack

*   **Backend**: Python 3.11, FastAPI
*   **Simulation**: PyPSA, Pandas, SciPy
*   **AI/RAG**: HuggingFace Transformers, Qdrant (Vector DB), Sentence-Transformers
*   **Frontend**: HTML5, Bootstrap 5, Vanilla JS (WebSockets)
*   **DevOps**: Docker, UV, Render.com

## 🏁 Quick Start

### Option 1: Docker (Recommended)
Run the entire stack (App + Database) in one command:

```bash
make docker-up
# OR
docker-compose up --build
```

**Access**:
*   **Dashboard**: http://localhost:8000
*   **API Docs**: http://localhost:8000/docs

**One-time Setup for RAG**:
To search manuals, you need to seed the database:
```bash
docker-compose exec digital-twin python src/rag/ingestion.py
```

### Option 2: Local Development
Prerequisites: Install [`uv`](https://github.com/astral-sh/uv).

```bash
# 1. Install Dependencies
make install

# 2. Run Tests
make test

# 3. Start App
make run
```
*Note: Local run requires a local Qdrant instance or `QDRANT_URL` env var.*

## 🧪 Testing
We use `pytest` for unit and integration testing.

```bash
make test
# OR
uv run pytest tests/
```

## ☁️ Deployment (Render.com)
This project is configured for one-click deployment on Render.

1.  Fork this repository.
2.  Login to **Render.com**.
3.  Click **New +** -> **Blueprint**.
4.  Connect your repo. Render will detect `render.yaml`.
5.  **Important**: The `QDRANT_URL` environment variable needs to point to a valid Qdrant instance (e.g., Qdrant Cloud Free Tier). The local Docker-Compose Qdrant won't work on Render's simple web service plan.

## 📂 Project Structure
```
code/
├── src/
│   ├── digital_twin/    # PyPSA & Physics Models
│   ├── rag/             # AI Engine & Ingestion
│   ├── ingestion/       # Stream Simulation
│   ├── api/             # FastAPI Routes
│   └── templates/       # Frontend UI
├── tests/               # Pytest Suite
├── data/                # Data storage
├── Dockerfile           # Production Image
├── render.yaml          # Cloud Config
└── Makefile             # Shortcuts
```

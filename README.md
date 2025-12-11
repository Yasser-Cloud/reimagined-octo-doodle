# Digital Twin & AI Maintenance for Electricity Assets

This project implements a Digital Twin solution for an electricity grid, integrated with a local RAG AI system for asset maintenance.

## Tech Stack
- **Digital Twin**: Eclipse Ditto (via Docker), OpenDSS
- **AI/RAG**: LiquidAI/LFM2-1.2B-RAG (Local LLM)
- **Backend**: Python (managed by `uv`)
- **Infrastructure**: Docker

## Getting Started

### Prerequisites
- `uv` installed
- Docker installed (for Eclipse Ditto)

### Setup
```bash
uv sync
uv run python src/main.py
```

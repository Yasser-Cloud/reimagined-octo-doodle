# Makefile

.PHONY: help install install-ai run test lint format docker-build docker-up clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install LITE dependencies (FastAPI + Digital Twin)"
	@echo "  make install-ai - Install FULL dependencies (AI + RAG + Torch)"
	@echo "  make clean      - Clean cache to free space"
	@echo "  make run        - Run local dev server"

install:
	uv sync

install-ai:
	uv sync --extra ai

deploy-ai:
	uv run modal deploy modal_llm.py

clean:

	uv cache clean
	rm -rf .venv

run:
	uv run uvicorn src.main:app --reload

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/

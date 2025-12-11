# Makefile

.PHONY: help install run test lint format docker-build docker-up

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies with uv"
	@echo "  make run        - Run local dev server"
	@echo "  make test       - Run tests with pytest"
	@echo "  make lint       - Lint code (ruff/flake8)"
	@echo "  make docker-up  - Run with Docker Compose"

install:
	uv sync

run:
	uv run uvicorn src.main:app --reload

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check src/

format:
	uv run ruff format src/

docker-build:
	docker-compose build

docker-up:
	docker-compose up

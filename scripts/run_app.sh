#!/bin/bash

set -e

echo start migrations
uv run --no-sync alembic upgrade head
# /app/.venv/bin/alembic upgrade head

echo start uvicorn
uv run --no-sync uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# /app/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
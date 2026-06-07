#!/bin/bash

echo start migrations
./.venv/bin/alembic upgrade head

echo start uvicorn
./.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
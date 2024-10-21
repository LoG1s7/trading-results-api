#!/bin/sh

set -e

#echo "Make Alembic migrations..."
#alembic revision --autogenerate
#
#echo "Running Alembic migrations..."
#alembic upgrade head

#echo "Starting parser..."
#python -m src.parser

echo "Starting Uvicorn..."
poetry run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

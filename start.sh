#! /usr/bin/env bash

# python -m payroll.cli database init
timestamp=$(date +"%Y-%m-%d_%H-%M-%S")

poetry run alembic revision --autogenerate -m "revision_$timestamp"

poetry run alembic upgrade head

uvicorn payroll.main:app --host 0.0.0.0 --port 8000

#! /usr/bin/env bash

# python -m payroll.cli database init
poetry run alembic upgrade head

uvicorn payroll.main:app --host 0.0.0.0 --port 8000

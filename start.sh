#! /usr/bin/env bash

poetry run alembic upgrade head

uvicorn app.main:app --host 0.0.0.0 --port 8000

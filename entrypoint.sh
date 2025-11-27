#!/bin/bash

# Применение миграций
alembic upgrade head

exec uvicorn main:app --reload --host 127.0.0.1 --port 8000 --log-level debug
#!/usr/bin/env bash
cd ..
alembic upgrade head
cd app
uvicorn main:app --host 0.0.0.0 --port 80 --reload

#!/usr/bin/env bash
cd ..
alembic upgrade head
cd app
gunicorn main:app -b unix:/app-socket/async.sock -w 4 -k uvicorn.workers.UvicornWorker
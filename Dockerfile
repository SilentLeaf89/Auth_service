#syntax=docker/dockerfile:1.4

FROM python:3.11-slim

ENV DOCKER_ENV=true

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

COPY ./alembic.ini /alembic.ini
COPY ./alembic /alembic

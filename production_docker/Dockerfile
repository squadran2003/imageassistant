# Multi-stage build: Frontend first
FROM node:18-slim AS frontend-builder

# Build frontend
WORKDIR /usr/src/app/frontend
COPY ./imageassistant/frontend/package*.json ./
RUN npm ci 
COPY ./imageassistant/frontend/ ./
RUN npm run build

# Main Python application
FROM python:3.10-slim-bullseye

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# change <botify> to your project name
WORKDIR /usr/src/imageassistant/

COPY ./pyproject.toml ./poetry.lock ./

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi --no-root
# set the working directory to where the manage.py file is located

# Copy project files
COPY ./ /usr/src/imageassistant/

# Copy built frontend files from frontend-builder stage (overwrite the old ones)
COPY --from=frontend-builder /usr/src/app/templates/ /usr/src/imageassistant/imageassistant/templates/
COPY --from=frontend-builder /usr/src/app/assets/ /usr/src/imageassistant/imageassistant/assets/

WORKDIR /usr/src/imageassistant/imageassistant/
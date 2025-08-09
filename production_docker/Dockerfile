# Multi-stage build: Frontend first
FROM node:18-slim AS frontend-builder

# Build frontend
WORKDIR /usr/src/app/frontend
COPY ./imageassistant/frontend/package*.json ./
RUN npm ci 
COPY ./imageassistant/frontend/ ./
ENV NODE_ENV=production
ENV VUE_APP_STATIC_URL=https://d203745bu6qd7u.cloudfront.net/static/
RUN npm run build:vue && echo "Build completed, listing dist folder:" && ls -la dist/ && echo "Files in dist:" && find dist/ -type f

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

# Copy built frontend files from frontend-builder stage
COPY --from=frontend-builder /usr/src/app/frontend/dist/ /usr/src/imageassistant/imageassistant/assets/
COPY --from=frontend-builder /usr/src/app/frontend/dist/index.html /usr/src/imageassistant/imageassistant/templates/


WORKDIR /usr/src/imageassistant/imageassistant/
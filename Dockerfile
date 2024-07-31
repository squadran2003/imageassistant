FROM python:3.10.13-bullseye


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# change <botify> to your project name
WORKDIR /usr/src/imageassistant/

COPY pyproject.toml poetry.lock ./


RUN pip install poetry



RUN poetry config virtualenvs.create false \
    && poetry lock --no-update && poetry install --only main --no-interaction --no-ansi

# set the working directory to where the manage.py file is located
WORKDIR /usr/src/imageassistant/imageassistant/

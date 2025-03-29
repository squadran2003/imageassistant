FROM python:3.10.13-bullseye


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# change <botify> to your project name
RUN mkdir /usr/src/imageassistant/
WORKDIR /usr/src/imageassistant/




COPY pyproject.toml poetry.lock ./


# install open cv for debian
RUN apt-get update -y || (apt-get clean && apt-get update -y) && \
    apt-get install -y --no-install-recommends libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip install "poetry==2.0.0" \
    && pip --version




RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi --no-root


# set the working directory to where the manage.py file is located
WORKDIR /usr/src/imageassistant/imageassistant/


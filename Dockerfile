FROM python:3.11.6-slim-bullseye as iot_smart_home

RUN pip install poetry==1.4.2

RUN apt-get update -y && apt-get install tcpdump -y

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false

RUN poetry install -n

COPY . /app/
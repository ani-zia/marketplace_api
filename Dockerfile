
FROM python:3.10 AS base_build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN pip install poetry==1.3.2

WORKDIR /app

COPY . .

RUN poetry config virtualenvs.create false && poetry install --with prod

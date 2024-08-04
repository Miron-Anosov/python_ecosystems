FROM python:3.12-slim-bullseye AS builder
LABEL authors="mairon26rus@gmail.com"

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential libpq-dev curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME=/opt/poetry

ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3

RUN poetry config virtualenvs.create false --local
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-dev
COPY ./app /app/app

FROM python:3.12-slim-bullseye
WORKDIR /app/app/
COPY --from=builder /app /app
COPY --from=builder /usr/local/ /usr/local/

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app", "--access-logfile=-"]
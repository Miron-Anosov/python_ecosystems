FROM python:3.12-slim-bullseye AS builder
LABEL authors="mairon26rus@gmail.com"

WORKDIR /app
COPY ./app /app/
COPY pyproject.toml poetry.lock* /app/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential libpq-dev  && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip
RUN python -m pip install poetry==1.8

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-dev --verbose



FROM python:3.12-slim-bullseye
WORKDIR /app

COPY --from=builder /app /app
ENV VIRTUAL_ENV=/app/.venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app", "--access-logfile=-"]


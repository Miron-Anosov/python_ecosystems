FROM ubuntu:latest
LABEL authors="miron"

COPY requirements.txt /app/
COPY application_flask.py /app/
COPY sentry_install.bash /sentry/

RUN pip install -r /app/requirements.txt
RUN bash /sentry/sentry_install.bash

WORKDIR /app/
CMD ["python3", "-m", "application_flask.py"]

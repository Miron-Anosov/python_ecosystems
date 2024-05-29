FROM python:3.12-slim
LABEL authors="miron" version="0.1"

RUN apt-get update && \
    apt-get install -y python3-pip

COPY requirements.txt /app/
COPY application_flask.py /app/

RUN pip install -r /app/requirements.txt

WORKDIR /app/
CMD ["python3.12", "-m", "application_flask", "--host=0.0.0.0"]

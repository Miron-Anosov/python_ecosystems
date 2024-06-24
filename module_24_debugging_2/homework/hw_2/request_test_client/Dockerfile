FROM python:3.12-slim
LABEL authors="miron" version="0.1"

RUN apt-get update && \
    apt-get install -y python3-pip

COPY requirements.txt /test_client/
COPY run.py /test_client/run.py

RUN pip install -r /test_client/requirements.txt

WORKDIR /test_client/
CMD ["python3.12", "-m", "run"]

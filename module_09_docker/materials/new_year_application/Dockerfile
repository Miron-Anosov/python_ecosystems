FROM python:3.11.0-slim

LABEL OWNER=ANOSOV_MIRON

WORKDIR /new_year_application/

COPY  . .

EXPOSE 80

RUN pip install -r requirements.txt

ENTRYPOINT ["flask", "run"]

CMD [ "-h 0.0.0.0", "-p 80"]

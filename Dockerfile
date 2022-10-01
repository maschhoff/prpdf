# syntax=docker/dockerfile:1
FROM knex666/prpdf:latest
WORKDIR /source
ENV FLASK_APP=prpdf.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY . /source
CMD ["flask", "run"]

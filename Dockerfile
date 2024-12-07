# syntax=docker/dockerfile:1
#FROM python:3.11.0-slim-buster
FROM python:3.11-slim-bookworm
WORKDIR /source
ENV WORKDIR=/source
ENV FLASK_APP=prpdf.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80
COPY ./ /source
RUN apt-get update && apt-get install tesseract-ocr poppler-utils tesseract-ocr-deu ocrmypdf ghostscript -y
RUN pip3 install -r /source/requirements.txt
CMD ["flask", "run"]

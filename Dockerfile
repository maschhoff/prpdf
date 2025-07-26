# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm

WORKDIR /source
ENV WORKDIR=/source
ENV FLASK_APP=prpdf.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

# Copy source files
COPY ./ /source

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget curl build-essential tesseract-ocr poppler-utils tesseract-ocr-deu ocrmypdf \
    libjpeg-dev libtiff-dev libpng-dev libfreetype6-dev zlib1g-dev

# Install Ghostscript 10.03.1 from official release
RUN wget -q https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10031/ghostscript-10.03.1.tar.gz && \
    tar -xzf ghostscript-10.03.1.tar.gz && \
    cd ghostscript-10.03.1 && ./configure && make -j"$(nproc)" && make install && \
    cd .. && rm -rf ghostscript-10.03.1*

# Ensure new ghostscript is used first
ENV PATH="/usr/local/bin:$PATH"

# Verify version (optional, good for debugging)
RUN gs --version

# Install Python dependencies
RUN pip3 install --no-cache-dir -r /source/requirements.txt

# Start the app
CMD ["flask", "run"]

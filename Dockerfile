# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm

# Set working directory and environment
WORKDIR /source
ENV WORKDIR=/source
ENV FLASK_APP=prpdf.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

# Copy application source code
COPY ./ /source

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl build-essential \
    tesseract-ocr tesseract-ocr-deu \
    poppler-utils ocrmypdf \
    libjpeg-dev libtiff-dev libpng-dev libfreetype6-dev zlib1g-dev \
    libopenjp2-7 \
    jbig2enc qpdf \
    ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Ghostscript 10.03.1 from source
RUN wget -q https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10031/ghostscript-10.03.1.tar.gz && \
    tar -xzf ghostscript-10.03.1.tar.gz && \
    cd ghostscript-10.03.1 && ./configure && make -j"$(nproc)" && make install && \
    cd .. && rm -rf ghostscript-10.03.1*

# Ensure the latest Ghostscript is used
ENV PATH="/usr/local/bin:$PATH"

# Check Ghostscript version (optional but helpful)
RUN gs --version

# Install Python dependencies (including pycryptodome for AES support)
RUN pip3 install --no-cache-dir -r /source/requirements.txt

# Start Flask app
CMD ["flask", "run"]

# ----------- BUILDER-STAGE -------------
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    autoconf automake libtool pkg-config \
    git \
    wget \
    curl \
    ca-certificates \
    libleptonica-dev \
    cmake \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Build jbig2enc
RUN git clone https://github.com/agl/jbig2enc.git && \
    cd jbig2enc && \
    ./autogen.sh && ./configure && \
    make -j"$(nproc)" && \
    cp src/jbig2 /usr/local/bin/jbig2enc

# Build Ghostscript
RUN wget -q https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10031/ghostscript-10.03.1.tar.gz && \
    tar -xzf ghostscript-10.03.1.tar.gz && \
    cd ghostscript-10.03.1 && \
    ./configure && make -j"$(nproc)" && make install

# ----------- FINAL-STAGE ----------------
FROM python:3.11-slim-bookworm

WORKDIR /source

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-deu \
    poppler-utils \
    qpdf \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    zlib1g-dev \
    libopenjp2-7 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy built binaries from builder
COPY --from=builder /usr/local/bin/jbig2enc /usr/local/bin/jbig2enc
COPY --from=builder /usr/local/bin/gs /usr/local/bin/gs
COPY ./ /source

# Set entrypoint or command if needed (optional)
# CMD ["python", "main.py"]

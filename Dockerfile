FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    DOWNLOAD_PATH=/downloads \
    THENKIRI_LOG_PATH=/app/logs/thenkiri.log

WORKDIR /app

# system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends aria2 wget \
    && rm -rf /var/lib/apt/lists/*

# create non-root user
RUN useradd -m appuser

# copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . .

USER root
RUN mkdir -p /downloads && chmod -R 777 /downloads

USER appuser

WORKDIR /app/src

VOLUME ["/downloads"]

CMD ["python", "main.py"]
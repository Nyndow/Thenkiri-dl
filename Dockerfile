FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    DOWNLOAD_PATH=/downloads \
    THENKIRI_LOG_PATH=/app/logs/thenkiri.log

WORKDIR /app

# system dependencies + setup directories
RUN apt-get update \
    && apt-get install -y --no-install-recommends aria2 wget \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /app/logs

# copy requirements first for better caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . .

WORKDIR /app/src

CMD ["python", "main.py"]
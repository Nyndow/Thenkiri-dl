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

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /downloads /app/logs \
    && chown -R appuser:appuser /app /downloads

# switch to non-root user
USER appuser

VOLUME ["/downloads"]

WORKDIR /app/src

CMD ["python", "main.py"]
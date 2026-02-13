# stage 1 (kitchen)

FROM python:3.11-slim AS builder

WORKDIR /app

# 1. Install the compilers needed for hnswlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

#install dependancies into spacif folder
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

#stage 2 (dinning)
FROM python:3.11-slim

WORKDIR /app

#copy only installed libraries from builder stage
COPY --from=builder /install /usr/local

#copy actual application code
COPY . .

EXPOSE 8686

# COMMAND TO RUN API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8686"]


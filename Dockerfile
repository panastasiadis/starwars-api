# Use Python 3.12 slim as base
FROM python:3.12-slim

# Set working directory
WORKDIR /code

# Install build essentials (needed for asyncpg etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install uv (universal virtual environment)
RUN python -m pip install --upgrade pip \
    && pip install uv

# Copy project files
COPY . .
WORKDIR /code/starwars-api-app

# # Install dependencies into uv-managed venv
RUN uv sync

# # Production command: uvicorn with multiple workers
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

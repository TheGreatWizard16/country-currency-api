FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System deps you might need for MySQL
RUN apt-get update && apt-get install -y --no-install-recommends default-mysql-client && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Make sure Python can import "src" package
ENV PYTHONPATH=/app

# Default (Railway overrides)
ENV PORT=8000
EXPOSE 8000

# Use a shell so ${PORT} expands
CMD ["sh","-c","echo \"Starting on port ${PORT}\" && exec uvicorn src.app:app --host 0.0.0.0 --port ${PORT}"]

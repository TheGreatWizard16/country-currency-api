FROM python:3.11-slim

WORKDIR /app

# Install deps first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY src ./src

# Runtime cache dir for image output
RUN mkdir -p cache

EXPOSE 8000
# Use Railway's $PORT if present, else 8000 locally
CMD ["sh", "-c", "uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}"]

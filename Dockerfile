FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src

# Create cache directory
RUN mkdir -p cache

EXPOSE 8000

# ✅ Start app with proper shell so $PORT is expanded
CMD sh -c "uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}"

# Base image with Python 3.11
FROM python:3.11-slim

# Working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and env
COPY src ./src
COPY .env ./.env

# Create cache folder for summary image
RUN mkdir -p cache

EXPOSE 8000

# Start FastAPI with Uvicorn
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]

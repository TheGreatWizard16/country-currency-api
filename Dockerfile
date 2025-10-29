FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app
ENV PORT=8000
EXPOSE 8000

# No shell, no $PORT — Python reads the env and passes an int to uvicorn
CMD ["python", "/app/entrypoint.py"]

FROM python:3.13-slim

# Prevent Python from writing .pyc files & buffer output (Logs instant )
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install MySQL system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Production Engine: Gunicorn with 3 Workers
CMD ["gunicorn", "electronics_shop.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
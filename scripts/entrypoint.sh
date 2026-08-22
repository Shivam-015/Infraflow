#!/bin/bash
set -e

echo "=== InfraFlow Backend Startup ==="

# Wait for MySQL database connection
echo "Waiting for MySQL database..."
while ! nc -z ${DB_HOST:-mysql-service} ${DB_PORT:-3306}; do
  sleep 1
done
echo "MySQL is ready."

# Apply Django Database Migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect Static Files for Nginx serving
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn WSGI Server
echo "Starting Gunicorn application server..."
exec gunicorn infraflow.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 60
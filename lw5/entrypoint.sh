#!/bin/sh
set -e

echo "Waiting for database at db:5432..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is up. Applying migrations..."
alembic upgrade head

echo "Starting application..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8000

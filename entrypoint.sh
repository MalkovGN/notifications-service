#!/usr/bin/env bash
set -e

echo "Waiting for database to be ready..."

until python manage.py migrate --noinput; do
  echo "Database is not ready yet, retrying in 2 seconds..."
  sleep 2
done

echo "Database migrated."

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Loading initial data"
python manage.py loaddata notifications/fixtures/initial_data.json

echo "Starting gunicorn..."
gunicorn project.wsgi:application --bind 0.0.0.0:8000

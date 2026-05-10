#!/usr/bin/env sh
set -e

# Ensure environment variables are available
export PORT=${PORT:-8000}
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-habit_tracker.settings.production}

echo "Running database migrations..."
python manage.py migrate --no-input

echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

echo "Starting Gunicorn on port ${PORT}..."
exec gunicorn habit_tracker.wsgi:application --bind 0.0.0.0:${PORT} --workers 2

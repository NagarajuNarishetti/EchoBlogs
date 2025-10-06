#!/bin/bash

# Docker entrypoint script for EchoBlogs

set -e

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h $DATABASE_HOST -p $DATABASE_PORT -U $DATABASE_USER; do
  sleep 1
done
echo "Database is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate_schemas --shared

# Setup public tenant if it doesn't exist
echo "Setting up public tenant..."
python manage.py setup_public_tenant

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start server
echo "Starting server..."
exec "$@"

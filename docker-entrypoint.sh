#!/bin/bash
set -e

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  sleep 1
done
echo "PostgreSQL is ready."

# Apply all schema files
for file in /app/app/database/schema/*.sql; do
  echo "Running $file"
  psql "postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME" -f "$file"
done

# Start the FastAPI app
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

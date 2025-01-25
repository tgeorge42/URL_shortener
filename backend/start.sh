#!/bin/bash

# Wait until the db is ready
until sqlite3 /app/db/mydatabase.db "SELECT 1;" > /dev/null 2>&1; do
  echo "Waiting for database to be ready..."
  sleep 1
done

# Make the migrations
alembic upgrade head
sleep 5

# Start Uvicorn server
uvicorn app.main:app --host 0.0.0.0 --port 8000

#!/bin/bash
set -e

# Ensure database and reports directories exist with proper permissions
mkdir -p /app/database /app/reports
chmod -R 777 /app/database /app/reports

# Initialize database if it doesn't exist
python -c "from database.db import init_db; init_db()" || true

# Start the application
exec uvicorn webhook_server.main:app --host 0.0.0.0 --port 8000


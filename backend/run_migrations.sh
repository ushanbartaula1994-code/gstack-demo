#!/bin/bash

# Database migration script for AI Fitness Coach

echo "🚀 Running database migrations..."
echo "========================================"

# Change to backend directory
cd "$(dirname "$0")"

# Wait for PostgreSQL to be ready
echo "🔄 Waiting for PostgreSQL to be ready..."
MAX_RETRIES=60
RETRY_INTERVAL=5

for i in $(seq 1 $MAX_RETRIES); do
    if pg_isready -h localhost -U aifitness -d aifitnesscoach 2>/dev/null; then
        echo "✅ PostgreSQL is ready!"
        break
    fi

    if [ $i -eq $MAX_RETRIES ]; then
        echo "❌ Timeout: PostgreSQL did not become ready after $MAX_RETRIES attempts"
        exit 1
    fi

    echo "⏳ Attempt $i/$MAX_RETRIES - PostgreSQL not yet ready, retrying in $RETRY_INTERVAL seconds..."
    sleep $RETRY_INTERVAL
done

echo ""
echo "📈 Running Alembic migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Database migrations completed successfully!"
else
    echo "❌ Database migrations failed!"
    exit 1
fi

echo ""
echo "🌱 Seeding database..."
python -m app.db.seed

if [ $? -eq 0 ]; then
    echo "✅ Database seeding completed successfully!"
else
    echo "❌ Database seeding failed!"
    exit 1
fi

echo ""
echo "🎉 Database setup completed successfully!"
echo ""
echo "You can now run the FastAPI server:"
echo "  uvicorn app.main:app --reload --port 8000"
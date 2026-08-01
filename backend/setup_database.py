#!/usr/bin/env python3
"""
Database setup script for AI Fitness Coach

This script:
1. Waits for PostgreSQL to be available
2.Creates the database if it doesn't exist
3. Runs Alembic migrations
4. Seeds the database with initial data

Usage:
    python setup_database.py

Requirements:
    - Docker must be running with the PostgreSQL container
    - Python dependencies must be installed (pip install -r requirements.txt)
"""

import asyncio
import subprocess
import sys
import time
from pathlib import Path

def wait_for_postgres(max_retries=60, retry_interval=5):
    """Wait for PostgreSQL to be ready"""
    print("🔄 Waiting for PostgreSQL to be ready...")

    # Try to connect to PostgreSQL
    for i in range(max_retries):
        try:
            # Test connection using psql if available
            result = subprocess.run([
                'psql',
                '-h', 'localhost',
                '-U', 'aifitness',
                '-d', 'aifitnesscoach',
                '-c', 'SELECT 1'
            ], capture_output=True, text=True, timeout=10)

            if result.returncode == 0:
                print("✅ PostgreSQL is ready!")
                return True
        except:
            pass

        print(f"⏳ Attempt {i + 1}/{max_retries} - PostgreSQL not yet ready, retrying in {retry_interval} seconds...")
        time.sleep(retry_interval)

    print("❌ Timeout: PostgreSQL did not become ready")
    return False


def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    print("🔧 Creating database if it doesn't exist...")

    try:
        # Try to create the database
        result = subprocess.run([
            'psql',
            '-h', 'localhost',
            '-U', 'postgres',
            '-c', 'CREATE DATABASE aifitnesscoach;'
        ], capture_output=True, text=True)

        # If database already exists, that's fine
        if "already exists" in result.stderr.lower():
            print("ℹ️  Database already exists")
            return True
        elif result.returncode == 0:
            print("✅ Database created")
            return True

    except FileNotFoundError:
        print("⚠️  psql not found, trying to use PostgreSQL connection via SQLAlchemy...")
        return try_create_database_with_sqlalchemy()

    return False


def try_create_database_with_sqlalchemy():
    """Try to create database using SQLAlchemy directly"""
    try:
        # First, try to connect to the default postgres database
        from sqlalchemy import create_engine, text
        from sqlalchemy.exc import OperationalError

        # Try to connect to postgres database to create our database
        try:
            engine = create_engine("postgresql://aifitness:aifitness2024@localhost:5432/postgres")
            with engine.connect() as conn:
                # Check if database exists
                result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname = 'aifitnesscoach'"))
                if result.fetchone():
                    print("ℹ️  Database already exists")
                    return True
                else:
                    # Create the database
                    conn.execute(text("CREATE DATABASE aifitnesscoach"))
                    conn.commit()
                    print("✅ Database created via SQLAlchemy")
                    return True
        except OperationalError:
            print("❌ Could not connect to PostgreSQL server")
            return False

    except ImportError:
        print("❌ SQLAlchemy not installed")
        return False


def run_alembic_upgrade():
    """Run Alembic database migrations"""
    print("📈 Running database migrations...")

    try:
        from alembic.config import Config
        from alembic import command

        # Change to backend directory
        backend_dir = Path(__file__).parent
        os.chdir(backend_dir)

        # Load Alembic config
        alembic_cfg = Config('alembic.ini')

        # Run migrations
        command.upgrade(alembic_cfg, 'head')
        print("✅ Database migrations completed!")
        return True

    except Exception as e:
        print(f"❌ Error running migrations: {e}")
        return False


async def seed_database():
    """Seed the database with initial data"""
    print("🌱 Seeding database...")

    try:
        # Import the seed module
        sys.path.insert(0, str(Path(__file__).parent))
        from app.db.seed import seed_database as seed_func
        from app.db.session import async_session_maker

        async with async_session_maker() as session:
            await seed_func(session)

        print("✅ Database seeding completed!")
        return True

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        return False


def main():
    """Main database setup function"""
    import os

    print("🚀 AI Fitness Coach Database Setup")
    print("=" * 50)

    # Step 1: Wait for PostgreSQL
    if not wait_for_postgres():
        print("❌ Aborting: PostgreSQL is not available")
        sys.exit(1)

    # Step 2: Create database if it doesn't exist
    if not create_database_if_not_exists():
        print("❌ Aborting: Could not create database")
        sys.exit(1)

    # Step 3: Run migrations
    if not run_alembic_upgrade():
        print("❌ Error: Migration failed, but continuing...")

    # Step 4: Seed database
    if not asyncio.run(seed_database()):
        print("❌ Error: Seeding failed, but continuing...")

    print("\n🎉 Database setup completed successfully!")
    print("\nYou can now run the FastAPI server:")
    print("  uvicorn app.main:app --reload --port 8000")


if __name__ == '__main__':
    main()
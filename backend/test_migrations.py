#!/usr/bin/env python3
"""
Test script to verify migrations work without database connection
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all models and dependencies can be imported"""
    print("🧪 Testing imports...")

    try:
        # Test SQLAlchemy
        import sqlalchemy
        print(f"✅ SQLAlchemy: {sqlalchemy.__version__}")

        # Test Alembic
        import alembic
        print("✅ Alembic: installed")

        # Test models
        from app.models.base import Base
        from app.models.user import User, UserProfile
        from app.models.exercise import Exercise
        from app.models.workout import Workout, WorkoutExercise, WorkoutSession
        from app.models.form_analysis import FormAnalysisEvent
        from app.models.progress import ProgressMetrics
        from app.models.subscription import Subscription
        print("✅ All models imported successfully")

        # Test config
        from app.config.settings import settings
        print(f"✅ Settings loaded: DATABASE_URL = {settings.DATABASE_URL}")

        # Test database session
        from app.db.session import async_session_maker, engine
        print("✅ Database session configured")

        # List all tables
        tables = [table.name for table in Base.metadata.tables.values()]
        print(f"✅ Database tables defined: {', '.join(sorted(tables))}")

        return True

    except Exception as e:
        print(f"❌ Import test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_alembic_config():
    """Test that Alembic configuration works"""
    print("\n🧪 Testing Alembic configuration...")

    try:
        from alembic.config import Config
        from alembic import command

        config = Config('alembic.ini')
        print(f"✅ Alembic config loaded")
        print(f"   SQLAlchemy URL: {config.get_main_option('sqlalchemy.url')}")

        # Test listing migrations
        from alembic.script import ScriptDirectory
        script = ScriptDirectory.from_config(config)
        heads = script.get_heads()
        print(f"✅ Found {len(heads)} migration head(s)")
        for head in heads:
            print(f"   - {head}")

        return True

    except Exception as e:
        print(f"❌ Alembic config test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_migration_sql():
    """Test that migration SQL can be generated"""
    print("\n🧪 Testing migration SQL generation...")

    try:
        import subprocess
        result = subprocess.run([
            'alembic', 'upgrade', 'head', '--sql'
        ], capture_output=True, text=True, cwd='.')

        if result.returncode == 0:
            # Count the number of CREATE TABLE statements
            create_tables = result.stdout.count('CREATE TABLE')
            print(f"✅ Migration SQL generated successfully")
            print(f"   Found {create_tables} CREATE TABLE statements")

            # Check for our main tables
            tables = ['users', 'exercises', 'workouts', 'user_profiles']
            for table in tables:
                if f'CREATE TABLE {table}' in result.stdout:
                    print(f"   ✅ Table '{table}' found in migration")
                else:
                    print(f"   ❌ Table '{table}' missing from migration")
                    return False

            return True
        else:
            print(f"❌ Migration SQL generation failed: {result.stderr}")
            return False

    except Exception as e:
        print(f"❌ Migration SQL test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_seed_imports():
    """Test that seed module can be imported"""
    print("\n🧪 Testing seed module...")

    try:
        from app.db.seed import (
            seed_database,
            seed_exercises,
            CORE_EXERCISES_DATA,
            SUPPORTING_EXERCISES_DATA
        )
        print(f"✅ Seed module imported successfully")
        print(f"   Core exercises: {len(CORE_EXERCISES_DATA)}")
        print(f"   Supporting exercises: {len(SUPPORTING_EXERCISES_DATA)}")
        print(f"   Total exercises: {len(CORE_EXERCISES_DATA) + len(SUPPORTING_EXERCISES_DATA)}")

        return True

    except Exception as e:
        print(f"❌ Seed module test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 AI Fitness Coach Backend - Migration Test Suite")
    print("=" * 60)

    all_passed = True

    # Run all tests
    all_passed &= test_imports()
    all_passed &= test_alembic_config()
    all_passed &= test_migration_sql()
    all_passed &= test_seed_imports()

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Migrations are ready to run.")
        print("\nNext steps:")
        print("1. Start PostgreSQL: docker-compose up -d postgres")
        print("2. Run migrations: python test_migrations.py (when DB is ready)")
        print("   OR: alembic upgrade head")
        print("3. Seed database: python -m app.db.seed")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
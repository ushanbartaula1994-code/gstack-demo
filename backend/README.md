# AI Fitness Coach - Backend

FastAPI backend for the AI Fitness Coach application.

## Prerequisites

- Python 3.11+
- PostgreSQL 15+
- pip

## Getting Started

### 1. Setup Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

For development (optional):
```bash
pip install -r requirements.txt[dev]
```

### 3. Configure Environment

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your database credentials and other settings.

### 4. Database Setup

#### Option A: Local PostgreSQL

Start PostgreSQL locally and create the database:
```bash
# Using Docker (recommended)
docker-compose up -d postgres

# Or install PostgreSQL natively
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql -c "CREATE DATABASE aifitnesscoach;"
sudo -u postgres psql -c "CREATE USER aifitness WITH PASSWORD 'aifitness2024';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE aifitnesscoach TO aifitness;"
```

#### Option B: Cloud PostgreSQL (Neon)

1. Sign up at https://neon.tech
2. Create a project
3. Get your connection URL and update `.env`:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require
```

### 5. Run Migrations

Initialize Alembic (if needed):
```bash
alembic init alembic
```

Create and apply migrations:
```bash
# Auto-generate migrations from models
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 6. Seed Database

```bash
python -m app.db.seed
```

### 7. Run Development Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at: http://localhost:8000

API Documentation (Swagger UI): http://localhost:8000/docs

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config/              # Configuration files
│   │   ├── __init__.py
│   │   └── settings.py      # Pydantic settings
│   ├── db/                  # Database configuration
│   │   ├── __init__.py
│   │   ├── session.py       # Database session management
│   │   └── seed.py          # Database seed data
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── base.py          # Base model
│   │   ├── user.py          # User and UserProfile models
│   │   ├── exercise.py      # Exercise model
│   │   ├── workout.py       # Workout, WorkoutExercise, WorkoutSession
│   │   ├── form_analysis.py # FormAnalysisEvent model
│   │   ├── progress.py      # ProgressMetrics model
│   │   └── subscription.py # Subscription model
│   ├── routes/              # API route handlers
│   │   ├── __init__.py
│   │   ├── health.py        # Health check endpoint
│   │   ├── users.py         # User endpoints
│   │   ├── exercises.py     # Exercise endpoints
│   │   ├── workouts.py      # Workout endpoints
│   │   └── progress.py      # Progress endpoints
│   └── schemas/             # Pydantic models
│       └── __init__.py
├── alembic/                 # Alembic migrations
│   ├── env.py
│   └── versions/
├── migrations/              # Additional migrations (optional)
├── tests/                   # Test files
├── .env.example             # Environment variables template
├── alembic.ini              # Alembic configuration
├── pyproject.toml           # Project configuration
├── README.md
└── requirements.txt
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection URL | postgresql://aifitness:aifitness2024@localhost:5432/aifitnesscoach |
| JWT_SECRET | JWT secret key for authentication | - |
| JWT_EXPIRY_MINUTES | JWT token expiry in minutes | 60 |
| JWT_REFRESH_EXPIRY_DAYS | JWT refresh token expiry in days | 7 |
| CORS_ORIGINS | Comma-separated CORS origins | http://localhost:3000,http://localhost:8000 |
| STRIPE_SECRET_KEY | Stripe secret key | - |
| STRIPE_PUBLISHABLE_KEY | Stripe publishable key | - |
| STRIPE_WEBHOOK_SECRET | Stripe webhook secret | - |
| CLAUDE_API_KEY | Claude API key for LLM | - |

## Available Scripts

- `uvicorn app.main:app --reload` - Start development server
- `alembic revision --autogenerate -m "message"` - Create new migration
- `alembic upgrade head` - Apply all migrations
- `alembic downgrade -1` - Rollback last migration
- `python -m app.db.seed` - Seed database with initial data

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | API info |
| GET | /docs | Swagger UI documentation |
| GET | /api/v1/health | Health check |
| GET | /api/v1/users/me | Get current user profile |
| PUT | /api/v1/users/me | Update user profile |
| GET | /api/v1/exercises | List all exercises |
| GET | /api/v1/exercises/:id | Get exercise details |
| POST | /api/v1/workouts/generate | Generate workout |
| GET | /api/v1/workouts | List user workouts |
| GET | /api/v1/workouts/:id | Get workout details |
| GET | /api/v1/progress | Get user progress |

## Database Models

The application uses the following database tables:

- **users** - User authentication and account information
- **user_profiles** - User fitness preferences and goals
- **exercises** - Exercise library (5 core + supporting exercises)
- **workouts** - Generated workout programs
- **workout_exercises** - Exercises within workouts
- **workout_sessions** - Individual workout sessions
- **form_analysis_events** - Real-time form analysis data
- **progress_metrics** - User progress tracking
- **subscriptions** - Subscription and payment information

## Testing

Run tests with pytest:
```bash
pytest tests/ -v
```

## Deployment

### With Docker

Create a Dockerfile and deploy to your preferred platform.

### Without Docker

Ensure all environment variables are set and run:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## License

Private - All rights reserved.

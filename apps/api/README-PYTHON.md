# Python Environment Setup for Agent Router API

This project uses `pyproject.toml` for dependency management, which is the modern Python standard.

## Quick Setup (Recommended)

### Option 1: Using the setup script (Windows)
```bash
cd apps/api
setup-venv-pyproject.bat
```

### Option 2: Manual setup
```bash
cd apps/api

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate.bat
# macOS/Linux:
source venv/bin/activate

# Install project in editable mode
pip install -e .

# Install development dependencies (optional)
pip install -e ".[dev]"
```

## Key Commands

### Install Dependencies
```bash
# Production dependencies only
pip install -e .

# Production + development dependencies
pip install -e ".[dev]"
```

### Run the API Server
```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the script defined in pyproject.toml
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Development Tools
```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Lint code
ruff check .

# Format code
ruff format .

# Type checking
mypy app

# Security audit
bandit -r app/
pip-audit
```

## Why `pyproject.toml`?

- **Modern Standard**: PEP 518/621 compliant
- **Better Dependency Resolution**: More reliable than requirements.txt
- **Development Dependencies**: Separate production and dev dependencies
- **Project Metadata**: Centralized project information
- **Build System**: Integrated with modern Python packaging tools

## Virtual Environment Benefits

- **Isolation**: Dependencies don't conflict with system Python
- **Reproducibility**: Same environment across different machines
- **Clean Uninstall**: Easy to remove all dependencies
- **Version Control**: Lock specific dependency versions

## Environment Variables

Create a `.env` file in `apps/api/`:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Database Setup

```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"
```

## Redis Setup

For local development, you can use Docker:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

Or install Redis locally on your system.

@echo off
echo Setting up Python virtual environment for Agent Router API using pyproject.toml...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.12+ from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install the project in editable mode with all dependencies
echo Installing project dependencies from pyproject.toml...
pip install -e .

echo.
echo Virtual environment setup complete!
echo.
echo To activate the environment in the future, run:
echo   venv\Scripts\activate.bat
echo.
echo To install development dependencies, run:
echo   pip install -e ".[dev]"
echo.
echo To run the API server, run:
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
pause

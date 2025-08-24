@echo off
echo Stopping any running FastAPI server...
taskkill /f /im python.exe 2>nul
taskkill /f /im uvicorn.exe 2>nul

echo Starting FastAPI server with CORS fixes...
cd /d "%~dp0"
call venv\Scripts\activate.bat
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

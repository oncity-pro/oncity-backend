@echo off
REM ONCITY-Django Backend Startup Script for Windows

echo ========================================
echo   ONCITY-Django Backend Setup
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and configure it.
    echo.
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env file with your MySQL credentials before continuing!
    pause
)

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

REM Start development server
echo ========================================
echo   Starting Django Development Server
echo   URL: http://127.0.0.1:8000
echo   Admin: http://127.0.0.1:8000/admin/
echo   API: http://127.0.0.1:8000/api/health/
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

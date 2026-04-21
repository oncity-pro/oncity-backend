#!/bin/bash
# ONCITY-Django Backend Startup Script for Linux/Mac

echo "========================================"
echo "  ONCITY-Django Backend Setup"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    echo ""
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Edit .env file with your MySQL credentials before continuing!"
    read -p "Press enter to continue after editing .env..."
fi

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo ""

# Start development server
echo "========================================"
echo "  Starting Django Development Server"
echo "  URL: http://127.0.0.1:8000"
echo "  Admin: http://127.0.0.1:8000/admin/"
echo "  API: http://127.0.0.1:8000/api/health/"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver

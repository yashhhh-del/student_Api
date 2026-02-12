#!/bin/bash

echo "🎓 Student Management System - Launcher"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r streamlit_requirements.txt

# Check if Django API is running
echo ""
echo "⚠️  Make sure your Django API is running on http://localhost:8000"
echo ""
echo "If not, open a new terminal and run:"
echo "  cd student_project"
echo "  python manage.py runserver"
echo ""

# Wait for user confirmation
read -p "Press Enter when Django API is ready..."

# Run Streamlit app
echo ""
echo "🚀 Starting Streamlit app..."
echo "App will open at: http://localhost:8501"
echo ""

streamlit run streamlit_app.py

# Deactivate virtual environment on exit
deactivate

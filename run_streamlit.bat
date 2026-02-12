@echo off
echo ========================================
echo Student Management System - Launcher
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r streamlit_requirements.txt

REM Reminder to start Django
echo.
echo WARNING: Make sure your Django API is running on http://localhost:8000
echo.
echo If not, open a new terminal and run:
echo   cd student_project
echo   python manage.py runserver
echo.
pause

REM Run Streamlit app
echo.
echo Starting Streamlit app...
echo App will open at: http://localhost:8501
echo.

streamlit run streamlit_app.py

REM Deactivate virtual environment
deactivate

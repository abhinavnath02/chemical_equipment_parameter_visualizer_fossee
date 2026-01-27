@echo off
REM Quick start script for Chemical Equipment Parameter Visualizer Desktop App
echo.
echo ========================================
echo Chemical Equipment Parameter Visualizer
echo Desktop Application Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo Please ensure Python 3.8+ is installed
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
    echo.
) else (
    echo [1/4] Virtual environment already exists
    echo.
)

REM Activate virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [3/4] Checking and installing dependencies...
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully
echo.

REM Test imports
echo [4/4] Testing dependencies...
python test_dependencies.py
if errorlevel 1 (
    echo.
    echo ERROR: Dependency check failed
    echo Please review the errors above
    pause
    exit /b 1
)
echo.

REM Start the application
echo ========================================
echo Starting the application...
echo ========================================
echo.
echo IMPORTANT: Make sure the backend server is running at:
echo   http://127.0.0.1:8000
echo.
echo If the backend is not running, start it with:
echo   cd backend
echo   python manage.py runserver
echo.
timeout /t 3 /nobreak >nul
python main.py

REM Deactivate on exit
deactivate

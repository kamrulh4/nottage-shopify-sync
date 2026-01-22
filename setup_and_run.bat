@echo off
REM Nottage-Shopify Sync - Setup and Run Script for Windows

REM Navigate to script directory
cd /d "%~dp0"

echo =========================================
echo Nottage-Shopify Sync - Setup and Run
echo =========================================

REM Check if venv exists, create if not
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        exit /b 1
    )
    echo Virtual environment created successfully
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo Installing/updating requirements...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install requirements
    exit /b 1
)

REM Run main.py
echo =========================================
echo Starting sync process...
echo =========================================
python main.py

echo =========================================
echo Sync completed
echo =========================================

pause

@echo off
REM Windows Batch Script for Nottage-Shopify Sync

REM Navigate to project directory (UPDATE THIS PATH)
cd /d "C:\Path\To\Your\Project\technase"

REM Activate Virtual Environment and Run Script
REM Assumes 'venv' is in the project folder
call venv\Scripts\activate.bat

REM Run main.py and append output to log file
python main.py >> sync.log 2>&1

echo Sync Finished at %date% %time% >> sync.log
echo ---------------------------------------- >> sync.log

#!/bin/bash

# Navigate to project directory
cd /Users/kamrul/Desktop/Projects/technase

# Configure logging
LOG_FILE="/Users/kamrul/Desktop/Projects/technase/sync.log"
echo "Starting Sync at $(date)" >> "$LOG_FILE"

# Run the python script using the virtual environment python
# Capturing both stdout and stderr to the log file
/Users/kamrul/Desktop/Projects/technase/venv/bin/python main.py >> "$LOG_FILE" 2>&1

echo "Sync Finished at $(date)" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE"

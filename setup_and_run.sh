#!/bin/bash

# Navigate to script directory
cd "$(dirname "$0")"

echo "========================================="
echo "Nottage-Shopify Sync - Setup and Run"
echo "========================================="

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "Installing/updating requirements..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install requirements"
    exit 1
fi

# Run main.py
echo "========================================="
echo "Starting sync process..."
echo "========================================="
python main.py

echo "========================================="
echo "Sync completed"
echo "========================================="

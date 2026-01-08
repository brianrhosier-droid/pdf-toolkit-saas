#!/bin/bash

echo "===================================="
echo "PDF Toolkit SaaS - Starting Server"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f .env ]; then
    echo "WARNING: .env file not found"
    echo "Creating from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit .env and add your Stripe API keys"
    echo "Then run this script again."
    echo ""
    exit 1
fi

echo ""
echo "Starting PDF Toolkit SaaS..."
echo ""
echo "===================================="
echo "Access the application at:"
echo "http://localhost:5000"
echo "===================================="
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the Flask application
python app.py

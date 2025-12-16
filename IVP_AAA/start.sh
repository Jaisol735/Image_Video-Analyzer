#!/bin/bash

echo "Starting IVP AI Photographer Analyzer..."
echo

echo "Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "Error installing Node.js dependencies"
    exit 1
fi

echo
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error installing Python dependencies"
    exit 1
fi

echo
echo "Starting the application..."
echo "Please set your GEMINI_API_KEY environment variable before running"
echo "You can get your API key from: https://makersuite.google.com/app/apikey"
echo
echo "Starting server on http://localhost:3000"
echo

npm start

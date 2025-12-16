@echo off
echo Starting IVP AI Photographer Analyzer...
echo.

echo Installing Node.js dependencies...
call npm install
if %errorlevel% neq 0 (
    echo Error installing Node.js dependencies
    pause
    exit /b 1
)

echo.
echo Installing Python dependencies...
call pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Python dependencies
    pause
    exit /b 1
)

echo.
echo Starting the application...
echo Please set your GEMINI_API_KEY environment variable before running
echo You can get your API key from: https://makersuite.google.com/app/apikey
echo.
echo Starting server on http://localhost:3000
echo.

call npm start

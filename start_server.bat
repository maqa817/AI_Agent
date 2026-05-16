@echo off
title FreshGuard AI Server

echo ===================================================
echo             FRESHGUARD AI - LOCAL SERVER           
echo ===================================================
echo.
echo Make sure your Ollama app is running in the background!
echo.
echo Starting the FastAPI Backend...
echo.

:: Open the browser automatically after a short delay
timeout /t 2 >nul
start http://127.0.0.1:8000

:: Start the Python server
python main.py

pause

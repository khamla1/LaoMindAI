@echo off
cd /d "%~dp0"
title Installing Dependencies...
echo ========================================================
echo      Installing Project Dependencies
echo ========================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not found in PATH.
    echo Please install Python 3.12 or newer.
    pause
    exit /b
)

if exist "..\.venv" (
    echo [INFO] Virtual environment already exists.
) else (
    echo [INFO] Creating virtual environment (.venv)...
    python -m venv ..\.venv
)

call ..\.venv\Scripts\activate
echo [INFO] Upgrade pip...
python -m pip install --upgrade pip
echo [INFO] Installing requirements...
pip install -r requirements.txt

echo.
echo ========================================================
echo      Installation Complete!
echo ========================================================
echo.
pause

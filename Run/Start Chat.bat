@echo off
cd /d "%~dp0"
if not exist "..\.venv" (
    echo [ERROR] Virtual environment not found. Please run Install\install.bat first.
    pause
    exit /b
)

REM Activate venv
call ..\.venv\Scripts\activate

REM Change dir to System
cd ..\System

REM Run Chat
start pythonw run_chat.py
exit

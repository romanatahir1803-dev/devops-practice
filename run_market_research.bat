@echo off
setlocal enabledelayedexpansion

title Amazon Mattress AI Market Research Tool (DE & NL)
echo ======================================================================
echo    Amazon Mattress AI Market Research Tool (DE & NL)
echo ======================================================================
echo.

REM Detect Python executable
set "PYTHON_EXE="

if exist "C:\Users\Waqas Ahmed\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PYTHON_EXE=C:\Users\Waqas Ahmed\AppData\Local\Programs\Python\Python312\python.exe"
    goto :PYTHON_FOUND
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_EXE=py -3.12"
    goto :PYTHON_FOUND
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PYTHON_EXE=python"
    goto :PYTHON_FOUND
)

echo [ERROR] Python was not detected on this system.
echo Please install Python 3.8+ from https://www.python.org/downloads/
pause
exit /b 1

:PYTHON_FOUND
echo [INFO] Using Python: %PYTHON_EXE%
echo.

REM Install / verify dependencies
echo [1/3] Checking and installing dependencies...
"%PYTHON_EXE%" -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARNING] Encountered minor dependency check notice. Continuing...
)

echo.
echo [2/3] Launching Web Dashboard...
start "" "http://localhost:8000"

echo.
echo [3/3] Starting Server at http://localhost:8000
echo Press Ctrl+C in this window to stop the server anytime.
echo ======================================================================
echo.

"%PYTHON_EXE%" app.py

pause

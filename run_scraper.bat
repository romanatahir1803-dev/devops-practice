@echo off
echo ===================================================
echo     bett1.de Mattress Web Scraper for Windows
echo ===================================================
echo.

:: Check if Python is installed
set PYTHON_CMD=

:: Check direct local AppData paths first
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
)

:: Check py -3.12 launcher
if "%PYTHON_CMD%"=="" (
    py -3.12 --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 set PYTHON_CMD=py -3.12
)

:: Check general python command
if "%PYTHON_CMD%"=="" (
    python --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 set PYTHON_CMD=python
)

:: Check general py launcher
if "%PYTHON_CMD%"=="" (
    py --version >nul 2>&1
    if %ERRORLEVEL% EQU 0 set PYTHON_CMD=py
)

if "%PYTHON_CMD%"=="" (
    echo [ERROR] Python is not found on this system!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check the box "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking and installing required dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo [2/3] Running web scraper to extract all mattress variants...
echo.
%PYTHON_CMD% scraper.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Web scraper encountered an issue.
    pause
    exit /b 1
)

echo.
echo [3/3] Done! Data has been exported to bett1_mattresses_data.xlsx
echo.
pause

@echo off
title ADRDE Address Management System — Launcher
color 1F
echo.
echo ==========================================
echo   ADRDE, DRDO — Address Management System
echo   एडीआरडीई, डीआरडीओ — पता प्रबंधन प्रणाली
echo ==========================================
echo.

REM Try different Python executables
set PYTHON_CMD=

REM Check python3.12, python3.11, python3.10, python3 in common locations
for %%P in (
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
    "C:\Python39\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
) do (
    if exist %%P (
        set PYTHON_CMD=%%P
        goto :found
    )
)

REM Try PATH
where python.exe >nul 2>&1
if %ERRORLEVEL%==0 (
    for /f "tokens=*" %%i in ('where python.exe') do (
        set PYTHON_CMD=%%i
        goto :found
    )
)

echo [ERROR] Python not found on this system!
echo.
echo Please install Python 3.10 or later from:
echo   https://www.python.org/downloads/
echo.
echo Make sure to check "Add Python to PATH" during installation.
echo.
pause
exit /b 1

:found
echo [OK] Found Python: %PYTHON_CMD%
echo.

REM Check if dependencies are installed
"%PYTHON_CMD%" -c "import PySide6" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Installing required packages...
    echo        This may take a few minutes on first run.
    echo.
    "%PYTHON_CMD%" -m pip install --upgrade pip >nul 2>&1
    "%PYTHON_CMD%" -m pip install PySide6 bcrypt reportlab pandas openpyxl Pillow
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to install packages. Check your internet connection.
        pause
        exit /b 1
    )
    echo [OK] Packages installed successfully.
    echo.
)

REM Generate placeholder logos if not present
if not exist "assets\adrde_logo.png" (
    echo [INFO] Creating placeholder logos...
    "%PYTHON_CMD%" create_logos.py
)

REM Create data directory
if not exist "data" mkdir data

echo [INFO] Starting ADRDE Address Management System...
echo.
echo Default Admin Login:
echo   Username: admin
echo   Password: Admin@1234
echo.
echo ==========================================
echo.

"%PYTHON_CMD%" main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application exited with an error.
    pause
)

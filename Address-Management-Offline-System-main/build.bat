@echo off
echo ============================================
echo  ADRDE Address Management System - Build
echo ============================================
echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Building executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "ADRDE_Address_Management" ^
    --icon "assets\adrde_logo.png" ^
    --add-data "assets;assets" ^
    --add-data "utils;utils" ^
    --add-data "modules;modules" ^
    --add-data "database;database" ^
    --add-data "ui;ui" ^
    --hidden-import "bcrypt" ^
    --hidden-import "reportlab" ^
    --hidden-import "PySide6.QtCore" ^
    --hidden-import "PySide6.QtWidgets" ^
    --hidden-import "PySide6.QtGui" ^
    --hidden-import "PySide6.QtPrintSupport" ^
    main.py

echo.
echo Build complete! Executable is in the 'dist' folder.
echo.
pause

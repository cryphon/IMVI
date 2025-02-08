@echo off
setlocal EnableDelayedExpansion

REM First run the Python build script
echo Building executable with build_exe.py...
python build_exe.py
if errorlevel 1 (
    echo Python build failed!
    pause
    exit /b 1
)

REM Check if executable exists
if not exist "dist\IMVI.exe" (
    echo Executable not found! Build may have failed.
    pause
    exit /b 1
)

REM Check for Inno Setup
if not exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    echo Inno Setup not found! Please install Inno Setup 6
    echo Download from: https://jrsoftware.org/isdl.php
    pause
    exit /b 1
)

REM Create installer
echo Creating installer...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" IMVI.iss
if errorlevel 1 (
    echo Installer creation failed!
    pause
    exit /b 1
)

echo Installer created successfully! Check the installer folder.
pause
#!/bin/bash

# Echo commands as they run
set -x

# Function to check if last command succeeded
check_status() {
    if [ $? -ne 0 ]; then
        echo "Error: $1 failed!"
        exit 1
    fi
}

# Check and install PyInstaller if not present
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip3 install pyinstaller
    check_status "PyInstaller installation"
fi

echo "Building executable with PyInstaller..."
python3 build_exe.py
check_status "PyInstaller build"

# Check if executable exists
if [ ! -f "dist/IMVI" ]; then
    echo "Error: Executable not found! Build may have failed."
    exit 1
fi

echo "Building installer with Inno Setup..."
# Using wine to run Inno Setup from WSL
ISCC_PATH="/mnt/c/Program Files (x86)/Inno Setup 6/ISCC.exe"

if [ ! -f "$ISCC_PATH" ]; then
    echo "Error: Inno Setup not found at $ISCC_PATH"
    exit 1
fi

# Convert WSL path to Windows path for Inno Setup
INSTALLER_PATH=$(wslpath -w "installer/IMVI.iss")

# Run Inno Setup through Windows
cmd.exe /c "\"$ISCC_PATH\" \"$INSTALLER_PATH\""
check_status "Inno Setup build"

echo "Installer created successfully! Check the 'installer' folder."
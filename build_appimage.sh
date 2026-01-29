#!/bin/bash
# This script was generated using Antigravity
set -e

# Define directories
APPIMAGE_DIR="AppImage"
BIN_DIR="$APPIMAGE_DIR/usr/bin"
SOURCE_BUILD_DIR="build/linux"
APPIMAGETOOL_URL="https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage"

# Clean up previous build artifacts in the AppImage directory
echo "Cleaning up $BIN_DIR..."
rm -rf "$BIN_DIR"
mkdir -p "$BIN_DIR"

# Build the Flet application for Linux
echo "Building Flet application..."
uv run flet build linux

# Verify if the build was successful and the bundle directory exists
if [ ! -d "$SOURCE_BUILD_DIR" ]; then
    echo "Error: Build directory $SOURCE_BUILD_DIR does not exist. Build might have failed."
    exit 1
fi

# Check if appimagetool exists, download if not
if ! command -v appimagetool &> /dev/null; then
    if [ ! -f "appimagetool" ]; then
        echo "appimagetool not found in PATH. Downloading..."
        wget -O appimagetool "$APPIMAGETOOL_URL"
        chmod +x appimagetool
    fi
    APPIMAGETOOL="./appimagetool"
else
    APPIMAGETOOL="appimagetool"
fi

# Move the build files to the AppImage/usr/bin/ directory
echo "Moving build files to $BIN_DIR..."
cp -r "$SOURCE_BUILD_DIR"/* "$BIN_DIR/"

# Create the AppImage
echo "Creating AppImage..."
ARCH=x86_64 $APPIMAGETOOL "$APPIMAGE_DIR"
mv DaVinci_Re-Solver-x86_64.AppImage "$APPIMAGE_DIR/Davinci_Re-Solver.AppImage"

echo "AppImage creation complete!"

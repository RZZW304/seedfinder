#!/bin/bash
# Build script for SeedFinder

echo "Building SeedFinder..."

# Clean previous builds
rm -rf build dist

# Build executable
pyinstaller seedfinder.spec

# Check if build was successful
if [ -f "dist/SeedFinder" ] || [ -f "dist/SeedFinder.exe" ]; then
    echo "Build successful! Executable located in dist/"
else
    echo "Build failed!"
    exit 1
fi

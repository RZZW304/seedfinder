@echo off
REM Build script for SeedFinder on Windows

echo Building SeedFinder...

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM Build executable
pyinstaller seedfinder.spec

REM Check if build was successful
if exist "dist\SeedFinder.exe" (
    echo Build successful! Executable located in dist\
) else (
    echo Build failed!
    exit /b 1
)

pause

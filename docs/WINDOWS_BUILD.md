# Windows Executable Build Instructions

## Method 1: GitHub Actions (Recommended)

The repository includes a GitHub Actions workflow that automatically builds the Windows .exe file.

### Steps:

1. **Push a new version tag**:
```bash
git tag v0.2.0
git push origin v0.2.0
```

2. **GitHub Actions will automatically**:
   - Install dependencies on Windows runner
   - Build the executable using PyInstaller
   - Upload to GitHub Releases
   - Create/update release with .exe file

3. **Download the .exe**:
   - Go to: https://github.com/RZZW304/seedfinder/releases
   - Download the .exe file attached to the release

### Advantages:
- No need for Windows machine
- Automated build process
- Consistent builds
- No manual steps required

## Method 2: Manual Windows Build

If you have a Windows machine:

1. **Install Python 3.12+**
   - Download from: https://www.python.org/downloads/

2. **Clone repository**:
```bash
git clone https://github.com/RZZW304/seedfinder.git
cd seedfinder
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Build executable**:
```bash
pyinstaller seedfinder.spec
```

5. **Find the .exe**:
   - Location: `dist/SeedFinder.exe`
   - This file can be distributed

## Method 3: Docker Build (Cross-platform)

For building on Linux with Docker:

1. **Create Dockerfile** (already included):
```dockerfile
FROM python:3.12-windowsservercore
# Build instructions included
```

2. **Build using Docker**:
```bash
docker build -t seedfinder-builder .
docker run -v $(pwd)/dist:/app/dist seedfinder-builder
```

## Troubleshooting

### Build fails on GitHub Actions
- Check Actions tab for detailed logs
- Ensure all dependencies are in requirements.txt
- Verify PyInstaller configuration in seedfinder.spec

### Antivirus flags the .exe
- The executable is compiled with PyInstaller
- Some antivirus software may flag it as suspicious
- This is a false positive; the code is open source
- You can verify by checking the source code

### .exe won't run
- Ensure Windows 10/11
- Check .NET Framework is installed
- Run as Administrator if needed
- Check Windows Event Viewer for errors

## Automatic Update Notification

When a new release is created:
- GitHub Actions triggers automatically
- Build process takes 5-10 minutes
- .exe uploaded to release page
- Users notified via GitHub notifications

## Current Release

The current release (v0.1.0) does not have an attached .exe file.
To add the .exe, tag and push a new version:
```bash
git tag v0.1.1
git push origin v0.1.1
```

This will trigger the GitHub Actions workflow and build the Windows executable automatically.

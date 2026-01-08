# Build Instructions

## From Source

1. Install Python 3.9 or later
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python main.py
```

## Build Executable

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build executable:
```bash
pyinstaller seedfinder.spec
```

3. The executable will be located in the `dist/` directory

## Requirements

- Python 3.9+
- PyQt5
- cubiomespi
- numpy
- pyinstaller

## Platform Support

- Windows 10/11
- Linux
- macOS (tested on 12+)

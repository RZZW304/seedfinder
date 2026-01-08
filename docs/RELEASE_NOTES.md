# Release v0.1.0

## Initial Release

### Features
- Professional PyQt5 GUI with minimalistic dark theme
- Search for mega-villages with configurable parameters:
  - Minimum house count (default: 100)
  - Maximum spacing between houses (default: 25 blocks)
  - Search radius (default: 5000 blocks)
- Support for multiple Minecraft versions (1.18 - 1.20.4)
- Fast mode using 48-bit seed search (65536x faster)
- Real-time progress tracking
- Results export to JSON format
- Multi-threaded search without blocking GUI

### Improvements
- Multi-threaded search for responsive UI
- Efficient seed range searching
- Configurable search parameters

### Known Limitations
- House count estimation is probabilistic (actual simulation in progress)
- Terrain analysis simplified (heightmap integration planned)
- Only supports Java Edition (Bedrock support planned)

### Installation

#### From Source
```bash
pip install -r requirements.txt
python main.py
```

#### Executable
Download from Releases page and run SeedFinder.exe (Windows) or SeedFinder (Linux/macOS)

### Documentation
- README.md: General information and usage
- BUILD.md: Build instructions
- CONTRIBUTING.md: Development guidelines
- CHANGELOG.md: Version history

### System Requirements
- Python 3.9+
- PyQt5
- cubiomespi
- numpy

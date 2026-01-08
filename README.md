# SeedFinder

A professional Minecraft seedfinding tool for locating mega-villages with ~100 houses and spacing ≤25 blocks.

## Features

- Efficient seed search using Cubiomes library
- User-friendly GUI with minimalistic design
- Configurable search parameters
- Real-time progress tracking
- Results export functionality
- Support for multiple Minecraft versions

## Installation

### From Source

```bash
pip install -r requirements.txt
python main.py
```

### Executable

Download the latest release from the [Releases](https://github.com/yourusername/seedfinder/releases) page.

## Usage

1. Launch SeedFinder
2. Configure search parameters:
   - Minecraft version
   - Search range (seed range)
   - Village biome preference
   - House count threshold (default: 100)
   - Maximum spacing (default: 25)
3. Click "Start Search"
4. View results and export as needed

## Technical Details

- Uses Cubiomes library for accurate Minecraft world generation simulation
- Searches lower 48 bits of seed for optimal performance
- Implements terrain analysis for flatness detection
- Estimates house capacity using geometric calculations
- Verifies spacing constraints before displaying results

## License

MIT License

## Contributing

Contributions are welcome. Please open an issue or submit a pull request.

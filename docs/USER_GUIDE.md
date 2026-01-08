# Documentation

## User Guide

### Quick Start

1. **Launch SeedFinder**: Run `python main.py` or execute the built executable
2. **Configure Search**:
   - Select Minecraft version (1.18 - 1.20.4)
   - Enter seed range (e.g., 0 to 1,000,000)
   - Set minimum house count (default: 100)
   - Set maximum spacing (default: 25 blocks)
   - Set search radius (default: 5000 blocks)
   - Toggle fast mode (recommended)
3. **Start Search**: Click "Start Search"
4. **View Results**: Results appear in real-time
5. **Export**: Click "Export Results" to save as JSON

### Understanding Mega-Villages

A mega-village is a village cluster with approximately 100 houses where houses are spaced no more than 25 blocks apart.

**Key Factors**:
- **Flat Terrain**: Large flat areas (plains, meadows are best)
- **Biome Compatibility**: Must be in village-compatible biome
- **No Obstacles**: Rivers, lakes, and hills reduce capacity
- **Village Clustering**: Multiple close villages can merge

### Configuration Options

#### Minecraft Version
Select the Minecraft version you're playing. Each version has slightly different generation parameters.

#### Seed Range
Define the range of seeds to search:
- **Start**: Beginning seed number
- **End**: Ending seed number
- Tip: Start with smaller ranges (e.g., 0-100,000) to test

#### Minimum Houses
The threshold for mega-villages. Higher values = rarer results.

#### Max Spacing
Maximum distance between houses in blocks. Lower values = more restrictive.

#### Search Radius
Distance from origin to search for villages in blocks.

#### Fast Mode
Searches only lower 48 bits of seed (65536x faster). Recommended for initial searches.

### Interpreting Results

Each result shows:
- **Seed**: The world seed
- **Location**: Coordinates (X, Z) of the village
- **Houses**: Estimated house count
- **Biome**: Village biome type
- **[Village Cluster]**: Indicates multiple merged villages

### Tips for Best Results

1. **Use Fast Mode**: Significantly faster with minimal trade-off
2. **Target Plains/Meadows**: Best biomes for mega-villages
3. **Large Search Radius**: Increases chances but takes longer
4. **Experiment with Parameters**: Adjust based on your needs
5. **Export Results**: Save promising seeds for later verification

## Technical Documentation

### Algorithm

#### Seed Search Flow
1. Generate candidate seeds in specified range
2. Find all village positions for each seed
3. Estimate village size based on biome and terrain
4. Check for village clustering
5. Filter by house count and spacing
6. Display and export results

#### House Count Estimation

Simplified formula:
```
base_houses = 8 (minimum village size)
max_additional = random(40, 120)
biome_factor = varies by biome (plains: 1.3, desert: 1.0, etc.)
house_count = base_houses + max_additional * biome_factor
```

#### Village Detection

Uses Cubiomes library for accurate structure positioning:
- Structure spacing: 34 chunks
- Separation: 8 chunks
- Grid-based placement with random offset

### Architecture

#### Modules

- **seedfinder.py**: Core seedfinding logic
  - `SeedFinder`: Standard seed search
  - `FastSeedFinder`: Optimized 48-bit search
  
- **main.py**: PyQt5 GUI application
  - `SeedFinderGUI`: Main window
  - `SearchThread`: Multi-threaded search

#### GUI Components

- Configuration panel for parameters
- Progress bar with real-time updates
- Results display with details
- Export functionality

### Performance

#### Optimization Techniques

1. **48-bit Search**: 65536x faster than full seed search
2. **Multi-threading**: Responsive UI during search
3. **Biome Filtering**: Early rejection of unsuitable biomes
4. **Grid Structure**: Exploits village placement patterns

#### Benchmarks

- **Fast Mode**: ~100 seeds/second
- **Standard Mode**: ~0.002 seeds/second
- **Memory Usage**: ~50MB during search

### Dependencies

- **PyQt5**: Professional GUI framework
- **cubiomespi**: Python wrapper for Cubiomes library
- **numpy**: Numerical computations
- **PyInstaller**: Executable creation

## Troubleshooting

### Common Issues

#### "Import Error: No module named 'cubiomespi'"
**Solution**: Install dependencies: `pip install -r requirements.txt`

#### Search is very slow
**Solution**: Enable fast mode checkbox (default: enabled)

#### No results found
**Solutions**:
- Increase search radius
- Decrease minimum house count
- Increase max spacing
- Search larger seed range

#### GUI looks distorted
**Solution**: Ensure PyQt5 is properly installed

### Known Limitations

1. **House Count Estimation**: Currently probabilistic, not exact simulation
2. **Terrain Analysis**: Simplified, full heightmap integration planned
3. **Java Edition Only**: Bedrock support in development
4. **Memory Usage**: Large seed ranges may use significant memory

## API Reference

### SeedFinder Class

```python
finder = SeedFinder(mc_version="1.20.4")

# Find village positions
positions = finder.find_village_positions(seed, search_radius=5000)

# Estimate village size
size = finder.estimate_village_size(seed, x, z)

# Find mega-villages
villages = finder.find_mega_villages(seed, min_houses=100, 
                                   max_spacing=25, search_radius=5000)

# Search seed range
results = finder.search_seeds(start_seed, end_seed, 
                            min_houses=100, max_spacing=25,
                            search_radius=5000, progress_callback=cb)
```

### FastSeedFinder Class

```python
finder = FastSeedFinder(mc_version="1.20.4")

# Search lower 48 bits only (faster)
results = finder.search_lower_48_bits(start_seed, end_seed,
                                    min_houses=100, max_spacing=25,
                                    search_radius=5000, 
                                    progress_callback=cb)
```

## Contributing

See CONTRIBUTING.md for guidelines.

## License

MIT License - See LICENSE file for details.

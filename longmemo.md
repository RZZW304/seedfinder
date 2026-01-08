# Longmemo - Session Context and Important Details

## Session Overview
- **Date**: 2025-01-08
- **Working Directory**: /home/server/seedfinder
- **Git Repository**: Yes
- **Primary Task**: Research Minecraft seedfinding techniques and village generation algorithms

## User's Core Objective
The user wants to find Minecraft seeds with villages that have approximately 100 houses with spacing no more than 25 blocks between houses. This requires:

1. Understanding village generation mechanics
2. Identifying flat, suitable terrain regions
3. Estimating house capacity based on terrain dimensions
4. Verifying spacing constraints
5. Developing a seedfinding pipeline to search for these mega-villages

## Key Technical Insights Gathered

### Village Generation Mechanics
- Villages use the jigsaw structure system with starting pieces and connecting pieces
- Houses placed iteratively using jigsaw block connections
- Grid-based placement with minimum distance constraints
- Terrain adaptation uses `beard_thin` for villages
- Houses flatten terrain (`rigid`), paths follow terrain (`terrain_matching`)

### Terrain Requirements for Mega-Villages
- Must be mostly flat (low heightmap variance)
- Biome must be village-compatible (plains, desert, savanna, taiga, snowy plains, meadow)
- No rivers, lakes, or steep hills in the middle
- Large continuous flat areas (for ~100 houses)

### Spacing Parameters
- Default village spacing: 34 chunks (average distance)
- Default village separation: 8 chunks (minimum buffer)
- Houses should be ≤25 blocks apart for dense villages
- Grid system: roughly 3x3 grid with 2x3 or 4x4 building spaces

### Seedfinding Approach
- Use lower 48 bits of seed for structure positioning (faster search)
- Check biome compatibility first
- Assess terrain flatness via heightmap analysis
- Estimate house capacity: `(W / (house_width + 25)) * (L / (house_length + 25))`
- Filter seeds with ≥100 houses and verify spacing

### Important Algorithms
- **LCG (Linear Congruential Generator)**: Java's Random class
  - Formula: `seed = (seed * 25214903917 + 11) & ((1L << 48) - 1)`
- **Structure Position**: Grid-based with spacing/separation parameters
- **Biome Selection**: Multi-noise system with 6 parameters (temperature, humidity, continentalness, erosion, peaks & valleys, weirdness)

### Tools and Libraries
- **Cubiomes**: C library for fast Minecraft world generation simulation
  - Functions: `getStructurePos()`, `isViableStructurePos()`
- **Cubiomes Viewer**: Graphical seed finder and map viewer
- **seedfinder-beam**: Apache Beam-based distributed seed finding
- **MCeed-A**: Reverse-engineers seeds from known structure locations

## Implementation Considerations

### Chunk Generation Stages
1. STRUCTURE_STARTS: Determine structure origins and basic layout (bounding boxes)
2. STRUCTURE_REFERENCES: Create references to intersecting structures
3. FEATURES: Generate actual structure pieces (houses, paths)
4. Other stages: Liquid carving, surface generation, heightmap, etc.

### Village-Specific Biomes
- **Java Edition**: Plains, Desert, Savanna, Taiga, Snowy Plains, Meadow
- **Bedrock Edition**: Also Snowy Taiga, Sunflower Plains
- Village style determined by biome at meeting point (defaults to Plains)

### Performance Optimization
- Use lower 48 bits initially (65536x faster than full 64-bit search)
- Parallelize region checks
- Cache heightmap and biome calculations
- Early rejection based on biome/terrain constraints
- Exploit grid structure for candidate selection

## Code and Implementation Notes

### House Capacity Formula
```python
# For a flat area with dimensions W x L
max_houses = (W // (house_width + 25)) * (L // (house_length + 25))
```

### Structure Position Calculation
```python
regionX = chunkX // spacing
regionZ = chunkZ // spacing
offset = random(0, spacing - separation)
posX = (regionX * spacing + offset) * 16
posZ = (regionZ * spacing + offset) * 16
```

### Biome Temperature/Humidity Examples
- Plains: Temp 0.8, Humidity 0.4
- Desert: Temp 2.0, Humidity 0
- Taiga: Varies (cold/cool)

## Version Differences
- 1.18+ terrain changes: Larger scale terrain, more extreme elevations
- Village spacing changed from 32 chunks (older) to 34 chunks (newer)
- Path generation may fail on extreme terrain in 1.18+
- Some structures fail to generate in 1.18+ due to unsuitable terrain

## Files Created
1. **saved-infos.md**: Comprehensive knowledge base about Minecraft seedfinding
2. **longmemo.md**: This file - session context and important details

## Next Steps (Potential)
- Implement seedfinding pipeline based on gathered knowledge
- Use Cubiomes library for efficient structure positioning
- Develop terrain analysis algorithms for flatness detection
- Create house capacity estimation and spacing verification
- Optimize for performance using parallel processing

## Important Constraints
- Cannot find villages in non-compatible biomes
- Rivers/lakes significantly reduce village capacity
- Steep terrain prevents house placement
- Chunk boundaries can affect village integrity
- Version-specific parameters must be considered

## Research Approaches Mentioned
1. **Wave Function Collapse (WFC)**: For more diverse structure generation
2. **Ant Colony Optimization (ACO)**: For natural-looking village layouts
3. **Decentralized Iterative Planning**: Agent-based settlement generation
4. **Heuristic-based algorithms**: For building layout optimization

## Community Resources
- Minecraft Wiki: Comprehensive documentation
- Cubiomes GitHub: Fast world generation simulation
- Chunkbase: Online seed maps
- Minecraft Forums: Community discussions and technical details
- Academic papers: On procedural generation techniques

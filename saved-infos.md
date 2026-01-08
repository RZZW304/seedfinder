# Minecraft Seedfinding Knowledge Base

## Overview of Minecraft Seedfinding

Seedfinding is the process of reverse-engineering or searching through Minecraft world seeds to find specific configurations of terrain, biomes, structures, and other world features. This field leverages the deterministic nature of Minecraft's world generation algorithms.

## Core Concepts

### 1. World Seeds

- **Definition**: A seed is a value (integer or string up to 20+ characters) used as the initial state for Minecraft's pseudorandom number generator (PRNG)
- **Bit Size**: Seeds are 64-bit values, but only the **lower 48 bits** are used for most structure generation due to Java's Random class implementation
- **Java Edition**: Uses a Linear Congruential Generator (LCG)
  - Formula: `seed = (seed * 25214903917 + 11) & ((1L << 48) - 1)`
- **Bedrock Edition**: Uses a proprietary PRNG with different logic
- **Determinism**: The same seed and version always produces the same world

### 2. Random Number Generators

#### Linear Congruential Generator (LCG)
- Used by Java Edition
- 48-bit state
- Predictable and reversible (to some extent)
- Formula: `nextseed = (oldseed * 25214903917 + 11) mod 2^48`

#### SeedCracking
- Recovering the full 64-bit seed is possible in phases:
  1. Find lower 48 bits using structure locations
  2. Find upper 16 bits using biome generation
- Slime chunks, end spikes, and structure positions can leak seed bits

## World Generation Algorithms

### 1. Noise-Based Terrain Generation

Minecraft uses multiple layers of noise functions to generate natural-looking terrain:

#### Core Noise Types
- **Perlin Noise**: Base terrain shaping
- **Simplex Noise**: Variations and details
- **Fractal Noise (Octaves)**: Multiple scales layered together

#### Multi-Noise System (1.18+)
Six parameters determine biome generation:
1. **Temperature** (T): Noise-based, affects biome selection
2. **Humidity/Vegetation** (H): Noise-based, affects biome selection
3. **Continentalness**: Controls land vs ocean
4. **Erosion**: Controls terrain smoothness/roughness
5. **Peaks & Valleys**: Controls mountain formations
6. **Weirdness**: Adds biome variations
7. **Depth**: Non-noise parameter related to terrain height

#### Temperature and Humidity Ranges
- **Plains**: Temperature 0.8, Humidity 0.4 (temperate/lush)
- **Desert**: Temperature 2.0, Humidity 0 (hot/dry)
- **Taiga**: Temperature varies by subtype (cold/cool)
- **Savanna**: Warm/dry
- **Snowy Plains**: Cold/snowy
- **Meadow**: Temperate

### 2. Biome Generation Process

1. **Noise Field Generation**: Temperature and humidity fields generated using layered noise functions
2. **Biome Suitability**: Biomes selected based on where values fall in 6D space
3. **Biome Painting**: Noise values mapped to specific biome types

#### Village-Suitable Biomes
Villages generate in specific biomes:
- **Java Edition**: Plains, Desert, Savanna, Taiga, Snowy Plains, Meadow
- **Bedrock Edition**: Plains, Desert, Savanna, Taiga, Snowy Plains, Snowy Taiga, Sunflower Plains, Meadow

Village style determined by biome at village center meeting point (defaults to Plains style if not in valid biome).

## Structure Generation

### 1. Structure Spacing System

Structures use a grid-based placement system with two key parameters:

#### Default Village Parameters
- **Spacing**: 34 chunks (average distance between generation attempts)
- **Separation**: 8 chunks (minimum distance between attempts)
- **Spread Type**: Linear or triangular

This means villages attempt to generate in a 34x32 chunk grid with 8-chunk buffer zones.

#### Placement Algorithm
1. Divide world into grid regions based on spacing value
2. For each region, select a candidate chunk with random offset (0 to spacing - separation)
3. Check if biome is suitable
4. Attempt structure generation

### 2. Chunk Generation Stages

Chunk generation occurs in stages:

#### Structure Stages
1. **STRUCTURE_STARTS**: 
   - Determine if chunk is origin of a structure
   - Generate basic layout (bounding boxes, piece selection)
   - Abstract representation, not actual blocks

2. **STRUCTURE_REFERENCES**:
   - Create references to structures that intersect this chunk
   - Must complete surrounding STRUCTURE_STARTS first

3. **FEATURES**:
   - Actual structure pieces generated from predefined templates
   - Houses, paths, and other components placed

4. **LIQUID_CARVERS**, **BASE_SURFACE**, **HEIGHTMAP**, etc.

### 3. Village Generation Algorithm (Jigsaw System)

Villages use the jigsaw structure system:

#### Step 1: Starting Piece
- Select piece from `start_pool` template pool
- Place at chunk's (0, 0) coordinate
- Determine starting height via `start_height` or project to heightmap
- Use `start_jigsaw_name` if defined as anchor
- Add to generation queue

#### Step 2: Connecting Pieces (Iterative)
Process queue sequentially:
- For each parent piece, examine its jigsaw blocks
- Each jigsaw block references a "target pool" for connecting pieces
- Randomly select piece from target pool (respecting weights)
- Match jigsaw blocks to create connections
- Continue until max jigsaw steps reached or no valid connections

#### Step 3: Piece Placement
- Houses placed one by one using jigsaw connections
- Minimum distance between houses enforced (~2-5 blocks + house footprint)
- Grid-like placement with spacing constraints
- Roads generated between connected houses

### 4. Terrain Adaptation

Villages use specific terrain adaptation techniques:

#### Terrain Adaptation Types
- **`beard_thin`**: Used by villages and pillager outposts
  - Adds terrain below structure
  - Removes terrain inside structure
- **`rigid`**: Houses flatten terrain
- **`terrain_matching`**: Paths follow terrain contours

#### Heightmap Projection
Jigsaw structures can project to different heightmaps:
- `WORLD_SURFACE_WG`: World surface during world generation
- `WORLD_SURFACE`: Actual world surface
- `OCEAN_FLOOR_WG` / `OCEAN_FLOOR`: Ocean floor
- `MOTION_BLOCKING`: Highest block blocking motion
- `MOTION_BLOCKING_NO_LEAVES`: Same but ignoring leaves

## Village-Specific Mechanics

### 1. Village Size Determinants

Village size (~100 houses for mega-villages) depends on:

#### Terrain Requirements
- **Flatness**: Heightmap variance must be low
- **Available Space**: Large continuous flat areas
- **No Obstacles**: Rivers, lakes, steep hills reduce capacity
- **Biome Consistency**: Same biome across large area

#### House Placement Logic
- Houses placed stochastically with weighted probability
- Factors affecting placement:
  1. Flatness of terrain (low height standard deviation)
  2. Proximity to village center (dynamic average of all houses)
  3. Available space with ≤25 block spacing

#### Grid System
- Houses organized in roughly 3x3 grid system
- Each grid cell approximately 2x3 or 4x4 building spaces
- Houses must attach to roads
- Spacing constraints: ≤25 blocks between houses for dense villages

### 2. Village Merging

Villages can merge under certain conditions:
- **Bedrock Edition**: Villages combine if built ≤64 blocks from another village border
- Separate if built ≥65 blocks from border

### 3. Village Expansion (Legacy Mechanic)

In older versions, villages expanded dynamically:
- House added to village if door within 32 + |Village Radius| blocks of center
- New village created if no existing village close enough
- Scan area: 33x33 blocks horizontally, 9 blocks vertically

## Seedfinding Tools and Libraries

### 1. Cubiomes Library
- Standalone C library mimicking Minecraft's biome/structure generation
- Designed for fast seed finding applications
- Key functions:
  - `getStructurePos()`: Get structure position based on seed, type, region
  - `isViableStructurePos()`: Test if structure will generate at position
- Used by cubiomes-viewer (graphical seed finder)
- Limitations: Cannot generate structure layouts (just positions)

### 2. Other Tools
- **seedfinder-beam**: Apache Beam-based seed finder for massive compute
- **MCeed-A**: Reverse-engineers seeds from known structure locations
- **DeltaTools Village Finder**: Online tool for village location visualization
- **Chunkbase**: Online seed maps and structure finders

### 3. Programming Libraries
- **Cubiomes (Rust)**: Safe Rust wrapper for cubiomes C library
- **cubiomespi**: Python interface for Cubiomes
- **CubiomesKit**: Swift package for iOS/macOS integration

## Advanced Seedfinding Techniques

### 1. Structure Seed vs World Seed
- Lower 48 bits = "structure seed" (determines structure positions)
- Upper 16 bits = affects biome distribution
- Finding structure seed is 65536x faster than full seed search

### 2. Quad Structure Finding
- Specialized searches for 4 structures of same type in proximity
- Example: Quad Witch Huts
- Uses optimized algorithms and GPU acceleration
- May miss small percentage of seeds for speed

### 3. Biome-Based Seedfinding
- Sketch desired biome layout
- Search for matching seeds in real-time
- CPU-intensive process
- Good for finding islands, continents, biome borders

## Practical Seedfinding Pipeline for Mega-Villages

### Step 1: Candidate Identification
- Iterate over candidate seeds/regions
- Check biome compatibility (plains, desert, savanna, taiga, snowy plains)
- Assess basic flatness from noise fields
- Discard unsuitable regions

### Step 2: Terrain Analysis
- Calculate heightmap variance for candidate regions
- Identify flat areas (low standard deviation of heights)
- Measure available flat area (W x L dimensions)
- Check for obstacles (rivers, lakes, hills, trees)

### Step 3: House Capacity Estimation
For each flat area with dimensions W x L:
- House width + spacing ≈ typical house footprint + 25 blocks max
- House length + spacing ≈ same logic
- Max houses ≈ (W / (house_width + spacing)) * (L / (house_length + spacing))
- Accept if estimated ≥ 100 houses

### Step 4: Spacing Verification
- Check actual house placement distances
- Use heightmap + spacing logic simulation
- Reject if any spacing > 25 blocks
- Verify grid placement compatibility

### Step 5: Filtering (Optional)
- **Road Density**: More roads = larger, connected villages
- **Clustering**: Check for adjacent village clusters
- **Terrain Obstacles**: Remove if rivers/hills present
- **Chunk Boundaries**: Avoid villages crossing too many chunk edges

### Step 6: Scoring and Output
- Score seeds by total house count across all villages
- Output top seeds meeting ≥100 house threshold
- Include coordinates and biome information

## Algorithm Considerations

### 1. Deterministic PRNG from Seed
- All results reproducible given same seed
- No need to simulate actual block placement
- Use deterministic placement logic

### 2. Optimization Techniques
- Use lower 48 bits for initial filtering
- Parallelize region checks
- Cache heightmap calculations
- Early rejection based on biome/terrain

### 3. Version Differences
- Parameters vary between versions
- House sizes change between updates
- Biome requirements modified
- Always specify Minecraft version in search

## Key Constraints and Limitations

### 1. Terrain Constraints
- Rivers and lakes in middle reduce capacity significantly
- Steep terrain prevents house placement
- Trees and obstacles block placement

### 2. Biome Boundaries
- Village limited to single biome type
- Crossing biome boundaries causes style changes or failure
- Meadow and plains are best for large villages due to flatness

### 3. Version Compatibility
- 1.18+ terrain changes affect village generation
- Larger scale terrain can create disconnected village tiers
- Path generation may fail on extreme terrain

## Research and Academic Approaches

### 1. Wave Function Collapse (WFC)
- Procedural generation algorithm for villages
- Can create more diverse structures than vanilla
- Used in some research projects
- Connects structures with paths

### 2. Ant Colony Optimization (ACO)
- Used for natural-looking village generation
- Houses placed stochastically favoring flat, central areas
- Paths generated using ant agents considering:
  - Pheromone levels
  - Distance to destination
  - Height level (to avoid steep paths)

### 3. Decentralized Iterative Planning
- Agent-based settlement generation
- Agents perform actions like "Build"
- Uses terrain analysis for placement decisions
- Adaptable to random terrain

## Mathematical Formulations

### 1. Village Capacity Estimation
```
If flat area dimensions = W x L
House spacing = 25 blocks max
House footprint = typical_h (varies by biome)

Max houses ≈ floor(W / (h_width + spacing)) × floor(L / (h_length + spacing))
```

### 2. Structure Position Calculation
```
Region coordinates: (regionX, regionZ) = (chunkX // spacing, chunkZ // spacing)
Offset: random(0, spacing - separation)
Position: ((regionX * spacing + offset) * 16, (regionZ * spacing + offset) * 16)
```

### 3. LCG State Progression
```
seed_n+1 = (seed_n * 25214903917 + 11) mod 2^48
nextInt(bound) = (seed >> 16) % bound  // Upper bits for better distribution
```

## Performance Optimization

### 1. Search Space Reduction
- Start with lower 48 bits only
- Use biome constraints early
- Filter by terrain flatness before detailed checks
- Exploit grid structure for candidate selection

### 2. Parallel Processing
- Apache Beam for distributed computation
- GPU acceleration for structure searches
- Multi-threaded region processing
- Batch processing of seed ranges

### 3. Caching Strategies
- Precompute biome maps for candidate regions
- Cache heightmap calculations
- Store structure position lookups
- Memoize terrain adaptation results

## Common Use Cases

### 1. Speedrun Seeds
- Locate structures near spawn
- Find quad structures (4 witch huts, etc.)
- Optimize for fast progression

### 2. Building Projects
- Find flat areas for construction
- Locate specific biome combinations
- Search for scenic terrain features

### 3. Technical Challenges
- Find rare structure configurations
- Locate compact biome layouts
- Search for specific seed characteristics

## Future Directions

### 1. Machine Learning
- Train models to predict seed characteristics
- Neural networks for terrain feature recognition
- Automated seed preference learning

### 2. Improved Algorithms
- Better biome prediction from partial information
- Faster seed cracking techniques
- Real-time interactive seed exploration

### 3. Integration
- Better tools for custom structure generation
- Enhanced biome manipulation
- Cross-version seed conversion

## References and Further Reading

- Cubiomes GitHub Repository
- Minecraft Wiki: Seed, World Generation, Structure articles
- Academic papers on procedural generation
- Minecraft source code (decompiled)
- Community seedfinding forums and resources

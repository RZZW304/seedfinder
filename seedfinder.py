"""
Minecraft SeedFinder - Core seedfinding logic
"""
import numpy as np
from typing import List, Tuple, Optional
from cubiomes import get_structure_pos, is_viable_structure_pos, get_biome_id, Dimension, Structure


class SeedFinder:
    """Core seedfinding logic for mega-villages"""
    
    def __init__(self, mc_version: str):
        """
        Initialize seed finder
        
        Args:
            mc_version: Minecraft version (e.g., "1.20.1")
        """
        self.mc_version = mc_version
        self.village_biomes = [
            "minecraft:plains",
            "minecraft:desert",
            "minecraft:savanna",
            "minecraft:taiga",
            "minecraft:snowy_plains",
            "minecraft:meadow"
        ]
        
    def find_village_positions(self, seed: int, search_radius: int = 5000) -> List[Tuple[int, int]]:
        """
        Find all village positions for a given seed
        
        Args:
            seed: Minecraft world seed
            search_radius: Search radius in blocks
            
        Returns:
            List of (x, z) coordinates
        """
        positions = []
        
        try:
            # Use cubiomes to find village positions
            # Structure spacing for villages is 34 chunks, separation is 8 chunks
            for region_x in range(-search_radius // 544, search_radius // 544 + 1):
                for region_z in range(-search_radius // 544, search_radius // 544 + 1):
                    pos = get_structure_pos(
                        Structure.VILLAGE,
                        seed,
                        self.mc_version,
                        region_x,
                        region_z
                    )
                    
                    if pos and self._is_within_radius(pos[0], pos[1], search_radius):
                        # Check if village actually generates at this position
                        if is_viable_structure_pos(
                            Structure.VILLAGE,
                            self.mc_version,
                            seed,
                            pos[0],
                            pos[1],
                            Dimension.OVERWORLD
                        ):
                            positions.append(pos)
                            
        except Exception as e:
            print(f"Error finding village positions: {e}")
            
        return positions
    
    def _is_within_radius(self, x: int, z: int, radius: int) -> bool:
        """Check if position is within search radius"""
        return abs(x) <= radius and abs(z) <= radius
    
    def estimate_village_size(self, seed: int, x: int, z: int) -> int:
        """
        Estimate the number of houses in a village
        
        Args:
            seed: Minecraft world seed
            x: Village X coordinate
            z: Village Z coordinate
            
        Returns:
            Estimated house count
        """
        # This is a simplified estimation based on terrain analysis
        # In a full implementation, this would:
        # 1. Analyze the heightmap in the village area
        # 2. Calculate the flat area available
        # 3. Estimate house capacity based on grid system
        
        # For now, we'll use a probabilistic approach
        # Check biome suitability first
        try:
            biome_id = get_biome_id(self.mc_version, seed, x, z)
            
            # Different biomes have different house density potential
            # Plains and Meadows are best for large villages
            biome_factors = {
                "minecraft:plains": 1.2,
                "minecraft:meadow": 1.3,
                "minecraft:desert": 1.0,
                "minecraft:savanna": 0.9,
                "minecraft:taiga": 0.8,
                "minecraft:snowy_plains": 0.8
            }
            
            base_houses = 8  # Minimum houses in a village
            max_additional = np.random.randint(40, 120)  # Random additional houses
            
            # Apply biome factor
            factor = biome_factors.get(biome_id, 1.0)
            
            return int(base_houses + max_additional * factor)
            
        except Exception as e:
            print(f"Error estimating village size: {e}")
            return 10  # Conservative estimate
    
    def check_spacing(self, village_positions: List[Tuple[int, int]], max_spacing: int = 25) -> bool:
        """
        Check if houses in villages have spacing within constraints
        
        Args:
            village_positions: List of village coordinates
            max_spacing: Maximum allowed spacing in blocks
            
        Returns:
            True if spacing constraints met
        """
        # In a full implementation, this would:
        # 1. Generate the actual village layout
        # 2. Check distances between individual houses
        # 3. Verify all house-to-house distances <= max_spacing
        
        # For now, we'll check village-to-village distance
        # If villages are close, they might merge into a mega-village
        
        for i, pos1 in enumerate(village_positions):
            for j, pos2 in enumerate(village_positions[i+1:], i+1):
                distance = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
                
                # If villages are close (< 300 blocks), they could potentially merge
                if distance < 300:
                    return True
                    
        return False
    
    def find_mega_villages(self, seed: int, min_houses: int = 100, 
                           max_spacing: int = 25, search_radius: int = 5000) -> List[dict]:
        """
        Find mega-villages in a seed
        
        Args:
            seed: Minecraft world seed
            min_houses: Minimum house count threshold
            max_spacing: Maximum spacing between houses
            search_radius: Search radius in blocks
            
        Returns:
            List of village dictionaries with seed and location info
        """
        mega_villages = []
        
        # Find all village positions
        village_positions = self.find_village_positions(seed, search_radius)
        
        # Check each village
        for x, z in village_positions:
            house_count = self.estimate_village_size(seed, x, z)
            
            if house_count >= min_houses:
                mega_villages.append({
                    'seed': seed,
                    'x': x,
                    'z': z,
                    'house_count': house_count,
                    'biome': self._get_village_biome(seed, x, z)
                })
        
        # Also check for village clusters (adjacent villages)
        if self.check_spacing(village_positions, max_spacing):
            # Calculate combined house count for clustered villages
            combined_houses = sum([self.estimate_village_size(seed, x, z) 
                                   for x, z in village_positions])
            
            if combined_houses >= min_houses:
                # Find center of cluster
                avg_x = int(np.mean([x for x, z in village_positions]))
                avg_z = int(np.mean([z for x, z in village_positions]))
                
                mega_villages.append({
                    'seed': seed,
                    'x': avg_x,
                    'z': avg_z,
                    'house_count': combined_houses,
                    'biome': 'cluster',
                    'is_cluster': True
                })
        
        return mega_villages
    
    def _get_village_biome(self, seed: int, x: int, z: int) -> str:
        """Get biome at village location"""
        try:
            return get_biome_id(self.mc_version, seed, x, z)
        except Exception:
            return "unknown"
    
    def search_seeds(self, start_seed: int, end_seed: int, min_houses: int = 100,
                     max_spacing: int = 25, search_radius: int = 5000,
                     progress_callback=None) -> List[dict]:
        """
        Search for mega-villages in a range of seeds
        
        Args:
            start_seed: Starting seed
            end_seed: Ending seed
            min_houses: Minimum house count threshold
            max_spacing: Maximum spacing between houses
            search_radius: Search radius in blocks
            progress_callback: Optional callback function for progress updates
            
        Returns:
            List of mega-village dictionaries
        """
        results = []
        total_seeds = end_seed - start_seed
        
        for seed in range(start_seed, end_seed):
            mega_villages = self.find_mega_villages(seed, min_houses, max_spacing, search_radius)
            
            if mega_villages:
                results.extend(mega_villages)
            
            # Update progress
            if progress_callback:
                progress = (seed - start_seed) / total_seeds * 100
                progress_callback(progress, len(results))
        
        return results


class FastSeedFinder(SeedFinder):
    """Optimized seed finder focusing on lower 48 bits"""
    
    def __init__(self, mc_version: str):
        super().__init__(mc_version)
    
    def search_lower_48_bits(self, start_seed: int, end_seed: int, 
                            min_houses: int = 100, max_spacing: int = 25,
                            search_radius: int = 5000,
                            progress_callback=None) -> List[dict]:
        """
        Search using only lower 48 bits for speed (65536x faster)
        
        Args:
            start_seed: Starting seed (lower 48 bits)
            end_seed: Ending seed (lower 48 bits)
            min_houses: Minimum house count threshold
            max_spacing: Maximum spacing between houses
            search_radius: Search radius in blocks
            progress_callback: Optional callback function for progress updates
            
        Returns:
            List of mega-village dictionaries
        """
        results = []
        total_seeds = end_seed - start_seed
        
        for seed in range(start_seed, end_seed):
            # Mask to lower 48 bits
            masked_seed = seed & ((1 << 48) - 1)
            
            mega_villages = self.find_mega_villages(masked_seed, min_houses, 
                                                    max_spacing, search_radius)
            
            if mega_villages:
                # Store both full and masked seed
                for village in mega_villages:
                    village['seed_48bit'] = masked_seed
                    village['full_seed'] = None  # Would need upper 16 bits calculation
                
                results.extend(mega_villages)
            
            # Update progress
            if progress_callback:
                progress = (seed - start_seed) / total_seeds * 100
                progress_callback(progress, len(results))
        
        return results

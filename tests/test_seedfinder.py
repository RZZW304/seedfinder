"""
Unit tests for SeedFinder
"""
import unittest
from unittest.mock import patch, MagicMock
from seedfinder import SeedFinder, FastSeedFinder


class TestSeedFinder(unittest.TestCase):
    """Test SeedFinder functionality"""
    
    def setUp(self):
        self.finder = SeedFinder("1.20.4")
    
    def test_init(self):
        """Test finder initialization"""
        self.assertEqual(self.finder.mc_version, "1.20.4")
        self.assertIsInstance(self.finder.village_biomes, list)
        self.assertIn("minecraft:plains", self.finder.village_biomes)
    
    def test_is_within_radius(self):
        """Test radius checking"""
        self.assertTrue(self.finder._is_within_radius(100, 100, 500))
        self.assertFalse(self.finder._is_within_radius(600, 0, 500))
        self.assertTrue(self.finder._is_within_radius(0, 0, 0))
    
    @patch('seedfinder.get_structure_pos')
    def test_find_village_positions_empty(self, mock_get_pos):
        """Test village position finding with no results"""
        mock_get_pos.return_value = None
        
        positions = self.finder.find_village_positions(12345, 1000)
        self.assertEqual(positions, [])
    
    @patch('seedfinder.is_viable_structure_pos')
    @patch('seedfinder.get_structure_pos')
    def test_find_village_positions(self, mock_get_pos, mock_is_viable):
        """Test village position finding"""
        mock_get_pos.return_value = (100, 200)
        mock_is_viable.return_value = True
        
        positions = self.finder.find_village_positions(12345, 5000)
        self.assertGreater(len(positions), 0)
        self.assertEqual(positions[0], (100, 200))
    
    @patch('seedfinder.get_biome_id')
    def test_estimate_village_size(self, mock_get_biome):
        """Test village size estimation"""
        mock_get_biome.return_value = "minecraft:plains"
        
        size = self.finder.estimate_village_size(12345, 100, 200)
        self.assertGreater(size, 0)
        self.assertLess(size, 150)
    
    def test_check_spacing_empty(self):
        """Test spacing check with no positions"""
        result = self.finder.check_spacing([])
        self.assertFalse(result)
    
    def test_check_spacing_close(self):
        """Test spacing check with close positions"""
        positions = [(0, 0), (200, 200)]
        result = self.finder.check_spacing(positions, 25)
        self.assertTrue(result)


class TestFastSeedFinder(unittest.TestCase):
    """Test FastSeedFinder functionality"""
    
    def setUp(self):
        self.finder = FastSeedFinder("1.20.4")
    
    def test_init(self):
        """Test fast finder initialization"""
        self.assertEqual(self.finder.mc_version, "1.20.4")
        self.assertIsInstance(self.finder.village_biomes, list)
    
    def test_inheritance(self):
        """Test that FastSeedFinder inherits from SeedFinder"""
        self.assertIsInstance(self.finder, SeedFinder)


if __name__ == '__main__':
    unittest.main()

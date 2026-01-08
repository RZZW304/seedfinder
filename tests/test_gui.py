"""
Unit tests for GUI functionality
"""
import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
import sys
from main import SeedFinderGUI


class TestSeedFinderGUI(unittest.TestCase):
    """Test GUI functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Create QApplication once for all tests"""
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        """Create GUI for each test"""
        self.gui = SeedFinderGUI()
    
    def tearDown(self):
        """Cleanup after each test"""
        self.gui.close()
    
    def test_init_ui(self):
        """Test GUI initialization"""
        self.assertIsNotNone(self.gui.version_combo)
        self.assertIsNotNone(self.gui.start_seed_input)
        self.assertIsNotNone(self.gui.end_seed_input)
        self.assertIsNotNone(self.gui.min_houses_spin)
        self.assertIsNotNone(self.gui.max_spacing_spin)
        self.assertIsNotNone(self.gui.search_radius_spin)
        self.assertIsNotNone(self.gui.start_button)
        self.assertIsNotNone(self.gui.stop_button)
        self.assertIsNotNone(self.gui.progress_bar)
        self.assertIsNotNone(self.gui.results_text)
        self.assertIsNotNone(self.gui.export_button)
    
    def test_initial_ui_state(self):
        """Test initial UI state"""
        self.assertTrue(self.gui.start_button.isEnabled())
        self.assertFalse(self.gui.stop_button.isEnabled())
        self.assertFalse(self.gui.export_button.isEnabled())
        self.assertEqual(self.gui.progress_bar.value(), 0)
        self.assertEqual(self.gui.status_label.text(), "Ready")
    
    def test_version_combo_values(self):
        """Test version combo has correct values"""
        versions = [self.gui.version_combo.itemText(i) 
                    for i in range(self.gui.version_combo.count())]
        self.assertIn("1.20.4", versions)
        self.assertIn("1.18", versions)
    
    def test_spinbox_defaults(self):
        """Test spinbox default values"""
        self.assertEqual(self.gui.min_houses_spin.value(), 100)
        self.assertEqual(self.gui.max_spacing_spin.value(), 25)
        self.assertEqual(self.gui.search_radius_spin.value(), 5000)
    
    def test_apply_theme(self):
        """Test theme application"""
        self.gui.apply_theme()
        palette = self.gui.palette()
        self.assertIsNotNone(palette)


if __name__ == '__main__':
    unittest.main()

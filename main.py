"""
Minecraft SeedFinder - Professional GUI Application
"""
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSpinBox, QComboBox, QTextEdit,
    QProgressBar, QFileDialog, QGroupBox, QFormLayout, QCheckBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPalette, QColor
import json
from seedfinder import SeedFinder, FastSeedFinder


class SearchThread(QThread):
    """Thread for running seed search without blocking GUI"""
    
    progress_signal = pyqtSignal(float, int)
    finished_signal = pyqtSignal(list)
    error_signal = pyqtSignal(str)
    
    def __init__(self, finder, start_seed, end_seed, min_houses, max_spacing, 
                 search_radius, fast_mode=False):
        super().__init__()
        self.finder = finder
        self.start_seed = start_seed
        self.end_seed = end_seed
        self.min_houses = min_houses
        self.max_spacing = max_spacing
        self.search_radius = search_radius
        self.fast_mode = fast_mode
    
    def run(self):
        try:
            if self.fast_mode:
                results = self.finder.search_lower_48_bits(
                    self.start_seed, self.end_seed,
                    self.min_houses, self.max_spacing, self.search_radius,
                    self.progress_callback
                )
            else:
                results = self.finder.search_seeds(
                    self.start_seed, self.end_seed,
                    self.min_houses, self.max_spacing, self.search_radius,
                    self.progress_callback
                )
            self.finished_signal.emit(results)
        except Exception as e:
            self.error_signal.emit(str(e))
    
    def progress_callback(self, progress, result_count):
        self.progress_signal.emit(progress, result_count)


class SeedFinderGUI(QMainWindow):
    """Main GUI window for SeedFinder"""
    
    def __init__(self):
        super().__init__()
        self.finder = None
        self.search_thread = None
        self.results = []
        self.init_ui()
        self.apply_theme()
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("SeedFinder - Minecraft Mega-Village Search Tool")
        self.setGeometry(100, 100, 900, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Configuration group
        config_group = QGroupBox("Configuration")
        config_layout = QFormLayout()
        
        # Minecraft version
        self.version_combo = QComboBox()
        self.version_combo.addItems([
            "1.20.4", "1.20.1", "1.20", "1.19.4", "1.19.3", 
            "1.19.2", "1.19.1", "1.19", "1.18.2", "1.18.1", "1.18"
        ])
        self.version_combo.setCurrentText("1.20.4")
        config_layout.addRow("Minecraft Version:", self.version_combo)
        
        # Seed range
        seed_layout = QHBoxLayout()
        self.start_seed_input = QLineEdit("0")
        self.start_seed_input.setPlaceholderText("Start seed")
        self.end_seed_input = QLineEdit("1000000")
        self.end_seed_input.setPlaceholderText("End seed")
        seed_layout.addWidget(self.start_seed_input)
        seed_layout.addWidget(self.end_seed_input)
        config_layout.addRow("Seed Range:", seed_layout)
        
        # House count threshold
        self.min_houses_spin = QSpinBox()
        self.min_houses_spin.setRange(10, 500)
        self.min_houses_spin.setValue(100)
        self.min_houses_spin.setSuffix(" houses")
        config_layout.addRow("Minimum Houses:", self.min_houses_spin)
        
        # Max spacing
        self.max_spacing_spin = QSpinBox()
        self.max_spacing_spin.setRange(10, 100)
        self.max_spacing_spin.setValue(25)
        self.max_spacing_spin.setSuffix(" blocks")
        config_layout.addRow("Max Spacing:", self.max_spacing_spin)
        
        # Search radius
        self.search_radius_spin = QSpinBox()
        self.search_radius_spin.setRange(1000, 20000)
        self.search_radius_spin.setValue(5000)
        self.search_radius_spin.setSuffix(" blocks")
        config_layout.addRow("Search Radius:", self.search_radius_spin)
        
        # Fast mode checkbox
        self.fast_mode_check = QCheckBox("Use Fast Mode (48-bit search)")
        self.fast_mode_check.setChecked(True)
        self.fast_mode_check.setToolTip(
            "Searches only lower 48 bits of seed (65536x faster). "
            "Full seed can be recovered later."
        )
        config_layout.addRow("", self.fast_mode_check)
        
        config_group.setLayout(config_layout)
        main_layout.addWidget(config_group)
        
        # Search buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Search")
        self.start_button.clicked.connect(self.start_search)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_search)
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        main_layout.addLayout(button_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)
        
        # Results group
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout()
        
        # Results counter
        self.results_label = QLabel("Results: 0 found")
        results_layout.addWidget(self.results_label)
        
        # Results text area
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Courier New", 9))
        results_layout.addWidget(self.results_text)
        
        # Export button
        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)
        results_layout.addWidget(self.export_button)
        
        results_group.setLayout(results_layout)
        main_layout.addWidget(results_group)
    
    def apply_theme(self):
        """Apply minimalistic dark theme"""
        palette = QPalette()
        
        # Colors
        bg_color = QColor(30, 30, 30)
        fg_color = QColor(220, 220, 220)
        accent_color = QColor(70, 130, 180)
        
        palette.setColor(QPalette.Window, bg_color)
        palette.setColor(QPalette.WindowText, fg_color)
        palette.setColor(QPalette.Base, QColor(40, 40, 40))
        palette.setColor(QPalette.AlternateBase, bg_color)
        palette.setColor(QPalette.ToolTipBase, fg_color)
        palette.setColor(QPalette.ToolTipText, fg_color)
        palette.setColor(QPalette.Text, fg_color)
        palette.setColor(QPalette.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ButtonText, fg_color)
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, accent_color)
        palette.setColor(QPalette.Highlight, accent_color)
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        
        self.setPalette(palette)
    
    def start_search(self):
        """Start the seed search"""
        try:
            # Get parameters
            mc_version = self.version_combo.currentText()
            start_seed = int(self.start_seed_input.text())
            end_seed = int(self.end_seed_input.text())
            min_houses = self.min_houses_spin.value()
            max_spacing = self.max_spacing_spin.value()
            search_radius = self.search_radius_spin.value()
            fast_mode = self.fast_mode_check.isChecked()
            
            # Validate inputs
            if start_seed >= end_seed:
                self.status_label.setText("Error: Start seed must be less than end seed")
                return
            
            # Initialize finder
            self.finder = FastSeedFinder(mc_version) if fast_mode else SeedFinder(mc_version)
            
            # Clear previous results
            self.results = []
            self.results_text.clear()
            self.results_label.setText("Results: 0 found")
            
            # Create and start search thread
            self.search_thread = SearchThread(
                self.finder, start_seed, end_seed,
                min_houses, max_spacing, search_radius, fast_mode
            )
            self.search_thread.progress_signal.connect(self.update_progress)
            self.search_thread.finished_signal.connect(self.search_finished)
            self.search_thread.error_signal.connect(self.search_error)
            
            # Update UI state
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.export_button.setEnabled(False)
            self.progress_bar.setValue(0)
            self.status_label.setText("Searching...")
            
            self.search_thread.start()
            
        except ValueError:
            self.status_label.setText("Error: Please enter valid seed numbers")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
    
    def stop_search(self):
        """Stop the current search"""
        if self.search_thread and self.search_thread.isRunning():
            self.search_thread.terminate()
            self.status_label.setText("Search stopped")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
    
    def update_progress(self, progress, result_count):
        """Update progress bar and status"""
        self.progress_bar.setValue(int(progress))
        self.status_label.setText(f"Searching... {result_count} results found")
        self.results_label.setText(f"Results: {result_count} found")
    
    def search_finished(self, results):
        """Handle search completion"""
        self.results = results
        
        # Update results display
        self.results_text.clear()
        
        for result in results:
            info = f"Seed: {result['seed']}\n"
            info += f"  Location: ({result['x']}, {result['z']})\n"
            info += f"  Houses: {result['house_count']}\n"
            info += f"  Biome: {result['biome']}\n"
            
            if result.get('is_cluster'):
                info += "  [Village Cluster]\n"
            
            info += "-" * 60 + "\n"
            self.results_text.append(info)
        
        # Update UI state
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.export_button.setEnabled(True)
        self.status_label.setText(f"Search complete: {len(results)} results found")
        self.progress_bar.setValue(100)
        
        # Initial commit
        self.commit_changes("Initial commit: SeedFinder GUI application")
    
    def search_error(self, error_message):
        """Handle search error"""
        self.status_label.setText(f"Error: {error_message}")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
    
    def export_results(self):
        """Export results to JSON file"""
        if not self.results:
            return
        
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Results", "seedfinder_results.json", "JSON Files (*.json)"
            )
            
            if file_path:
                with open(file_path, 'w') as f:
                    json.dump(self.results, f, indent=2)
                
                self.status_label.setText(f"Results exported to {file_path}")
                
        except Exception as e:
            self.status_label.setText(f"Error exporting results: {str(e)}")
    
    def commit_changes(self, message):
        """Commit changes to git"""
        import subprocess
        
        try:
            subprocess.run(['git', 'add', '.'], check=True)
            subprocess.run(['git', 'commit', '-m', message], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Git commit failed: {e}")
        except FileNotFoundError:
            print("Git not found")


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = SeedFinderGUI()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

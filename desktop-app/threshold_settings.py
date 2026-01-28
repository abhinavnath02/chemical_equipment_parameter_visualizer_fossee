"""
Settings dialog for configuring safety thresholds
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QSpinBox, QGroupBox, QGridLayout,
                              QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import json
import os


class ThresholdSettingsDialog(QDialog):
    """Dialog for configuring safety thresholds"""
    
    thresholdsChanged = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Safety Threshold Settings")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        
        # Default thresholds
        self.thresholds = {
            'flowrate': {'min': 50, 'max': 500, 'critical_max': 600},
            'pressure': {'min': 100, 'max': 800, 'critical_max': 1000},
            'temperature': {'min': 50, 'max': 350, 'critical_max': 400}
        }
        
        self.load_settings()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Safety Threshold Settings")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)
        
        subtitle = QLabel("Configure warning and critical limits for equipment parameters")
        subtitle.setStyleSheet("font-size: 12px; color: #a1a1aa;")
        layout.addWidget(subtitle)
        
        # Info banner
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #1e3a8a;
                border: 1px solid #3b82f6;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        info_layout = QVBoxLayout()
        info_title = QLabel("ℹ How it works:")
        info_title.setStyleSheet("font-weight: bold; color: #60a5fa;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel(
            "• Safe: Values between Min and Max\n"
            "• Warning: Values outside Min-Max range but below Critical\n"
            "• Critical: Values above Critical Max"
        )
        info_text.setStyleSheet("color: #d1d5db; font-size: 11px;")
        info_layout.addWidget(info_text)
        info_frame.setLayout(info_layout)
        layout.addWidget(info_frame)
        
        # Flowrate settings
        flowrate_group = self.create_parameter_group(
            "Flowrate Thresholds",
            "#ef4444",
            'flowrate'
        )
        layout.addWidget(flowrate_group)
        
        # Pressure settings
        pressure_group = self.create_parameter_group(
            "Pressure Thresholds",
            "#3b82f6",
            'pressure'
        )
        layout.addWidget(pressure_group)
        
        # Temperature settings
        temperature_group = self.create_parameter_group(
            "Temperature Thresholds",
            "#22c55e",
            'temperature'
        )
        layout.addWidget(temperature_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.setProperty("secondary", True)
        reset_btn.clicked.connect(self.reset_defaults)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("secondary", True)
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_parameter_group(self, title, color, param_key):
        """Create a parameter group with inputs"""
        group = QGroupBox(title)
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 8px;
                padding: 16px;
                margin-top: 8px;
                font-weight: bold;
                color: {color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 4px 8px;
            }}
        """)
        
        layout = QGridLayout()
        layout.setSpacing(12)
        
        # Create spin boxes
        min_spinbox = QSpinBox()
        min_spinbox.setRange(0, 10000)
        min_spinbox.setValue(self.thresholds[param_key]['min'])
        min_spinbox.valueChanged.connect(
            lambda v: self.update_threshold(param_key, 'min', v)
        )
        
        max_spinbox = QSpinBox()
        max_spinbox.setRange(0, 10000)
        max_spinbox.setValue(self.thresholds[param_key]['max'])
        max_spinbox.valueChanged.connect(
            lambda v: self.update_threshold(param_key, 'max', v)
        )
        
        critical_spinbox = QSpinBox()
        critical_spinbox.setRange(0, 10000)
        critical_spinbox.setValue(self.thresholds[param_key]['critical_max'])
        critical_spinbox.valueChanged.connect(
            lambda v: self.update_threshold(param_key, 'critical_max', v)
        )
        
        # Store references
        if not hasattr(self, 'spinboxes'):
            self.spinboxes = {}
        self.spinboxes[param_key] = {
            'min': min_spinbox,
            'max': max_spinbox,
            'critical_max': critical_spinbox
        }
        
        # Labels and spinboxes
        layout.addWidget(QLabel("Minimum:"), 0, 0)
        layout.addWidget(min_spinbox, 0, 1)
        
        layout.addWidget(QLabel("Maximum:"), 0, 2)
        layout.addWidget(max_spinbox, 0, 3)
        
        layout.addWidget(QLabel("Critical Max:"), 0, 4)
        layout.addWidget(critical_spinbox, 0, 5)
        
        group.setLayout(layout)
        return group
    
    def update_threshold(self, param, key, value):
        """Update threshold value"""
        self.thresholds[param][key] = value
    
    def reset_defaults(self):
        """Reset to default thresholds"""
        self.thresholds = {
            'flowrate': {'min': 50, 'max': 500, 'critical_max': 600},
            'pressure': {'min': 100, 'max': 800, 'critical_max': 1000},
            'temperature': {'min': 50, 'max': 350, 'critical_max': 400}
        }
        
        # Update spinboxes
        for param_key, spinboxes in self.spinboxes.items():
            spinboxes['min'].setValue(self.thresholds[param_key]['min'])
            spinboxes['max'].setValue(self.thresholds[param_key]['max'])
            spinboxes['critical_max'].setValue(self.thresholds[param_key]['critical_max'])
    
    def load_settings(self):
        """Load settings from file"""
        settings_file = os.path.join(os.path.expanduser('~'), '.chemical_equipment_thresholds.json')
        if os.path.exists(settings_file):
            try:
                with open(settings_file, 'r') as f:
                    self.thresholds = json.load(f)
            except:
                pass
    
    def save_settings(self):
        """Save settings to file and emit signal"""
        settings_file = os.path.join(os.path.expanduser('~'), '.chemical_equipment_thresholds.json')
        try:
            with open(settings_file, 'w') as f:
                json.dump(self.thresholds, f)
        except:
            pass
        
        self.thresholdsChanged.emit(self.thresholds)
        self.accept()
    
    def get_thresholds(self):
        """Get current thresholds"""
        return self.thresholds

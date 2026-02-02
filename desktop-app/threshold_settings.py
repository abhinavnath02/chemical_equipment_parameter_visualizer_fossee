"""
Settings dialog for configuring safety thresholds with sliders and text inputs
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QSpinBox, QGroupBox, QGridLayout,
                              QFrame, QSlider, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
import json
import os


class SliderSpinBox(QWidget):
    """Combined slider and spinbox widget"""
    
    valueChanged = pyqtSignal(int)
    
    def __init__(self, label, value, min_val, max_val, color, parent=None):
        super().__init__(parent)
        self.color = color
        self.min_val = min_val
        self.max_val = max_val
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Top row: Label and SpinBox
        top_row = QHBoxLayout()
        
        lbl = QLabel(label)
        lbl.setStyleSheet("color: #a1a1aa; font-size: 12px;")
        top_row.addWidget(lbl)
        
        top_row.addStretch()
        
        self.spinbox = QSpinBox()
        self.spinbox.setRange(min_val, max_val)
        self.spinbox.setValue(value)
        self.spinbox.setFixedWidth(80)
        self.spinbox.setStyleSheet(f"""
            QSpinBox {{
                background-color: #09090b;
                border: 1px solid #3f3f46;
                border-radius: 4px;
                padding: 4px 8px;
                color: white;
                font-size: 12px;
            }}
            QSpinBox:focus {{
                border-color: {color};
            }}
            QSpinBox::up-button, QSpinBox::down-button {{
                background-color: #27272a;
                border: none;
                width: 16px;
            }}
            QSpinBox::up-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-bottom: 4px solid #a1a1aa;
            }}
            QSpinBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #a1a1aa;
            }}
        """)
        self.spinbox.valueChanged.connect(self._on_spinbox_changed)
        top_row.addWidget(self.spinbox)
        
        layout.addLayout(top_row)
        
        # Slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(value)
        self.slider.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 6px;
                background: #3f3f46;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: white;
                border: 2px solid #71717a;
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 9px;
            }}
            QSlider::handle:horizontal:hover {{
                border-color: {color};
            }}
            QSlider::sub-page:horizontal {{
                background: {color};
                border-radius: 3px;
            }}
        """)
        self.slider.valueChanged.connect(self._on_slider_changed)
        layout.addWidget(self.slider)
        
        self.setLayout(layout)
    
    def _on_slider_changed(self, value):
        self.spinbox.blockSignals(True)
        self.spinbox.setValue(value)
        self.spinbox.blockSignals(False)
        self.valueChanged.emit(value)
    
    def _on_spinbox_changed(self, value):
        self.slider.blockSignals(True)
        self.slider.setValue(value)
        self.slider.blockSignals(False)
        self.valueChanged.emit(value)
    
    def value(self):
        return self.spinbox.value()
    
    def setValue(self, value):
        self.spinbox.blockSignals(True)
        self.slider.blockSignals(True)
        self.spinbox.setValue(value)
        self.slider.setValue(value)
        self.spinbox.blockSignals(False)
        self.slider.blockSignals(False)


class ThresholdSettingsDialog(QDialog):
    """Dialog for configuring safety thresholds"""
    
    thresholdsChanged = pyqtSignal(dict)
    
    # Slider ranges for each parameter
    SLIDER_RANGES = {
        'flowrate': {'min': 0, 'max': 1000},
        'pressure': {'min': 0, 'max': 2000},
        'temperature': {'min': 0, 'max': 800}
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Safety Threshold Settings")
        self.setMinimumWidth(700)
        self.setMinimumHeight(600)
        
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
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title = QLabel("Safety Threshold Settings")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)
        
        subtitle = QLabel("Configure warning and critical limits for equipment parameters")
        subtitle.setStyleSheet("font-size: 13px; color: #a1a1aa;")
        layout.addWidget(subtitle)
        
        # Info banner
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(59, 130, 246, 0.1);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 8px;
                padding: 12px;
            }
        """)
        info_layout = QVBoxLayout()
        info_title = QLabel("ℹ How it works:")
        info_title.setStyleSheet("font-weight: bold; color: #60a5fa; font-size: 12px;")
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
        
        layout.addStretch()
        
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
        """Create a parameter group with slider inputs"""
        group = QFrame()
        group.setStyleSheet(f"""
            QFrame {{
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 8px;
                padding: 16px;
            }}
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)
        
        # Title with colored dot
        title_layout = QHBoxLayout()
        dot = QLabel("●")
        dot.setStyleSheet(f"color: {color}; font-size: 12px;")
        title_layout.addWidget(dot)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-weight: bold; font-size: 14px;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)
        
        # Sliders row
        sliders_layout = QHBoxLayout()
        sliders_layout.setSpacing(24)
        
        slider_range = self.SLIDER_RANGES[param_key]
        
        # Min slider
        min_slider = SliderSpinBox(
            "Minimum",
            self.thresholds[param_key]['min'],
            slider_range['min'],
            slider_range['max'],
            color
        )
        min_slider.valueChanged.connect(
            lambda v: self.update_threshold(param_key, 'min', v)
        )
        sliders_layout.addWidget(min_slider)
        
        # Max slider
        max_slider = SliderSpinBox(
            "Maximum",
            self.thresholds[param_key]['max'],
            slider_range['min'],
            slider_range['max'],
            color
        )
        max_slider.valueChanged.connect(
            lambda v: self.update_threshold(param_key, 'max', v)
        )
        sliders_layout.addWidget(max_slider)
        
        # Critical slider
        critical_slider = SliderSpinBox(
            "Critical Max",
            self.thresholds[param_key]['critical_max'],
            slider_range['min'],
            slider_range['max'],
            color
        )
        critical_slider.valueChanged.connect(
            lambda v: self.update_threshold(param_key, 'critical_max', v)
        )
        sliders_layout.addWidget(critical_slider)
        
        main_layout.addLayout(sliders_layout)
        
        # Store references
        if not hasattr(self, 'sliders'):
            self.sliders = {}
        self.sliders[param_key] = {
            'min': min_slider,
            'max': max_slider,
            'critical_max': critical_slider
        }
        
        group.setLayout(main_layout)
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
        
        # Update sliders
        for param_key, sliders in self.sliders.items():
            sliders['min'].setValue(self.thresholds[param_key]['min'])
            sliders['max'].setValue(self.thresholds[param_key]['max'])
            sliders['critical_max'].setValue(self.thresholds[param_key]['critical_max'])
    
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

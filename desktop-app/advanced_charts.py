"""
Additional analytical charts and safety visualization widgets
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
except ImportError:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import json
import os


class SafetyAlertsWidget(QWidget):
    """Widget displaying safety alerts with warning and critical indicators"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.thresholds = self.load_thresholds()
        self.init_ui()
    
    def load_thresholds(self):
        """Load thresholds from settings file"""
        default = {
            'flowrate': {'min': 50, 'max': 500, 'critical_max': 600},
            'pressure': {'min': 100, 'max': 800, 'critical_max': 1000},
            'temperature': {'min': 50, 'max': 350, 'critical_max': 400}
        }
        
        try:
            settings_file = os.path.join(os.path.expanduser('~'), '.chemical_equipment_thresholds.json')
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return default
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Title
        title = QLabel("Safety Status")
        title.setStyleSheet("font-size: 16px; font-weight: 600; color: #ffffff; margin-bottom: 8px;")
        layout.addWidget(title)
        
        # Scroll area for alerts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        
        self.alerts_container = QWidget()
        self.alerts_layout = QVBoxLayout()
        self.alerts_layout.setContentsMargins(0, 0, 0, 0)
        self.alerts_layout.setSpacing(8)
        self.alerts_container.setLayout(self.alerts_layout)
        
        scroll.setWidget(self.alerts_container)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
    
    def update_alerts(self, equipment_data):
        """Update alerts based on equipment data"""
        # Clear existing alerts
        while self.alerts_layout.count():
            child = self.alerts_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Reload thresholds in case they changed
        self.thresholds = self.load_thresholds()
        
        alerts = self.check_equipment(equipment_data)
        
        if not alerts:
            # Show all clear
            all_clear = QFrame()
            all_clear.setStyleSheet("""
                QFrame {
                    background-color: rgba(34, 197, 94, 0.1);
                    border: 1px solid rgba(34, 197, 94, 0.3);
                    border-radius: 8px;
                    padding: 16px;
                }
            """)
            layout = QVBoxLayout()
            
            icon_label = QLabel("✓")
            icon_label.setStyleSheet("font-size: 24px; color: #22c55e; font-weight: bold;")
            icon_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(icon_label)
            
            msg = QLabel("All Systems Normal")
            msg.setStyleSheet("font-size: 14px; color: #22c55e; font-weight: 600;")
            msg.setAlignment(Qt.AlignCenter)
            layout.addWidget(msg)
            
            desc = QLabel("All equipment operating within safe parameters")
            desc.setStyleSheet("font-size: 12px; color: #86efac;")
            desc.setAlignment(Qt.AlignCenter)
            layout.addWidget(desc)
            
            all_clear.setLayout(layout)
            self.alerts_layout.addWidget(all_clear)
        else:
            # Count critical and warnings
            critical_count = sum(1 for a in alerts if a['level'] == 'critical')
            warning_count = sum(1 for a in alerts if a['level'] == 'warning')
            
            # Summary banner
            summary = QFrame()
            if critical_count > 0:
                summary.setStyleSheet("""
                    QFrame {
                        background-color: rgba(239, 68, 68, 0.1);
                        border: 1px solid rgba(239, 68, 68, 0.3);
                        border-radius: 8px;
                        padding: 12px;
                    }
                """)
                color = "#ef4444"
                text_color = "#fca5a5"
            else:
                summary.setStyleSheet("""
                    QFrame {
                        background-color: rgba(245, 158, 11, 0.1);
                        border: 1px solid rgba(245, 158, 11, 0.3);
                        border-radius: 8px;
                        padding: 12px;
                    }
                """)
                color = "#f59e0b"
                text_color = "#fcd34d"
            
            layout = QVBoxLayout()
            
            title = QLabel("⚠ Safety Alerts Detected")
            title.setStyleSheet(f"font-size: 14px; color: {color}; font-weight: 600;")
            layout.addWidget(title)
            
            summary_text = ""
            if critical_count > 0:
                summary_text += f"{critical_count} Critical Alert{'s' if critical_count > 1 else ''}"
            if critical_count > 0 and warning_count > 0:
                summary_text += " • "
            if warning_count > 0:
                summary_text += f"{warning_count} Warning{'s' if warning_count > 1 else ''}"
            summary_text += " — Immediate attention required"
            
            desc = QLabel(summary_text)
            desc.setStyleSheet(f"font-size: 11px; color: {text_color};")
            layout.addWidget(desc)
            
            summary.setLayout(layout)
            self.alerts_layout.addWidget(summary)
            
            # Individual alerts
            for alert in alerts:
                alert_frame = self.create_alert_frame(alert)
                self.alerts_layout.addWidget(alert_frame)
        
        self.alerts_layout.addStretch()
    
    def create_alert_frame(self, alert):
        """Create individual alert frame"""
        frame = QFrame()
        
        if alert['level'] == 'critical':
            frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(239, 68, 68, 0.05);
                    border-left: 3px solid #ef4444;
                    border-radius: 4px;
                    padding: 12px;
                }
            """)
            dot_color = "#ef4444"
            text_color = "#fca5a5"
        else:
            frame.setStyleSheet("""
                QFrame {
                    background-color: rgba(245, 158, 11, 0.05);
                    border-left: 3px solid #f59e0b;
                    border-radius: 4px;
                    padding: 12px;
                }
            """)
            dot_color = "#f59e0b"
            text_color = "#fcd34d"
        
        layout = QVBoxLayout()
        layout.setSpacing(4)
        
        # Equipment name
        name_label = QLabel(f"{alert['equipment']} ({alert['type']})")
        name_label.setStyleSheet("font-size: 12px; color: #ffffff; font-weight: 600;")
        layout.addWidget(name_label)
        
        # Messages
        for msg in alert['messages']:
            msg_label = QLabel(msg)
            msg_label.setStyleSheet(f"font-size: 11px; color: {text_color};")
            msg_label.setWordWrap(True)
            layout.addWidget(msg_label)
        
        frame.setLayout(layout)
        return frame
    
    def check_equipment(self, equipment_data):
        """Check equipment for safety violations"""
        alerts = []
        
        for eq in equipment_data:
            messages = []
            level = 'warning'
            
            # Check flowrate
            if eq['flowrate'] > self.thresholds['flowrate']['critical_max']:
                messages.append(f"🔴 CRITICAL: Flowrate {eq['flowrate']:.1f} exceeds critical limit {self.thresholds['flowrate']['critical_max']}")
                level = 'critical'
            elif eq['flowrate'] > self.thresholds['flowrate']['max']:
                messages.append(f"⚠ Flowrate {eq['flowrate']:.1f} exceeds safe maximum {self.thresholds['flowrate']['max']}")
            elif eq['flowrate'] < self.thresholds['flowrate']['min']:
                messages.append(f"⚠ Flowrate {eq['flowrate']:.1f} below safe minimum {self.thresholds['flowrate']['min']}")
            
            # Check pressure
            if eq['pressure'] > self.thresholds['pressure']['critical_max']:
                messages.append(f"🔴 CRITICAL: Pressure {eq['pressure']:.1f} exceeds critical limit {self.thresholds['pressure']['critical_max']}")
                level = 'critical'
            elif eq['pressure'] > self.thresholds['pressure']['max']:
                messages.append(f"⚠ Pressure {eq['pressure']:.1f} exceeds safe maximum {self.thresholds['pressure']['max']}")
            elif eq['pressure'] < self.thresholds['pressure']['min']:
                messages.append(f"⚠ Pressure {eq['pressure']:.1f} below safe minimum {self.thresholds['pressure']['min']}")
            
            # Check temperature
            if eq['temperature'] > self.thresholds['temperature']['critical_max']:
                messages.append(f"🔴 CRITICAL: Temperature {eq['temperature']:.1f} exceeds critical limit {self.thresholds['temperature']['critical_max']}")
                level = 'critical'
            elif eq['temperature'] > self.thresholds['temperature']['max']:
                messages.append(f"⚠ Temperature {eq['temperature']:.1f} exceeds safe maximum {self.thresholds['temperature']['max']}")
            elif eq['temperature'] < self.thresholds['temperature']['min']:
                messages.append(f"⚠ Temperature {eq['temperature']:.1f} below safe minimum {self.thresholds['temperature']['min']}")
            
            if messages:
                alerts.append({
                    'equipment': eq['name'],
                    'type': eq['type'],
                    'level': level,
                    'messages': messages
                })
        
        return alerts


class SafetyStatusChart(FigureCanvasQTAgg):
    """Stacked bar chart showing safety status distribution"""
    
    def __init__(self, parent=None, width=6, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#000000')
        super().__init__(self.fig)
        self.setParent(parent)
        self.thresholds = self.load_thresholds()
    
    def load_thresholds(self):
        """Load thresholds from settings file"""
        default = {
            'flowrate': {'min': 50, 'max': 500, 'critical_max': 600},
            'pressure': {'min': 100, 'max': 800, 'critical_max': 1000},
            'temperature': {'min': 50, 'max': 350, 'critical_max': 400}
        }
        
        try:
            settings_file = os.path.join(os.path.expanduser('~'), '.chemical_equipment_thresholds.json')
            if os.path.exists(settings_file):
                with open(settings_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return default
    
    def update_chart(self, equipment_data):
        """Update chart with equipment data"""
        self.fig.clear()
        self.thresholds = self.load_thresholds()
        
        def categorize_values(values, param):
            safe = sum(1 for v in values if self.thresholds[param]['min'] <= v <= self.thresholds[param]['max'])
            warning = sum(1 for v in values if (v > self.thresholds[param]['max'] and v <= self.thresholds[param]['critical_max']) or v < self.thresholds[param]['min'])
            critical = sum(1 for v in values if v > self.thresholds[param]['critical_max'])
            return safe, warning, critical
        
        flowrates = [e['flowrate'] for e in equipment_data]
        pressures = [e['pressure'] for e in equipment_data]
        temperatures = [e['temperature'] for e in equipment_data]
        
        flow_safe, flow_warn, flow_crit = categorize_values(flowrates, 'flowrate')
        press_safe, press_warn, press_crit = categorize_values(pressures, 'pressure')
        temp_safe, temp_warn, temp_crit = categorize_values(temperatures, 'temperature')
        
        categories = ['Flowrate', 'Pressure', 'Temperature']
        safe_counts = [flow_safe, press_safe, temp_safe]
        warning_counts = [flow_warn, press_warn, temp_warn]
        critical_counts = [flow_crit, press_crit, temp_crit]
        
        ax = self.fig.add_subplot(111)
        x = np.arange(len(categories))
        width = 0.6
        
        p1 = ax.bar(x, safe_counts, width, label='Safe', color='#22c55e', edgecolor='#16a34a', linewidth=2)
        p2 = ax.bar(x, warning_counts, width, bottom=safe_counts, label='Warning', color='#f59e0b', edgecolor='#d97706', linewidth=2)
        
        bottom_crit = [safe_counts[i] + warning_counts[i] for i in range(len(categories))]
        p3 = ax.bar(x, critical_counts, width, bottom=bottom_crit, label='Critical', color='#ef4444', edgecolor='#dc2626', linewidth=2)
        
        ax.set_ylabel('Equipment Count', color='#d1d5db', fontsize=10)
        ax.set_title('Equipment Safety Status Distribution', color='#ffffff', fontsize=12, fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, color='#d1d5db', fontsize=10)
        ax.tick_params(axis='y', labelcolor='#d1d5db', labelsize=9)
        ax.set_facecolor('#000000')
        ax.legend(loc='upper right', fontsize=9, facecolor='#18181b', edgecolor='#3f3f46', labelcolor='#d1d5db')
        ax.grid(axis='y', alpha=0.2, color='#3f3f46')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#3f3f46')
        ax.spines['left'].set_color('#3f3f46')
        
        self.fig.tight_layout()
        self.draw()


class ParameterDistributionChart(FigureCanvasQTAgg):
    """Histogram showing parameter distribution"""
    
    def __init__(self, parent=None, width=4, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#000000')
        super().__init__(self.fig)
        self.setParent(parent)
    
    def update_chart(self, equipment_data, parameter):
        """Update chart with equipment data for specific parameter"""
        self.fig.clear()
        
        values = [e[parameter] for e in equipment_data]
        
        colors = {
            'flowrate': ('#ef4444', '#ef444480'),
            'pressure': ('#3b82f6', '#3b82f680'),
            'temperature': ('#22c55e', '#22c55e80')
        }
        
        titles = {
            'flowrate': 'Flowrate Distribution',
            'pressure': 'Pressure Distribution',
            'temperature': 'Temperature Distribution'
        }
        
        ax = self.fig.add_subplot(111)
        
        # Create histogram
        ax.hist(values, bins=10, color=colors[parameter][1], edgecolor=colors[parameter][0], linewidth=1.5)
        
        ax.set_xlabel(parameter.capitalize(), color='#d1d5db', fontsize=9)
        ax.set_ylabel('Count', color='#d1d5db', fontsize=9)
        ax.set_title(titles[parameter], color='#ffffff', fontsize=11, fontweight='bold', pad=10)
        ax.tick_params(axis='both', labelcolor='#d1d5db', labelsize=8)
        ax.set_facecolor('#000000')
        ax.grid(axis='y', alpha=0.2, color='#3f3f46')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('#3f3f46')
        ax.spines['left'].set_color('#3f3f46')
        
        self.fig.tight_layout()
        self.draw()

"""
Main dashboard window with file upload, charts, and data table
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QFileDialog, QTableWidget,
                              QTableWidgetItem, QFrame, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
except ImportError:
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from api_client import APIClient
from datetime import datetime
import os


class MplCanvas(FigureCanvasQTAgg):
    """Matplotlib canvas for embedding charts"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='#000000')
        super().__init__(self.fig)
        self.setParent(parent)


class DashboardWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.current_result = None
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Main content area
        main_content = self.create_main_content()
        main_layout.addWidget(main_content)
        central_widget.setLayout(main_layout)
    
    def create_main_content(self):
        """Create main content area"""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Scrollable content
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(24, 24, 24, 24)
        self.content_layout.setSpacing(24)
        
        # Upload section
        upload_section = self.create_upload_section()
        self.content_layout.addWidget(upload_section)
        
        # Summary stats (hidden initially)
        self.summary_frame = self.create_summary_stats()
        self.summary_frame.hide()
        self.content_layout.addWidget(self.summary_frame)
        
        # Charts section (hidden initially)
        self.charts_frame = self.create_charts_section()
        self.charts_frame.hide()
        self.content_layout.addWidget(self.charts_frame)
        
        # Data table (hidden initially)
        self.table_frame = self.create_data_table()
        self.table_frame.hide()
        self.content_layout.addWidget(self.table_frame)
        
        self.content_layout.addStretch()
        
        scroll_content.setLayout(self.content_layout)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        widget.setLayout(layout)
        return widget
    
    def create_header(self):
        """Create header with title and user info"""
        header = QFrame()
        header.setStyleSheet("background-color: #000000; border-bottom: 1px solid #27272a;")
        header.setFixedHeight(80)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(24, 16, 24, 16)
        
        # Title section
        title_layout = QVBoxLayout()
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setProperty("heading", True)
        subtitle = QLabel("Analyze and visualize equipment data")
        subtitle.setProperty("subheading", True)
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        layout.addLayout(title_layout)
        
        layout.addStretch()
        
        # User info
        if self.api_client.user:
            user_layout = QVBoxLayout()
            user_layout.setAlignment(Qt.AlignRight)
            username = QLabel(self.api_client.user.get('username', ''))
            username.setStyleSheet("font-size: 13px; color: #ffffff;")
            email = QLabel(self.api_client.user.get('email', ''))
            email.setProperty("subheading", True)
            user_layout.addWidget(username)
            user_layout.addWidget(email)
            layout.addLayout(user_layout)
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.setProperty("secondary", True)
        logout_btn.setFixedWidth(100)
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)
        
        header.setLayout(layout)
        return header
    
    def create_upload_section(self):
        """Create file upload section"""
        frame = QFrame()
        frame.setProperty("card", True)
        layout = QVBoxLayout()
        
        title = QLabel("Upload CSV File")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        # File selection
        file_layout = QHBoxLayout()
        self.file_label = QLabel("No file selected")
        self.file_label.setProperty("subheading", True)
        file_layout.addWidget(self.file_label)
        file_layout.addStretch()
        
        select_btn = QPushButton("Choose File")
        select_btn.setProperty("secondary", True)
        select_btn.clicked.connect(self.select_file)
        file_layout.addWidget(select_btn)
        layout.addLayout(file_layout)
        
        # Upload button
        self.upload_btn = QPushButton("Upload and Analyze")
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_btn)
        
        # Error message
        self.error_label = QLabel("")
        self.error_label.setProperty("error", True)
        self.error_label.hide()
        layout.addWidget(self.error_label)
        
        frame.setLayout(layout)
        return frame
    
    def create_summary_stats(self):
        """Create summary statistics section"""
        frame = QFrame()
        frame.setProperty("card", True)
        layout = QVBoxLayout()
        
        # Header with PDF button
        header_layout = QHBoxLayout()
        title = QLabel("Summary Statistics")
        title.setStyleSheet("font-size: 14px; font-weight: 600;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        self.pdf_btn = QPushButton("Download PDF")
        self.pdf_btn.clicked.connect(self.generate_pdf)
        header_layout.addWidget(self.pdf_btn)
        layout.addLayout(header_layout)
        
        # Stats grid
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)
        
        self.stat_equipment = self.create_stat_card("Equipment", "0")
        self.stat_flowrate = self.create_stat_card("Flowrate", "0.0")
        self.stat_pressure = self.create_stat_card("Pressure", "0.0")
        self.stat_temperature = self.create_stat_card("Temperature", "0.0")
        
        stats_layout.addWidget(self.stat_equipment)
        stats_layout.addWidget(self.stat_flowrate)
        stats_layout.addWidget(self.stat_pressure)
        stats_layout.addWidget(self.stat_temperature)
        
        layout.addLayout(stats_layout)
        frame.setLayout(layout)
        return frame
    
    def create_stat_card(self, label: str, value: str):
        """Create individual stat card"""
        card = QFrame()
        card.setProperty("stats", True)
        layout = QVBoxLayout()
        
        label_widget = QLabel(label)
        label_widget.setProperty("subheading", True)
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet("font-size: 20px; font-weight: bold; color: #ffffff;")
        value_widget.setObjectName(f"value_{label.lower()}")
        
        layout.addWidget(label_widget)
        layout.addWidget(value_widget)
        card.setLayout(layout)
        return card
    
    def create_charts_section(self):
        """Create charts section"""
        frame = QFrame()
        frame.setProperty("card", True)
        layout = QVBoxLayout()
        layout.setSpacing(16)
        
        # Charts grid
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(16)
        
        # Bar chart
        self.bar_canvas = MplCanvas(self, width=5, height=3.5, dpi=80)
        self.bar_canvas.setMinimumSize(400, 300)
        charts_layout.addWidget(self.bar_canvas)
        
        # Doughnut chart
        self.doughnut_canvas = MplCanvas(self, width=5, height=3.5, dpi=80)
        self.doughnut_canvas.setMinimumSize(400, 300)
        charts_layout.addWidget(self.doughnut_canvas)
        
        layout.addLayout(charts_layout)
        
        # Line chart
        self.line_canvas = MplCanvas(self, width=10, height=3.5, dpi=80)
        self.line_canvas.setMinimumSize(800, 300)
        layout.addWidget(self.line_canvas)
        
        frame.setLayout(layout)
        return frame
    
    def create_data_table(self):
        """Create data table section"""
        frame = QFrame()
        frame.setProperty("card", True)
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        title = QLabel("Equipment Data")
        title.setStyleSheet("font-size: 16px; font-weight: 600; color: #ffffff;")
        layout.addWidget(title)
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(5)
        self.data_table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        
        # Set column widths to auto-resize
        header = self.data_table.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(1, header.ResizeToContents)
        header.setSectionResizeMode(2, header.ResizeToContents)
        header.setSectionResizeMode(3, header.ResizeToContents)
        header.setSectionResizeMode(4, header.ResizeToContents)
        
        self.data_table.verticalHeader().setVisible(False)
        self.data_table.setMinimumHeight(300)
        self.data_table.setMaximumHeight(500)
        self.data_table.setAlternatingRowColors(True)
        self.data_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.data_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.data_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        layout.addWidget(self.data_table)
        
        frame.setLayout(layout)
        return frame
    
    def select_file(self):
        """Open file dialog to select CSV"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.upload_btn.setEnabled(True)
            self.error_label.hide()
    
    def upload_file(self):
        """Upload selected file"""
        if not hasattr(self, 'selected_file'):
            return
        
        self.upload_btn.setEnabled(False)
        self.upload_btn.setText("Uploading...")
        
        success, result, message = self.api_client.upload_csv(self.selected_file)
        
        self.upload_btn.setEnabled(True)
        self.upload_btn.setText("Upload and Analyze")
        
        if success:
            self.current_result = result
            self.display_results(result)
            self.error_label.hide()
        else:
            self.error_label.setText(message)
            self.error_label.show()
    
    def display_results(self, result):
        """Display analysis results"""
        # Update summary stats
        self.stat_equipment.findChild(QLabel, "value_equipment").setText(
            str(result.get('total_equipment', 0))
        )
        self.stat_flowrate.findChild(QLabel, "value_flowrate").setText(
            f"{result.get('avg_flowrate', 0):.1f}"
        )
        self.stat_pressure.findChild(QLabel, "value_pressure").setText(
            f"{result.get('avg_pressure', 0):.1f}"
        )
        self.stat_temperature.findChild(QLabel, "value_temperature").setText(
            f"{result.get('avg_temperature', 0):.1f}"
        )
        
        self.summary_frame.show()
        
        # Update charts
        self.plot_bar_chart(result)
        self.plot_doughnut_chart(result)
        self.plot_line_chart(result)
        self.charts_frame.show()
        
        # Update table
        self.populate_table(result.get('equipment_data', []))
        self.table_frame.show()
    
    def plot_bar_chart(self, result):
        """Plot parameter bar chart"""
        self.bar_canvas.fig.clear()
        ax = self.bar_canvas.fig.add_subplot(111, facecolor='#000000')
        
        categories = ['Flowrate', 'Pressure', 'Temperature']
        values = [
            result.get('avg_flowrate', 0),
            result.get('avg_pressure', 0),
            result.get('avg_temperature', 0)
        ]
        
        bars = ax.bar(categories, values, color=['#ef4444', '#3b82f6', '#22c55e'], width=0.6)
        
        ax.set_facecolor('#000000')
        ax.set_title('Average Parameters', color='#ffffff', fontsize=12, pad=15)
        ax.tick_params(colors='#a1a1aa', labelsize=9)
        ax.spines['bottom'].set_color('#3f3f46')
        ax.spines['left'].set_color('#3f3f46')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.1, color='#3f3f46', axis='y')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', color='#ffffff', fontsize=9)
        
        self.bar_canvas.fig.tight_layout()
        self.bar_canvas.draw()
    
    def plot_doughnut_chart(self, result):
        """Plot equipment type distribution"""
        self.doughnut_canvas.fig.clear()
        ax = self.doughnut_canvas.fig.add_subplot(111, facecolor='#000000')
        
        equipment_by_type = result.get('equipment_by_type', {})
        if equipment_by_type:
            labels = list(equipment_by_type.keys())
            sizes = list(equipment_by_type.values())
            colors = ['#ef4444', '#3b82f6', '#22c55e', '#f59e0b', '#8b5cf6']
            
            pie_result = ax.pie(
                sizes,
                labels=None,  # Remove labels from pie
                autopct='%1.1f%%',
                colors=colors[:len(labels)],
                startangle=90,
                pctdistance=0.85,
                wedgeprops={'edgecolor': '#000000', 'linewidth': 1.5}
            )
            
            # Handle different return types from pie()
            if len(pie_result) == 3:
                wedges, texts, autotexts = pie_result
                for autotext in autotexts:
                    autotext.set_color('#ffffff')
                    autotext.set_fontsize(9)
                    autotext.set_fontweight('bold')
            else:
                wedges, texts = pie_result
            
            # Add legend
            ax.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1),
                     facecolor='#18181b', edgecolor='#3f3f46', labelcolor='#ffffff',
                     fontsize=9, framealpha=1)
            
            ax.set_title('Equipment Distribution', color='#ffffff', fontsize=12, pad=15)
        
        self.doughnut_canvas.fig.tight_layout()
        self.doughnut_canvas.draw()
    
    def plot_line_chart(self, result):
        """Plot equipment parameters line chart"""
        self.line_canvas.fig.clear()
        ax = self.line_canvas.fig.add_subplot(111, facecolor='#000000')
        
        equipment_data = result.get('equipment_data', [])
        if equipment_data:
            # Limit to first 15 items for readability
            equipment_data = equipment_data[:15]
            names = [item['name'][:20] for item in equipment_data]
            flowrates = [item['flowrate'] for item in equipment_data]
            pressures = [item['pressure'] for item in equipment_data]
            temperatures = [item['temperature'] for item in equipment_data]
            
            x = range(len(names))
            ax.plot(x, flowrates, marker='o', color='#ef4444', label='Flowrate', linewidth=2, markersize=5)
            ax.plot(x, pressures, marker='s', color='#3b82f6', label='Pressure', linewidth=2, markersize=5)
            ax.plot(x, temperatures, marker='^', color='#22c55e', label='Temperature', linewidth=2, markersize=5)
            
            ax.set_xticks(x)
            ax.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
            ax.set_facecolor('#000000')
            ax.set_title('Equipment Parameters', color='#ffffff', fontsize=12, pad=15)
            ax.legend(loc='upper right', facecolor='#18181b', edgecolor='#3f3f46', 
                     labelcolor='#ffffff', fontsize=9, framealpha=1)
            ax.tick_params(colors='#a1a1aa', labelsize=9)
            ax.spines['bottom'].set_color('#3f3f46')
            ax.spines['left'].set_color('#3f3f46')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.1, color='#3f3f46', axis='y')
        
        self.line_canvas.fig.tight_layout()
        self.line_canvas.draw()
    
    def populate_table(self, data):
        """Populate data table"""
        self.data_table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            # Create items with explicit styling
            name_item = QTableWidgetItem(item['name'])
            type_item = QTableWidgetItem(item['type'])
            flowrate_item = QTableWidgetItem(str(item['flowrate']))
            pressure_item = QTableWidgetItem(str(item['pressure']))
            temperature_item = QTableWidgetItem(str(item['temperature']))
            
            # Center align numeric values
            flowrate_item.setTextAlignment(Qt.AlignCenter)
            pressure_item.setTextAlignment(Qt.AlignCenter)
            temperature_item.setTextAlignment(Qt.AlignCenter)
            
            self.data_table.setItem(row, 0, name_item)
            self.data_table.setItem(row, 1, type_item)
            self.data_table.setItem(row, 2, flowrate_item)
            self.data_table.setItem(row, 3, pressure_item)
            self.data_table.setItem(row, 4, temperature_item)
    
    def generate_pdf(self):
        """Generate and download PDF report"""
        if not self.current_result:
            return
        
        success, pdf_data, message = self.api_client.generate_pdf(self.current_result)
        
        if success:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save PDF Report",
                f"equipment_report_{self.current_result.get('total_equipment', '')}_items.pdf",
                "PDF Files (*.pdf)"
            )
            
            if file_path:
                if pdf_data:
                    with open(file_path, 'wb') as f:
                        f.write(pdf_data)
                    
                    QMessageBox.information(self, "Success", "PDF report saved successfully!")
                else:
                    QMessageBox.warning(self, "Error", "Failed to save PDF: No data received")
        else:
            QMessageBox.warning(self, "Error", f"Failed to generate PDF: {message}")
    
    def handle_logout(self):
        """Handle logout"""
        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.api_client.logout()
            self.close()

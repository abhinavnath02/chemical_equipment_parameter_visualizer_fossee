from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QWidget, QGridLayout
from PyQt5.QtCore import Qt

class SmartInsightsWidget(QFrame):
    """Widget to display automated insights (Correlations & Outliers)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("card", True)
        self.init_ui()
        
    def init_ui(self):
        layout = QGridLayout()
        layout.setSpacing(20)
        
        # Method 1: Correlations Section
        self.corr_frame = QFrame()
        self.corr_frame.setStyleSheet("""
            QFrame {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 8px;
            }
        """)
        corr_layout = QVBoxLayout()
        
        # Header
        corr_header = QHBoxLayout()
        icon = QLabel("🔗") 
        icon.setStyleSheet("font-size: 18px;")
        
        title_box = QVBoxLayout()
        title = QLabel("Parameter Correlations")
        title.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        subtitle = QLabel("Relationships between variables")
        subtitle.setStyleSheet("color: #a1a1aa; font-size: 11px;")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        
        corr_header.addWidget(icon)
        corr_header.addLayout(title_box)
        corr_header.addStretch()
        corr_layout.addLayout(corr_header)
        
        # Content Area
        self.corr_content = QVBoxLayout()
        self.corr_content.setSpacing(8)
        self.corr_placeholder = QLabel("No significant correlations found.")
        self.corr_placeholder.setStyleSheet("color: #71717a; padding: 20px;")
        self.corr_placeholder.setAlignment(Qt.AlignCenter)
        self.corr_content.addWidget(self.corr_placeholder)
        
        corr_layout.addLayout(self.corr_content)
        corr_layout.addStretch()
        self.corr_frame.setLayout(corr_layout)
        
        # Method 2: Outliers Section
        self.outlier_frame = QFrame()
        self.outlier_frame.setStyleSheet("""
            QFrame {
                background-color: #18181b;
                border: 1px solid #27272a;
                border-radius: 8px;
            }
        """)
        outlier_layout = QVBoxLayout()
        
        # Header
        outlier_header = QHBoxLayout()
        icon2 = QLabel("⚡")
        icon2.setStyleSheet("font-size: 18px;")
        
        title_box2 = QVBoxLayout()
        title2 = QLabel("Statistical Deviations")
        title2.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        subtitle2 = QLabel("Z-Score anomalies (> 2σ)")
        subtitle2.setStyleSheet("color: #a1a1aa; font-size: 11px;")
        title_box2.addWidget(title2)
        title_box2.addWidget(subtitle2)
        
        outlier_header.addWidget(icon2)
        outlier_header.addLayout(title_box2)
        outlier_header.addStretch()
        outlier_layout.addLayout(outlier_header)
        
        # Content Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setMaximumHeight(200)
        
        self.outlier_container = QWidget()
        self.outlier_container.setStyleSheet("background: transparent;")
        self.outlier_content = QVBoxLayout()
        self.outlier_content.setSpacing(8)
        self.outlier_content.setContentsMargins(0,0,0,0)
        
        self.outlier_placeholder = QLabel("No statistical anomalies detected.")
        self.outlier_placeholder.setStyleSheet("color: #71717a; padding: 20px;")
        self.outlier_placeholder.setAlignment(Qt.AlignCenter)
        self.outlier_content.addWidget(self.outlier_placeholder)
        
        self.outlier_container.setLayout(self.outlier_content)
        scroll.setWidget(self.outlier_container)
        
        outlier_layout.addWidget(scroll)
        self.outlier_frame.setLayout(outlier_layout)
        
        # Add to main grid
        layout.addWidget(self.corr_frame, 0, 0)
        layout.addWidget(self.outlier_frame, 0, 1)
        
        self.setLayout(layout)
        
    def update_insights(self, insights):
        """Update the widget with new data"""
        if not insights:
            self.hide()
            return
            
        self.show()
        
        # 1. Update Correlations
        # Clear previous (but don't delete, just remove from layout)
        while self.corr_content.count():
            item = self.corr_content.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
                
        correlations = insights.get('correlations', [])
        if correlations:
            for corr in correlations:
                row = QFrame()
                row.setStyleSheet("background-color: #27272a; border-radius: 4px; padding: 4px;")
                row_layout = QHBoxLayout()
                row_layout.setContentsMargins(8, 4, 8, 4)
                
                name_label = QLabel(corr['pair'])
                name_label.setStyleSheet("color: #e4e4e7; font-weight: 500;")
                
                val_label = QLabel(f"{abs(corr['value']):.2f}")
                color = "#4ade80" if corr['value'] > 0 else "#f87171"
                bg_color = "rgba(74, 222, 128, 0.1)" if corr['value'] > 0 else "rgba(248, 113, 113, 0.1)"
                val_label.setStyleSheet(f"color: {color}; background-color: {bg_color}; padding: 2px 6px; border-radius: 4px; font-weight: bold;")
                
                interp_label = QLabel(f"{corr['interpretation']} Correlation")
                interp_label.setStyleSheet("color: #71717a; font-size: 10px;")
                
                left_box = QVBoxLayout()
                left_box.setSpacing(2)
                left_box.addWidget(name_label)
                left_box.addWidget(interp_label)
                
                row_layout.addLayout(left_box)
                row_layout.addStretch()
                row_layout.addWidget(val_label)
                
                row.setLayout(row_layout)
                self.corr_content.addWidget(row)
        else:
            # Create a new placeholder each time
            placeholder = QLabel("No significant correlations found.")
            placeholder.setStyleSheet("color: #71717a; padding: 20px;")
            placeholder.setAlignment(Qt.AlignCenter)
            self.corr_content.addWidget(placeholder)

        # 2. Update Outliers
        # Clear previous
        while self.outlier_content.count():
            item = self.outlier_content.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()
                
        outliers = insights.get('outliers', [])
        if outliers:
            for item in outliers:
                row = QFrame()
                row.setStyleSheet("background-color: #27272a; border-radius: 4px; padding: 4px;")
                row_layout = QHBoxLayout()
                row_layout.setContentsMargins(8, 8, 8, 8)
                
                # Deviation Badge
                dev_label = QLabel(str(item['deviation']))
                dev_label.setStyleSheet("color: #fb923c; font-family: monospace; font-weight: bold;")
                
                # Info
                info_box = QVBoxLayout()
                info_box.setSpacing(2)
                
                top_line = QHBoxLayout()
                eq_name = QLabel(item['equipment'])
                eq_name.setStyleSheet("color: #e4e4e7; font-weight: 500;")
                val_display = QLabel(f"{item['value']:.1f}")
                val_display.setStyleSheet("color: white; font-weight: bold;")
                
                top_line.addWidget(eq_name)
                top_line.addStretch()
                top_line.addWidget(val_display)
                
                btm_line = QHBoxLayout()
                param_name = QLabel(item['parameter'].upper())
                param_name.setStyleSheet("color: #71717a; font-size: 10px; font-weight: bold;")
                avg_display = QLabel(f"Avg: {item['mean']}")
                avg_display.setStyleSheet("color: #a1a1aa; font-size: 10px;")
                
                btm_line.addWidget(param_name)
                btm_line.addStretch()
                btm_line.addWidget(avg_display)
                
                info_box.addLayout(top_line)
                info_box.addLayout(btm_line)
                
                row_layout.addWidget(dev_label)
                row_layout.addSpacing(10)
                row_layout.addLayout(info_box)
                
                row.setLayout(row_layout)
                self.outlier_content.addWidget(row)
        else:
            # Create a new placeholder each time
            placeholder = QLabel("No statistical anomalies detected.")
            placeholder.setStyleSheet("color: #71717a; padding: 20px;")
            placeholder.setAlignment(Qt.AlignCenter)
            self.outlier_content.addWidget(placeholder)

"""
Shared stylesheet for consistent dark theme across the application
Matches the web app's black/zinc/white color scheme
"""

DARK_STYLESHEET = """
QMainWindow, QDialog {
    background-color: #000000;
    color: #ffffff;
}

QWidget {
    background-color: transparent;
    color: #ffffff;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

QMainWindow, QDialog {
    background-color: #000000;
}

/* Labels - transparent background */
QLabel {
    background-color: transparent;
    color: #ffffff;
}

/* Headers */
QLabel[heading="true"] {
    font-size: 20px;
    font-weight: bold;
    color: #ffffff;
    background-color: transparent;
}

QLabel[subheading="true"] {
    font-size: 11px;
    color: #a1a1aa;
    background-color: transparent;
}

/* Input Fields */
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 8px 12px;
    color: #ffffff;
    selection-background-color: #ffffff;
    selection-color: #000000;
}

QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2px solid #ffffff;
    outline: none;
}

QLineEdit::placeholder {
    color: #71717a;
}

/* Error Labels */
QLabel[error="true"] {
    color: #ef4444;
    font-size: 11px;
    padding: 4px 0;
    background-color: transparent;
}

/* Buttons */
QPushButton {
    background-color: #ffffff;
    color: #000000;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background-color: #e5e5e5;
}

QPushButton:pressed {
    background-color: #d4d4d4;
}

QPushButton:disabled {
    background-color: #27272a;
    color: #71717a;
}

QPushButton[secondary="true"] {
    background-color: #27272a;
    color: #ffffff;
    border: 1px solid #3f3f46;
}

QPushButton[secondary="true"]:hover {
    background-color: #3f3f46;
}

/* Tables */
QTableWidget {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 12px;
    gridline-color: #27272a;
    color: #ffffff;
}

QTableWidget::item {
    padding: 8px;
    border: none;
    color: #ffffff;
}

QTableWidget::item:selected {
    background-color: #27272a;
    color: #ffffff;
}

QTableWidget::item:alternate {
    background-color: #27272a;
}

QHeaderView::section {
    background-color: #27272a;
    color: #ffffff;
    padding: 12px;
    border: none;
    border-bottom: 1px solid #3f3f46;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
}

/* Scrollbars */
QScrollBar:vertical {
    background-color: #000000;
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background-color: #27272a;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background-color: #3f3f46;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QScrollBar:horizontal {
    background-color: #000000;
    height: 8px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background-color: #27272a;
    border-radius: 4px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #3f3f46;
}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
}

/* Cards/Panels */
QFrame[card="true"] {
    background-color: #18181b;
    border: 1px solid #27272a;
    border-radius: 12px;
    padding: 16px;
}

QFrame[card="true"] QLabel {
    background-color: transparent;
}

QFrame[stats="true"] {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 12px;
}

QFrame[stats="true"] QLabel {
    background-color: transparent;
}

/* Status/Error Messages */
QLabel[success="true"] {
    background-color: rgba(34, 197, 94, 0.1);
    color: #22c55e;
    border: 1px solid #22c55e;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 13px;
}

/* List Widget */
QListWidget {
    background-color: transparent;
    border: none;
    color: #ffffff;
    outline: none;
}

QListWidget::item {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    padding: 8px;
    margin-bottom: 8px;
    color: #ffffff;
    min-height: 60px;
}

QListWidget::item:hover {
    background-color: #3f3f46;
    border-color: #52525b;
}

QListWidget::item:selected {
    background-color: #3f3f46;
    border-color: #ffffff;
}

/* Progress Bar */
QProgressBar {
    background-color: #27272a;
    border: 1px solid #3f3f46;
    border-radius: 8px;
    text-align: center;
    color: #ffffff;
}

QProgressBar::chunk {
    background-color: #ffffff;
    border-radius: 7px;
}

/* Menu Bar */
QMenuBar {
    background-color: #000000;
    border-bottom: 1px solid #27272a;
    color: #ffffff;
}

QMenuBar::item:selected {
    background-color: #27272a;
}

QMenu {
    background-color: #18181b;
    border: 1px solid #27272a;
    color: #ffffff;
}

QMenu::item:selected {
    background-color: #27272a;
}
"""

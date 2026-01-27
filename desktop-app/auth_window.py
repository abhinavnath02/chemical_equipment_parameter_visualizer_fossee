"""
Authentication window for login and registration
Matches web app's design with dark theme
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                              QLineEdit, QPushButton, QFrame, QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from api_client import APIClient
import re


class AuthWindow(QDialog):
    """Authentication dialog for login/register"""
    
    login_successful = pyqtSignal(object)  # Emits APIClient on successful login
    
    def __init__(self, api_client: APIClient):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setFixedSize(450, 600)
        self.setModal(True)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)
        
        # Title
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setProperty("heading", True)
        title.setAlignment(Qt.AlignCenter)
        title.setWordWrap(True)
        main_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Sign in to continue")
        subtitle.setProperty("subheading", True)
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        
        main_layout.addSpacing(10)
        
        # Stacked widget for login/register forms
        self.stacked_widget = QStackedWidget()
        self.login_widget = self.create_login_form()
        self.register_widget = self.create_register_form()
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)
        main_layout.addWidget(self.stacked_widget)
        
        # Toggle button
        self.toggle_button = QPushButton("Don't have an account? Register")
        self.toggle_button.setProperty("secondary", True)
        self.toggle_button.clicked.connect(self.toggle_form)
        main_layout.addWidget(self.toggle_button)
        
        main_layout.addStretch()
        
        self.setLayout(main_layout)
    
    def create_login_form(self):
        """Create login form"""
        widget = QFrame()
        widget.setProperty("card", True)
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Username
        username_label = QLabel("Username")
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        layout.addWidget(username_label)
        layout.addWidget(self.login_username)
        
        # Password
        password_label = QLabel("Password")
        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.returnPressed.connect(self.handle_login)
        layout.addWidget(password_label)
        layout.addWidget(self.login_password)
        
        # Error message
        self.login_error = QLabel("")
        self.login_error.setProperty("error", True)
        self.login_error.hide()
        layout.addWidget(self.login_error)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)
        
        widget.setLayout(layout)
        return widget
    
    def create_register_form(self):
        """Create registration form"""
        widget = QFrame()
        widget.setProperty("card", True)
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Username
        username_label = QLabel("Username")
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Choose a username")
        layout.addWidget(username_label)
        layout.addWidget(self.register_username)
        
        # Email
        email_label = QLabel("Email")
        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Enter your email")
        layout.addWidget(email_label)
        layout.addWidget(self.register_email)
        
        # Password
        password_label = QLabel("Password")
        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setPlaceholderText("Create a password")
        self.register_password.textChanged.connect(self.validate_password)
        layout.addWidget(password_label)
        layout.addWidget(self.register_password)
        
        # Password requirements
        self.password_requirements = QLabel()
        self.password_requirements.setProperty("subheading", True)
        self.password_requirements.setWordWrap(True)
        self.password_requirements.hide()
        layout.addWidget(self.password_requirements)
        
        # Confirm Password
        confirm_label = QLabel("Confirm Password")
        self.register_password2 = QLineEdit()
        self.register_password2.setEchoMode(QLineEdit.Password)
        self.register_password2.setPlaceholderText("Confirm your password")
        self.register_password2.textChanged.connect(self.validate_password_match)
        self.register_password2.returnPressed.connect(self.handle_register)
        layout.addWidget(confirm_label)
        layout.addWidget(self.register_password2)
        
        # Password match indicator
        self.password_match = QLabel()
        self.password_match.setProperty("subheading", True)
        self.password_match.hide()
        layout.addWidget(self.password_match)
        
        # Error message
        self.register_error = QLabel("")
        self.register_error.setProperty("error", True)
        self.register_error.hide()
        layout.addWidget(self.register_error)
        
        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.handle_register)
        self.register_button.setEnabled(False)
        layout.addWidget(self.register_button)
        
        widget.setLayout(layout)
        return widget
    
    def validate_password(self):
        """Validate password requirements"""
        password = self.register_password.text()
        
        if not password:
            self.password_requirements.hide()
            self.update_register_button_state()
            return
        
        requirements = []
        requirements.append(("✓" if len(password) >= 8 else "✗") + " At least 8 characters")
        requirements.append(("✓" if re.search(r'[A-Z]', password) else "✗") + " Contains uppercase letter")
        requirements.append(("✓" if re.search(r'[a-z]', password) else "✗") + " Contains lowercase letter")
        requirements.append(("✓" if re.search(r'\d', password) else "✗") + " Contains number")
        
        self.password_requirements.setText("\n".join(requirements))
        self.password_requirements.show()
        
        self.update_register_button_state()
    
    def validate_password_match(self):
        """Check if passwords match"""
        password = self.register_password.text()
        password2 = self.register_password2.text()
        
        if not password2:
            self.password_match.hide()
            self.update_register_button_state()
            return
        
        if password == password2:
            self.password_match.setText("✓ Passwords match")
            self.password_match.setStyleSheet("color: #22c55e;")
        else:
            self.password_match.setText("✗ Passwords don't match")
            self.password_match.setStyleSheet("color: #ef4444;")
        
        self.password_match.show()
        self.update_register_button_state()
    
    def update_register_button_state(self):
        """Enable/disable register button based on validation"""
        password = self.register_password.text()
        password2 = self.register_password2.text()
        
        valid = (
            len(password) >= 8 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'\d', password) and
            password == password2 and
            self.register_username.text() and
            self.register_email.text()
        )
        
        self.register_button.setEnabled(valid)
    
    def handle_login(self):
        """Handle login button click"""
        username = self.login_username.text().strip()
        password = self.login_password.text()
        
        if not username or not password:
            self.show_login_error("Please enter username and password")
            return
        
        self.login_button.setEnabled(False)
        self.login_button.setText("Logging in...")
        
        success, message = self.api_client.login(username, password)
        
        self.login_button.setEnabled(True)
        self.login_button.setText("Login")
        
        if success:
            self.login_successful.emit(self.api_client)
            self.accept()
        else:
            self.show_login_error(message)
    
    def handle_register(self):
        """Handle register button click"""
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        password = self.register_password.text()
        password2 = self.register_password2.text()
        
        if not all([username, email, password, password2]):
            self.show_register_error("Please fill in all fields")
            return
        
        self.register_button.setEnabled(False)
        self.register_button.setText("Creating account...")
        
        success, message = self.api_client.register(username, email, password, password2)
        
        self.register_button.setEnabled(True)
        self.register_button.setText("Register")
        
        if success:
            self.login_successful.emit(self.api_client)
            self.accept()
        else:
            self.show_register_error(message)
    
    def toggle_form(self):
        """Toggle between login and register forms"""
        if self.stacked_widget.currentIndex() == 0:
            self.stacked_widget.setCurrentIndex(1)
            self.toggle_button.setText("Already have an account? Login")
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.toggle_button.setText("Don't have an account? Register")
        
        # Clear errors
        self.login_error.hide()
        self.register_error.hide()
    
    def show_login_error(self, message: str):
        """Show login error message"""
        self.login_error.setText(message)
        self.login_error.show()
    
    def show_register_error(self, message: str):
        """Show register error message"""
        self.register_error.setText(message)
        self.register_error.show()

"""
Main entry point for the desktop application
"""
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from auth_window import AuthWindow
from dashboard import DashboardWindow
from api_client import APIClient
from styles import DARK_STYLESHEET


class App(QApplication):
    """Main application"""
    
    def __init__(self, argv):
        super().__init__(argv)
        self.setApplicationName("Chemical Equipment Parameter Visualizer")
        self.setStyleSheet(DARK_STYLESHEET)
        
        # Set dark palette
        self.setAttribute(Qt.AA_EnableHighDpiScaling)
        
        # Create API client
        self.api_client = APIClient()
        
        # Show auth window
        self.auth_window = AuthWindow(self.api_client)
        self.auth_window.login_successful.connect(self.show_dashboard)
        self.auth_window.show()
    
    def show_dashboard(self, api_client):
        """Show dashboard after successful login"""
        self.auth_window.close()
        self.dashboard = DashboardWindow(api_client)
        self.dashboard.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

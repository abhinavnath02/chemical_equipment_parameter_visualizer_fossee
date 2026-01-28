"""
API Client for communicating with Django backend
"""
import requests
from typing import Optional, Dict, List, Tuple


class APIClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000/api"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.user: Optional[Dict] = None

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with authorization token"""
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def register(self, username: str, email: str, password: str, password2: str) -> Tuple[bool, str]:
        """Register a new user"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/register/",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                    "password2": password2
                }
            )
            
            if response.status_code == 201:
                # Auto-login after registration
                return self.login(username, password)
            else:
                error = response.json()
                error_msg = " ".join([str(v) for v in error.values()])
                return False, error_msg
        except Exception as e:
            return False, str(e)

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """Login user and get tokens"""
        try:
            response = requests.post(
                f"{self.base_url}/auth/login/",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access")
                self.refresh_token = data.get("refresh")
                
                # Fetch user profile
                user_response = requests.get(
                    f"{self.base_url}/auth/user/",
                    headers=self._get_headers()
                )
                
                if user_response.status_code == 200:
                    self.user = user_response.json()
                    return True, "Login successful"
                else:
                    return False, "Failed to fetch user profile"
            else:
                error = response.json()
                return False, error.get("detail", "Login failed")
        except Exception as e:
            return False, str(e)

    def upload_csv(self, file_path: str) -> Tuple[bool, Optional[Dict], str]:
        """Upload CSV file for analysis"""
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                headers = {}
                if self.access_token:
                    headers["Authorization"] = f"Bearer {self.access_token}"
                
                response = requests.post(
                    f"{self.base_url}/upload/",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 201:
                    return True, response.json(), "Upload successful"
                else:
                    error = response.json()
                    return False, None, error.get("error", "Upload failed")
        except Exception as e:
            return False, None, str(e)

    def get_history(self) -> Tuple[bool, Optional[List], str]:
        """Get upload history"""
        try:
            response = requests.get(
                f"{self.base_url}/history/",
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return True, response.json(), "Success"
            else:
                return False, None, "Failed to fetch history"
        except Exception as e:
            return False, None, str(e)

    def get_dataset(self, dataset_id: int) -> Tuple[bool, Optional[Dict], str]:
        """Get specific dataset by ID"""
        try:
            response = requests.get(
                f"{self.base_url}/dataset/{dataset_id}/",
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return True, response.json(), "Success"
            else:
                return False, None, "Dataset not found"
        except Exception as e:
            return False, None, str(e)

    def generate_pdf(self, analysis_data: Dict) -> Tuple[bool, Optional[bytes], str]:
        """Generate PDF report"""
        try:
            response = requests.post(
                f"{self.base_url}/generate-pdf/",
                json=analysis_data,
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                return True, response.content, "PDF generated successfully"
            else:
                return False, None, "Failed to generate PDF"
        except Exception as e:
            return False, None, str(e)

    def logout(self):
        """Clear authentication tokens"""
        self.access_token = None
        self.refresh_token = None
        self.user = None

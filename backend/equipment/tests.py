from django.test import TestCase
from .utils import analyze_csv
from io import StringIO

class AnalyticsTest(TestCase):
    def test_valid_csv(self):
        csv = StringIO(
            "Equipment Name,Type,Flowrate,Pressure,Temperature\n"
            "Pump A,Pump,100,10,80\n"
        )
        summary = analyze_csv(csv)
        self.assertEqual(summary["total_equipment"], 1)


from rest_framework.test import APIClient
from django.contrib.auth.models import User
from io import BytesIO

class UploadAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user("test", "test@test.com", "1234")
        self.client.force_authenticate(user=self.user)

    def test_upload(self):
        csv = BytesIO(
            b"Equipment Name,Type,Flowrate,Pressure,Temperature\nPump A,Pump,100,10,80"
        )
        response = self.client.post("/api/upload/", {"file": csv})
        self.assertEqual(response.status_code, 201)

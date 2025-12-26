import sys
import os
import unittest
from fastapi.testclient import TestClient
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from services.service import service

client = TestClient(app)


class TestCustomerPrediction(unittest.TestCase):
    def test_logic_low_spend(self):
        result = service.predict(age=30, income=10000, spend=500)
        self.assertEqual(result["prediction"], "low")

    def test_logic_medium_spend(self):
        result = service.predict(age=30, income=10000, spend=2000)
        self.assertEqual(result["prediction"], "medium")

    def test_logic_high_spend(self):
        result = service.predict(age=30, income=10000, spend=5000)
        self.assertEqual(result["prediction"], "high")

    def test_api_predict_success(self):
        payload = {
            "customer_id": "TEST-001",
            "features": {"age": 25, "income": 50000, "avg_monthly_spend": 20000},
        }
        response = client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["customer_id"], "TEST-001")
        self.assertIn("prediction", data)


if __name__ == "__main__":
    unittest.main()

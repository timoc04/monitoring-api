import unittest

from app import create_app, db


class MonitoringApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
        })

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_health_endpoint(self):
        response = self.client.get("/api/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "ok")

    def test_create_measurement_success(self):
        payload = {
            "hostname": "server01",
            "ip_address": "192.168.10.5",
            "cpu_usage": 25.5,
            "memory_usage": 60.2
        }

        response = self.client.post("/api/measurements", json=payload)

        self.assertEqual(response.status_code, 201)

    def test_create_measurement_missing_field(self):
        payload = {
            "hostname": "server01"
        }

        response = self.client.post("/api/measurements", json=payload)

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
import unittest
from fastapi.testclient import TestClient
from api.main import app, auth_service, pipeline


class ApiAuthTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_login_success_returns_jwt_token(self):
        response = self.client.post(
            "/login",
            json={"username": "admin1", "password": "admin123"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual(data["token_type"], "bearer")
        self.assertEqual(data["user"]["username"], "admin1")
        self.assertEqual(data["user"]["role"], "admin")

    def test_login_failure_returns_401(self):
        response = self.client.post(
            "/login",
            json={"username": "admin1", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid username or password", response.json()["detail"])

    def test_query_without_token_returns_401_or_403(self):
        response = self.client.post(
            "/query",
            json={"question": "What is the code of ethics?"}
        )
        self.assertIn(response.status_code, [401, 403])

    def test_query_with_invalid_token_returns_401(self):
        headers = {"Authorization": "Bearer invalid.fake.token"}
        response = self.client.post(
            "/query",
            json={"question": "What is the code of ethics?"},
            headers=headers
        )
        self.assertEqual(response.status_code, 401)

    def test_query_with_valid_token_authenticated(self):
        # Generate valid token
        token = auth_service.create_access_token(
            data={"sub": "admin1", "role": "admin", "domain": None}
        )
        headers = {"Authorization": f"Bearer {token}"}
        
        response = self.client.post(
            "/query",
            json={"question": "What is the code of ethics?"},
            headers=headers
        )
        # Even if pipeline documents are mock or real, it should pass auth and return 200 or processed response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("answer", data)
        self.assertIn("sources", data)
        self.assertEqual(data["user"]["username"], "admin1")
        self.assertEqual(data["user"]["role"], "admin")


if __name__ == "__main__":
    unittest.main()

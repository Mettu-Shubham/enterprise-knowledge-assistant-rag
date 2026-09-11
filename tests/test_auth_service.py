from datetime import timedelta
import os
import json
import tempfile
import unittest
from src.auth.auth_service import AuthService


class AuthServiceTests(unittest.TestCase):

    def setUp(self):
        self.auth_service = AuthService()
        self.plain_pw = "secret123"
        self.hashed_pw = AuthService.hash_password(self.plain_pw)

    def test_hash_password_generates_valid_bcrypt_hash(self):
        self.assertTrue(self.hashed_pw.startswith("$2b$"))
        self.assertNotEqual(self.plain_pw, self.hashed_pw)

    def test_verify_password_correct(self):
        self.assertTrue(AuthService.verify_password(self.plain_pw, self.hashed_pw))

    def test_verify_password_incorrect(self):
        self.assertFalse(AuthService.verify_password("wrongpass", self.hashed_pw))

    def test_authenticate_with_temp_hashed_users_file(self):
        temp_file = tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json")
        try:
            users_data = [
                {
                    "username": "test_admin",
                    "password": self.hashed_pw,
                    "role": "admin",
                    "domain": None
                }
            ]
            json.dump(users_data, temp_file)
            temp_file.close()

            service = AuthService(users_path=temp_file.name)
            
            # Valid login
            user = service.authenticate("test_admin", "secret123")
            self.assertIsNotNone(user)
            self.assertEqual(user["username"], "test_admin")
            self.assertEqual(user["role"], "admin")

            # Invalid login
            invalid_user = service.authenticate("test_admin", "wrongpassword")
            self.assertIsNone(invalid_user)
        finally:
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)

    def test_create_and_decode_jwt_token_valid(self):
        payload = {"sub": "test_user", "role": "employee", "domain": "govt_policy"}
        token = self.auth_service.create_access_token(payload)

        decoded = self.auth_service.decode_access_token(token)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["sub"], "test_user")
        self.assertEqual(decoded["role"], "employee")
        self.assertEqual(decoded["domain"], "govt_policy")
        self.assertIn("exp", decoded)

    def test_decode_jwt_token_expired(self):
        payload = {"sub": "test_user", "role": "client"}
        # Create token that expired 10 minutes ago
        token = self.auth_service.create_access_token(
            payload,
            expires_delta=timedelta(minutes=-10)
        )

        decoded = self.auth_service.decode_access_token(token)
        self.assertIsNone(decoded)

    def test_decode_jwt_token_invalid_signature(self):
        other_service = AuthService(jwt_secret_key="different-secret-key-for-testing-32bytes!")
        token = other_service.create_access_token({"sub": "attacker"})

        decoded = self.auth_service.decode_access_token(token)
        self.assertIsNone(decoded)



if __name__ == "__main__":
    unittest.main()


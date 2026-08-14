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


if __name__ == "__main__":
    unittest.main()

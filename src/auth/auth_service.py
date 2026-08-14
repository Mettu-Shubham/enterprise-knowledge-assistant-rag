import json
import os
import bcrypt


class AuthService:

    def __init__(self, users_path="data/users.json"):
        self.users_path = users_path

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Hash a plain text password using bcrypt."""
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a stored hash or string."""
        if not hashed_password:
            return False
        if hashed_password.startswith("$2b$") or hashed_password.startswith("$2a$"):
            try:
                return bcrypt.checkpw(
                    plain_password.encode("utf-8"),
                    hashed_password.encode("utf-8")
                )
            except Exception:
                return False
        # Fallback for plain text legacy passwords
        return plain_password == hashed_password

    def load_users(self):
        if not os.path.exists(self.users_path):
            return []

        with open(self.users_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def authenticate(self, username, password):
        users = self.load_users()

        for user in users:
            if user["username"] == username and self.verify_password(password, user["password"]):
                return {
                    "username": user["username"],
                    "role": user["role"],
                    "domain": user.get("domain")
                }

        return None
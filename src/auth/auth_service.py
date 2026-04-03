import json
import os


class AuthService:

    def __init__(self, users_path="data/users.json"):
        self.users_path = users_path

    def load_users(self):
        if not os.path.exists(self.users_path):
            return []

        with open(self.users_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def authenticate(self, username, password):
        users = self.load_users()

        for user in users:
            if user["username"] == username and user["password"] == password:
                return {
                    "username": user["username"],
                    "role": user["role"],
                    "domain": user.get("domain")
                }

        return None
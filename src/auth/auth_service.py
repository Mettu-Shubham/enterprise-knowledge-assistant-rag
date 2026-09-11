from datetime import datetime
from datetime import timedelta
from datetime import timezone
import json
import os
import bcrypt
import jwt


class AuthService:

    def __init__(
        self,
        users_path="data/users.json",
        jwt_secret_key="dev-secret-key-change-in-prod-1234567890",
        jwt_algorithm="HS256",
        jwt_expiration_minutes=60
    ):
        self.users_path = users_path
        self.jwt_secret_key = jwt_secret_key
        self.jwt_algorithm = jwt_algorithm
        self.jwt_expiration_minutes = jwt_expiration_minutes

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        """Create a signed JWT access token."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (
            expires_delta if expires_delta is not None else timedelta(minutes=self.jwt_expiration_minutes)
        )
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.jwt_secret_key, algorithm=self.jwt_algorithm)

    def decode_access_token(self, token: str) -> dict | None:
        """Decode and validate a JWT access token."""
        try:
            payload = jwt.decode(
                token,
                self.jwt_secret_key,
                algorithms=[self.jwt_algorithm]
            )
            return payload
        except jwt.PyJWTError:
            return None


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
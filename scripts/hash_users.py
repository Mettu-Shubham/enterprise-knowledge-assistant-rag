import json
import os
import bcrypt


def hash_password(plain_password: str) -> str:
    """Hash a plain text password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def is_already_hashed(password: str) -> bool:
    """Check if the password string is already a bcrypt hash."""
    return password.startswith("$2b$") or password.startswith("$2a$")


def hash_users_file(users_path: str = "data/users.json"):
    """
    Migrates plaintext passwords in users.json to bcrypt hashes.
    """
    if not os.path.exists(users_path):
        print(f"Users file not found at: {users_path}")
        return

    with open(users_path, "r", encoding="utf-8") as f:
        users = json.load(f)

    updated_count = 0
    for user in users:
        current_password = user.get("password", "")
        if not is_already_hashed(current_password):
            user["password"] = hash_password(current_password)
            updated_count += 1
            print(f"Hashed password for user: {user['username']}")
        else:
            print(f"User {user['username']} already has a hashed password.")

    if updated_count > 0:
        with open(users_path, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)
        print(f"\nSuccessfully updated {updated_count} user password(s) in {users_path}.")
    else:
        print(f"\nNo users required updating in {users_path}.")


if __name__ == "__main__":
    hash_users_file()

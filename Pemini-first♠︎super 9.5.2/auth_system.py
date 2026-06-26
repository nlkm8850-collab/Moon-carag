"""
Pemini Girl 9.5.2 - Authentication System
"""

import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
import json
import os

class UserRole(Enum):
    ADMIN = "admin"
    DEVELOPER = "developer"
    STUDENT = "student"
    GUEST = "guest"

class AuthProvider(Enum):
    LOCAL = "local"
    GITHUB = "github"
    GOOGLE = "google"
    MICROSOFT = "microsoft"

@dataclass
class UserProfile:
    user_id: str
    username: str
    email: str
    display_name: str
    role: UserRole = UserRole.DEVELOPER
    auth_provider: AuthProvider = AuthProvider.LOCAL
    preferred_language: str = "ar"
    preferred_theme: str = "dark"
    default_code_language: str = "python"
    created_at: str = ""
    last_login: str = ""
    is_active: bool = True
    profile_picture: str = ""
    bio: str = ""
    location: str = ""
    github_username: str = ""
    total_code_generated: int = 0
    total_code_analyzed: int = 0
    favorite_snippets: List[str] = None

    def __post_init__(self):
        if self.favorite_snippets is None:
            self.favorite_snippets = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

class AuthenticationManager:
    SECRET_KEY = "pemini-girl-952-secret-key-change-in-production"
    TOKEN_EXPIRY_HOURS = 24

    def __init__(self, db_path: str = "users.json"):
        self.db_path = db_path
        self.users: Dict[str, Dict] = {}
        self.sessions: Dict[str, Dict] = {}
        self._load_users()

    def _load_users(self):
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
            except:
                self.users = {}

    def _save_users(self):
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)

    def _hash_password(self, password: str, salt: str = None):
        if salt is None:
            salt = secrets.token_hex(16)
        hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
        return hashed.hex(), salt

    def _verify_password(self, password: str, hashed: str, salt: str):
        new_hash, _ = self._hash_password(password, salt)
        return new_hash == hashed

    def _generate_token(self, user_id: str, token_type: str = "access"):
        expiry = datetime.utcnow() + timedelta(
            hours=self.TOKEN_EXPIRY_HOURS if token_type == "access" else 7 * 24
        )
        payload = {
            "user_id": user_id,
            "type": token_type,
            "exp": expiry,
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

    def register_user(self, username: str, email: str, password: str,
                     display_name: str = None, role: UserRole = UserRole.DEVELOPER):
        for user_data in self.users.values():
            if user_data.get("username") == username:
                return {"success": False, "message": "Username already exists", "user": None}
            if user_data.get("email") == email:
                return {"success": False, "message": "Email already used", "user": None}

        user_id = secrets.token_hex(8)
        hashed_pw, salt = self._hash_password(password)

        user_data = {
            "user_id": user_id,
            "username": username,
            "email": email,
            "display_name": display_name or username,
            "password_hash": hashed_pw,
            "salt": salt,
            "role": role.value,
            "auth_provider": AuthProvider.LOCAL.value,
            "preferred_language": "ar",
            "preferred_theme": "dark",
            "default_code_language": "python",
            "created_at": datetime.now().isoformat(),
            "last_login": "",
            "is_active": True,
            "profile_picture": "",
            "bio": "",
            "location": "",
            "github_username": "",
            "total_code_generated": 0,
            "total_code_analyzed": 0,
            "favorite_snippets": []
        }

        self.users[user_id] = user_data
        self._save_users()

        return {
            "success": True,
            "message": "Registration successful!",
            "user": UserProfile(**{k: v for k, v in user_data.items() if k not in ["password_hash", "salt"]})
        }

    def login(self, username_or_email: str, password: str):
        user_data = None
        user_id = None
        for uid, data in self.users.items():
            if data.get("username") == username_or_email or data.get("email") == username_or_email:
                user_data = data
                user_id = uid
                break

        if not user_data:
            return {"success": False, "message": "User not found", "token": None, "refresh_token": None, "user": None}

        if not self._verify_password(password, user_data["password_hash"], user_data["salt"]):
            return {"success": False, "message": "Invalid password", "token": None, "refresh_token": None, "user": None}

        user_data["last_login"] = datetime.now().isoformat()
        self.users[user_id] = user_data
        self._save_users()

        access_token = self._generate_token(user_id, "access")
        refresh_token = self._generate_token(user_id, "refresh")

        self.sessions[access_token] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat()
        }

        user_profile = UserProfile(**{k: v for k, v in user_data.items() if k not in ["password_hash", "salt"]})

        return {
            "success": True,
            "message": "Login successful!",
            "token": access_token,
            "refresh_token": refresh_token,
            "user": user_profile
        }

    def logout(self, token: str):
        if token in self.sessions:
            del self.sessions[token]
            return True
        return False

    def verify_token(self, token: str):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if user_id and user_id in self.users:
                user_data = self.users[user_id]
                return UserProfile(**{k: v for k, v in user_data.items() if k not in ["password_hash", "salt"]})
        except:
            return None
        return None

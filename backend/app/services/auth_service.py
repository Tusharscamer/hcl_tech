from typing import Optional, Dict, Any
from ..config.database import db
from ..utils.security import verify_password, create_access_token

class AuthService:
    @staticmethod
    def authenticate_user(username_or_id: str, password: str) -> Optional[Dict[str, Any]]:
        # Find by customer_id or email
        user = db.find_one("users", {"customer_id": username_or_id})
        if not user:
            user = db.find_one("users", {"email": username_or_id})

        if not user:
            return None

        # Check password against hash or plain
        if not verify_password(password, user.get("password_plain", "")) and not verify_password(password, user.get("password_hash", "")):
            return None

        return user

    @staticmethod
    def create_user_token(user: Dict[str, Any]) -> str:
        payload = {
            "sub": user["customer_id"],
            "name": user["name"],
            "role": user.get("role", "customer"),
            "email": user["email"]
        }
        return create_access_token(payload)

auth_service = AuthService()

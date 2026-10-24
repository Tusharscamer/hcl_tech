from typing import Dict, Any
from ...services.auth_service import auth_service
from ...config.database import db

def handle_login(data: Dict[str, Any]) -> Dict[str, Any]:
    username = data.get("username_or_id") or data.get("username") or data.get("customer_id", "")
    password = data.get("password", "")

    user = auth_service.authenticate_user(username, password)
    if not user:
        return {"success": False, "status_code": 401, "message": "Invalid customer ID, email, or password."}

    token = auth_service.create_user_token(user)
    return {
        "success": True,
        "status_code": 200,
        "data": {
            "access_token": token,
            "token_type": "bearer",
            "customer_id": user["customer_id"],
            "name": user["name"],
            "role": user.get("role", "customer"),
            "email": user["email"]
        }
    }

def handle_get_me(user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    profile = db.find_one("users", {"customer_id": cid})
    if not profile:
        return {"success": False, "status_code": 404, "message": "User profile not found."}

    # Hide password hash
    sanitized = {k: v for k, v in profile.items() if not k.startswith("password")}
    return {"success": True, "status_code": 200, "data": sanitized}

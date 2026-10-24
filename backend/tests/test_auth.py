import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.auth_service import auth_service
from app.utils.security import decode_access_token

def test_authentication():
    # Customer login
    user = auth_service.authenticate_user("C1001", "password123")
    assert user is not None
    assert user["customer_id"] == "C1001"
    assert user["role"] == "customer"

    token = auth_service.create_user_token(user)
    assert token is not None
    payload = decode_access_token(token)
    assert payload["sub"] == "C1001"

    # Admin login
    admin = auth_service.authenticate_user("A9001", "admin123")
    assert admin is not None
    assert admin["role"] == "admin"

    # Invalid login
    bad = auth_service.authenticate_user("C1001", "wrong_password")
    assert bad is None
    print("test_authentication passed")

if __name__ == "__main__":
    test_authentication()
    print("All auth tests PASSED!")

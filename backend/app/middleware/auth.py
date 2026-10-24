from typing import Optional, Dict, Any
from ..utils.security import decode_access_token

def authenticate_token(authorization_header: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Validates Bearer JWT token from header and extracts user payload.
    """
    if not authorization_header:
        return None

    parts = authorization_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]
    payload = decode_access_token(token)
    return payload

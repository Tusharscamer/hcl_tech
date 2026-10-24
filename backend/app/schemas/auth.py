from typing import Optional
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username_or_id: str  # customer_id or email
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    customer_id: str
    name: str
    role: str

class UserProfileResponse(BaseModel):
    customer_id: str
    name: str
    email: str
    phone: Optional[str] = None
    role: str
    kyc_status: str
    credit_score: int

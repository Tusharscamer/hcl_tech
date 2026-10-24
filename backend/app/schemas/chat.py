from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default-session"
    context: Optional[Dict[str, Any]] = None

class ActionConfirmationRequest(BaseModel):
    trace_id: str
    action_type: str  # BLOCK_CARD, RAISE_DISPUTE, INCREASE_LIMIT, APPROVE_PAYMENT
    action_payload: Dict[str, Any]
    confirmed: bool

class ChatResponse(BaseModel):
    trace_id: str
    answer: str
    answer_type: str = "conversational"  # conversational, calculated, retrieved, action_required, action_completed
    tools_invoked: List[str] = []
    systems_queried: List[str] = []
    requires_approval: bool = False
    requires_confirmation: bool = False
    action_type: Optional[str] = None
    action_payload: Optional[Dict[str, Any]] = None
    structured_data: Optional[Dict[str, Any]] = None
    latency_ms: Optional[float] = None

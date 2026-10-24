from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class AuditLog(BaseModel):
    audit_id: Optional[str] = None
    trace_id: str
    customer_id: str
    timestamp: str
    user_query: str
    tools_invoked: List[str] = []
    systems_queried: List[str] = []
    intent: Optional[str] = None
    decision_reasoning: Optional[str] = None
    action_outcome: Optional[str] = None
    latency_ms: float = 0.0
    status: str = "SUCCESS"  # SUCCESS, ESCALATED, FAILED
    error_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

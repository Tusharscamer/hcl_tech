from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    trace_id: str
    customer_id: str
    session_id: str = "default"
    user_query: str
    chat_history: List[Dict[str, Any]] = Field(default_factory=list)
    intent: Optional[str] = None
    confidence: float = 1.0
    plan: List[str] = Field(default_factory=list)
    tools_to_invoke: List[str] = Field(default_factory=list)
    tools_invoked: List[str] = Field(default_factory=list)
    systems_queried: List[str] = Field(default_factory=list)
    tool_results: Dict[str, Any] = Field(default_factory=dict)
    rag_context: Optional[str] = None
    requires_approval: bool = False
    requires_confirmation: bool = False
    action_type: Optional[str] = None
    action_payload: Optional[Dict[str, Any]] = None
    answer: Optional[str] = None
    answer_type: str = "conversational"
    structured_data: Optional[Dict[str, Any]] = None
    latency_ms: float = 0.0
    status: str = "SUCCESS"
    error: Optional[str] = None

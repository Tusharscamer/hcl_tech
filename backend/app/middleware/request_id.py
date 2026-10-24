from typing import Optional
from ..utils.trace import generate_trace_id

def get_or_generate_request_id(incoming_id: Optional[str] = None) -> str:
    """
    Extracts incoming client X-Request-ID or creates a BANK-XXXXX trace ID.
    """
    if incoming_id and incoming_id.strip():
        return incoming_id.strip()
    return generate_trace_id("BANK")

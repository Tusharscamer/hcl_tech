from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from ..config.database import db
from ..utils.logger import logger

class AuditService:
    @staticmethod
    def log_interaction(
        trace_id: str,
        customer_id: str,
        user_query: str,
        tools_invoked: List[str],
        systems_queried: List[str],
        intent: str,
        decision_reasoning: str,
        action_outcome: str,
        latency_ms: float,
        status: str = "SUCCESS",
        error_message: Optional[str] = None
    ) -> Dict[str, Any]:
        log_entry = {
            "audit_id": f"AUD-{int(datetime.now().timestamp() * 1000)}",
            "trace_id": trace_id,
            "customer_id": customer_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_query": user_query,
            "tools_invoked": tools_invoked,
            "systems_queried": systems_queried,
            "intent": intent,
            "decision_reasoning": decision_reasoning,
            "action_outcome": action_outcome,
            "latency_ms": round(latency_ms, 2),
            "status": status,
            "error_message": error_message
        }
        db.insert_one("audit_logs", log_entry)
        logger.info(f"[AUDIT] [{trace_id}] Customer: {customer_id} | Intent: {intent} | Latency: {latency_ms:.2f}ms | Tools: {tools_invoked}")
        return log_entry

    @staticmethod
    def get_audit_logs(limit: int = 50) -> List[Dict[str, Any]]:
        logs = db.find("audit_logs")
        logs = sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)
        return logs[:limit]

audit_service = AuditService()

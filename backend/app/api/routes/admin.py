from typing import Dict, Any
from ...config.database import db
from ...services.audit_service import audit_service
from ...utils.logger import logger

def handle_get_approvals(user: Dict[str, Any]) -> Dict[str, Any]:
    # Approvals list for Bank Employee review
    approvals = db.find("approvals")
    approvals = sorted(approvals, key=lambda x: x.get("created_at", ""), reverse=True)
    return {"success": True, "status_code": 200, "data": approvals}

def handle_decide_approval(approval_id: str, data: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    decision = data.get("decision", "APPROVED")  # APPROVED or REJECTED
    notes = data.get("notes", "Reviewed and authorized by Operations Officer")
    admin_id = user.get("sub") or user.get("customer_id", "A9001")

    item = db.find_one("approvals", {"approval_id": approval_id})
    if not item:
        return {"success": False, "status_code": 404, "message": f"Approval request {approval_id} not found."}

    db.update_one("approvals", {"approval_id": approval_id}, {
        "status": decision,
        "reviewed_by": admin_id,
        "review_notes": notes
    })

    # If it was a dispute, update dispute record
    if item.get("type") == "TRANSACTION_DISPUTE":
        dispute_id = item.get("reference_id")
        db.update_one("disputes", {"dispute_id": dispute_id}, {
            "status": "APPROVED" if decision == "APPROVED" else "REJECTED",
            "admin_notes": notes
        })

    logger.info(f"[ADMIN HITL] Approval {approval_id} decided as {decision} by {admin_id}")
    return {
        "success": True,
        "status_code": 200,
        "data": {
            "approval_id": approval_id,
            "status": decision,
            "reviewed_by": admin_id
        }
    }

def handle_get_audit_logs(user: Dict[str, Any]) -> Dict[str, Any]:
    logs = audit_service.get_audit_logs(limit=50)
    return {"success": True, "status_code": 200, "data": logs}

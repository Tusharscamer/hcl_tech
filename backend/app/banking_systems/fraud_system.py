from typing import Dict, Any, Optional
from datetime import datetime, timezone
from ..config.database import db
from ..utils.logger import logger

class FraudSystem:
    """
    Fraud Monitoring & Dispute Resolution Engine.
    """
    @staticmethod
    def verify_transaction(transaction_id: str, customer_id: Optional[str] = None) -> Dict[str, Any]:
        query = {"transaction_id": transaction_id}
        if customer_id:
            query["customer_id"] = customer_id
        txn = db.find_one("transactions", query)
        if not txn:
            # Also search by partial id
            all_txns = db.find("transactions", {"customer_id": customer_id} if customer_id else None)
            for t in all_txns:
                if transaction_id.lower() in t.get("transaction_id", "").lower() or transaction_id.lower() in t.get("merchant", "").lower():
                    txn = t
                    break

        if not txn:
            return {
                "found": False,
                "transaction_id": transaction_id,
                "message": f"Transaction '{transaction_id}' was not found in records."
            }

        # Deterministic Risk Assessment Rules:
        # 1. Foreign / International channel
        # 2. Status FLAGGED
        # 3. High amount overnight
        risk_score = 15
        risk_factors = []
        is_suspicious = False

        if "INTERNATIONAL" in txn.get("channel", "") or "UK" in txn.get("merchant", "") or "FOREIGN" in txn.get("channel", ""):
            risk_score += 55
            risk_factors.append("International overseas merchant channel")

        if txn.get("status") == "FLAGGED":
            risk_score += 30
            risk_factors.append("System anomaly alert: unusual spending pattern")

        if txn.get("amount", 0) > 10000:
            risk_score += 15
            risk_factors.append("High single-charge volume")

        is_suspicious = risk_score >= 60

        return {
            "found": True,
            "transaction_id": txn.get("transaction_id"),
            "amount": txn.get("amount"),
            "merchant": txn.get("merchant"),
            "channel": txn.get("channel"),
            "timestamp": txn.get("timestamp"),
            "risk_score": min(100, risk_score),
            "is_suspicious": is_suspicious,
            "risk_factors": risk_factors,
            "recommendation": "Freeze card immediately and open dispute ticket." if is_suspicious else "Verified regular activity."
        }

    @staticmethod
    def create_dispute(customer_id: str, transaction_id: str, reason: str = "Unrecognized transaction") -> Dict[str, Any]:
        txn = db.find_one("transactions", {"transaction_id": transaction_id})
        amount = txn.get("amount", 0.0) if txn else 0.0

        dispute_id = f"DSP-{int(datetime.now().timestamp())}"
        dispute_doc = {
            "dispute_id": dispute_id,
            "customer_id": customer_id,
            "transaction_id": transaction_id,
            "amount": amount,
            "reason": reason,
            "status": "PENDING_REVIEW",
            "provisional_credit": True,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        db.insert_one("disputes", dispute_doc)

        # Create approval queue item for bank operations staff (HITL)
        approval_id = f"APV-{int(datetime.now().timestamp())}"
        approval_doc = {
            "approval_id": approval_id,
            "type": "TRANSACTION_DISPUTE",
            "customer_id": customer_id,
            "reference_id": dispute_id,
            "title": f"Charge Dispute: ₹{amount:,.2f} at {txn.get('merchant', 'Unknown') if txn else 'Unknown'}",
            "severity": "HIGH",
            "status": "PENDING",
            "data": {
                "transaction_id": transaction_id,
                "amount": amount,
                "reason": reason
            },
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        db.insert_one("approvals", approval_doc)

        logger.info(f"[FraudSystem] Dispute {dispute_id} created and queued for Human-in-the-Loop review.")
        return {
            "dispute_id": dispute_id,
            "status": "PENDING_REVIEW",
            "provisional_credit": True,
            "approval_id": approval_id,
            "message": f"Dispute ticket {dispute_id} has been submitted under bank controls. Provisional credit initiated."
        }

fraud_system = FraudSystem()

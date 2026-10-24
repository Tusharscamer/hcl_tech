from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from ..config.database import db
from ..utils.logger import logger

class PaymentSystem:
    """
    Simulates Payment Gateway and UPI switch for status verification and transfers.
    """
    @staticmethod
    def get_payment_status(customer_id: str, query: Optional[str] = None, reference_number: Optional[str] = None) -> List[Dict[str, Any]]:
        txns = db.find("transactions", {"customer_id": customer_id})
        results = []
        for t in txns:
            # Match by reference number or merchant/description keyword
            if reference_number and t.get("reference_number") == reference_number:
                results.append(t)
            elif query:
                q_lower = query.lower()
                if q_lower in t.get("merchant", "").lower() or q_lower in t.get("description", "").lower():
                    results.append(t)
        if not results and not reference_number and not query:
            return txns[:5]
        logger.info(f"[PaymentSystem] Query '{query or reference_number}' returned {len(results)} matches.")
        return results

    @staticmethod
    def get_upcoming_bills(customer_id: str) -> List[Dict[str, Any]]:
        bills = db.find("bills", {"customer_id": customer_id, "status": "UPCOMING"})
        logger.info(f"[PaymentSystem] Retrieved {len(bills)} upcoming bills for customer {customer_id}")
        return bills

    @staticmethod
    def process_payment(customer_id: str, recipient: str, amount: float, channel: str = "UPI") -> Dict[str, Any]:
        ref_id = f"{channel}{int(datetime.now().timestamp())}"
        payment_record = {
            "payment_id": f"PAY-{int(datetime.now().timestamp())}",
            "customer_id": customer_id,
            "recipient": recipient,
            "amount": amount,
            "channel": channel,
            "status": "COMPLETED",
            "reference_number": ref_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        db.insert_one("payments", payment_record)
        return payment_record

payment_system = PaymentSystem()

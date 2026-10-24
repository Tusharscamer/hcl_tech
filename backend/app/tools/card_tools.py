from typing import Dict, Any, Optional
from ..banking_systems.card_system import card_system

def get_credit_card_details(customer_id: str) -> Dict[str, Any]:
    """
    Deterministic Tool: Retrieves credit card statement details, due date, min/total amount due.
    """
    cards = card_system.get_credit_cards(customer_id)
    if not cards:
        return {
            "found": False,
            "message": "No credit card account found for this customer."
        }
    primary_card = cards[0]
    return {
        "found": True,
        "customer_id": customer_id,
        "card_id": primary_card.get("card_id"),
        "card_number": primary_card.get("card_number"),
        "network": primary_card.get("network"),
        "total_due": primary_card.get("total_due"),
        "minimum_due": primary_card.get("minimum_due"),
        "statement_due_date": primary_card.get("statement_due_date"),
        "credit_limit": primary_card.get("credit_limit"),
        "available_limit": primary_card.get("available_limit"),
        "status": primary_card.get("status"),
        "billing_cycle": primary_card.get("billing_cycle")
    }

def block_card(customer_id: str, card_type: Optional[str] = "DEBIT", card_id: Optional[str] = None, reason: str = "Customer lost card") -> Dict[str, Any]:
    """
    Deterministic Tool: Blocks debit or credit card under bank security controls and initiates replacement.
    """
    return card_system.block_card(customer_id=customer_id, card_type=card_type, card_id=card_id, reason=reason)

def request_limit_change(customer_id: str, card_id: str, requested_limit: float) -> Dict[str, Any]:
    """
    Deterministic Tool: Submits credit limit change request.
    """
    return {
        "customer_id": customer_id,
        "card_id": card_id,
        "requested_limit": requested_limit,
        "status": "PENDING_APPROVAL",
        "message": f"Credit limit change to ₹{requested_limit:,.2f} submitted for risk assessment."
    }

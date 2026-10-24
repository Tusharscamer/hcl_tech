from typing import List, Dict, Any, Optional
from ..config.database import db
from ..utils.logger import logger

class CardSystem:
    """
    Card Management System (CMS) for credit/debit card lifecycle and blocking.
    """
    @staticmethod
    def get_cards(customer_id: str) -> List[Dict[str, Any]]:
        return db.find("cards", {"customer_id": customer_id})

    @staticmethod
    def get_credit_cards(customer_id: str) -> List[Dict[str, Any]]:
        return db.find("cards", {"customer_id": customer_id, "card_type": "CREDIT"})

    @staticmethod
    def get_card_by_id(card_id: str) -> Optional[Dict[str, Any]]:
        return db.find_one("cards", {"card_id": card_id})

    @staticmethod
    def block_card(customer_id: str, card_type: Optional[str] = None, card_id: Optional[str] = None, reason: str = "Customer lost card") -> Dict[str, Any]:
        cards = db.find("cards", {"customer_id": customer_id})
        target_card = None
        for c in cards:
            if card_id and c.get("card_id") == card_id:
                target_card = c
                break
            elif card_type and c.get("card_type") == card_type.upper():
                target_card = c
                break

        if not target_card and cards:
            # Default to first card if unspecified
            target_card = cards[0]

        if not target_card:
            return {"success": False, "message": "No active card found to block."}

        db.update_one("cards", {"card_id": target_card["card_id"]}, {"status": "BLOCKED"})
        logger.warning(f"[CardSystem] Card {target_card['card_id']} successfully BLOCKED for reason: {reason}")
        return {
            "success": True,
            "card_id": target_card["card_id"],
            "card_number": target_card["card_number"],
            "status": "BLOCKED",
            "message": f"{target_card['card_type']} card ({target_card['card_number']}) has been blocked immediately.",
            "replacement_dispatched": True,
            "estimated_delivery_days": 4
        }

    @staticmethod
    def update_card_limit(card_id: str, new_limit: float) -> bool:
        return db.update_one("cards", {"card_id": card_id}, {"credit_limit": new_limit, "available_limit": new_limit})

card_system = CardSystem()

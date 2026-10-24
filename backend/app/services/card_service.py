from typing import Dict, Any, List, Optional
from ..banking_systems.card_system import card_system

class CardService:
    @staticmethod
    def get_cards(customer_id: str) -> List[Dict[str, Any]]:
        return card_system.get_cards(customer_id)

    @staticmethod
    def block_card(customer_id: str, card_type: Optional[str] = None, card_id: Optional[str] = None, reason: str = "Customer lost card") -> Dict[str, Any]:
        return card_system.block_card(customer_id, card_type=card_type, card_id=card_id, reason=reason)

card_service = CardService()

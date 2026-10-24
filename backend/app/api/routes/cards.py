from typing import Dict, Any
from ...services.card_service import card_service

def handle_get_cards(user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    cards = card_service.get_cards(cid)
    return {"success": True, "status_code": 200, "data": cards}

def handle_block_card(data: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    card_type = data.get("card_type")
    card_id = data.get("card_id")
    reason = data.get("reason", "Customer requested card block")
    res = card_service.block_card(cid, card_type=card_type, card_id=card_id, reason=reason)
    return {"success": True, "status_code": 200, "data": res}

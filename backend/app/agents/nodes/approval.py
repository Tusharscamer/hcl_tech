from typing import Dict, Any
from ..state import AgentState
from ...utils.logger import logger

HIGH_RISK_INTENTS = {"CARD_SERVICES", "FRAUD_SUPPORT"}

def approval_node(state: AgentState) -> AgentState:
    """
    Evaluates whether an action requires immediate user confirmation
    or administrative Human-in-the-Loop (HITL) authorization under banking policy controls.
    """
    intent = state.intent or ""

    if intent in HIGH_RISK_INTENTS:
        state.requires_confirmation = True
        logger.info(f"[ApprovalNode] Action for intent '{intent}' requires Human-in-the-Loop oversight.")

        if intent == "CARD_SERVICES":
            card_info = state.tool_results.get("card_action_prepared", {})
            state.action_payload = {
                "action": "BLOCK_CARD",
                "card_type": card_info.get("card_type", "DEBIT"),
                "reason": "Customer reported lost card",
                "risk_level": "CRITICAL"
            }

        elif intent == "FRAUD_SUPPORT":
            fraud_data = state.tool_results.get("fraud_check", {})
            state.action_payload = {
                "action": "RAISE_DISPUTE",
                "transaction_id": fraud_data.get("transaction_id", "TXN123456"),
                "amount": fraud_data.get("amount", 14999.0),
                "merchant": fraud_data.get("merchant", "LUXURY_GADGETS_UK"),
                "risk_level": "HIGH"
            }

    return state

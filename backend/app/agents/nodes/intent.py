import re
from typing import Dict, Any
from ..state import AgentState
from ...utils.logger import logger

INTENT_PATTERNS = [
    # Remaining funds inquiry (Section 7)
    (
        "REMAINING_FUNDS",
        r"(after paying.*bills|money.*available after|available.*after.*bills|remaining funds|funds available after|left after bills)",
        0.95
    ),
    # 1. Account, Statement and Balance Inquiry (Use Case 1)
    (
        "ACCOUNT_BALANCE",
        r"(balance|account balance|available balance|how much.*in my account|check balance|ledger|statement|bank statement|account summary|summary of.*statement|account details|mini statement|recent credits and debits|my statement)",
        0.95
    ),
    # 2. Daily Expense Tracking (Use Case 2)
    (
        "EXPENSE_TRACKING",
        r"(spent this month|how much have i spent|expense|spending trends|spending breakdown|expenses|total spend|where did my money go)",
        0.90
    ),
    # 3. Credit Card Assistance (Use Case 3)
    (
        "CREDIT_CARD_ASSISTANCE",
        r"(credit card.*due|credit card.*payment|when is.*credit card|credit limit|minimum due|card due date)",
        0.90
    ),
    # 4. UPI and Payment Assistance (Use Case 4)
    (
        "UPI_PAYMENT_STATUS",
        r"(did my (upi|payment).*go through|payment.*status|upi.*amazon|reference number.*payment|amazon.*upi|payment.*success|transaction status)",
        0.95
    ),
    # 5. EMI and Loan Tracking (Use Case 5)
    (
        "LOAN_EMI_TRACKING",
        r"(next emi|loan details|emi amount|emi schedule|outstanding balance.*loan|how much emi|home loan emi|personal loan emi)",
        0.92
    ),
    # 6. Personal Finance Guidance (Use Case 6)
    (
        "FINANCE_GUIDANCE",
        r"(can i save more|savings observations|how can i save|financial advice|save more this month|savings plan|budget guidance)",
        0.88
    ),
    # 7. Smart Bill Reminder (Use Case 7)
    (
        "BILL_REMINDER",
        r"(payments.*due this week|bills due|upcoming bills|utility bills|due this week|subscription renewals|what bills)",
        0.90
    ),
    # 8. Card Services (Use Case 8)
    (
        "CARD_SERVICES",
        r"(lost my.*card|block.*card|freeze card|debit card.*lost|stolen card|replace card|disable card)",
        0.95
    ),
    # 9. Fraud Support (Use Case 9)
    (
        "FRAUD_SUPPORT",
        r"(do not recognize|unrecognized transaction|suspicious.*transaction|fraud|dispute|scam|fraudulent|unauthorized charge|unfamiliar charge)",
        0.95
    ),
    # 10. Personalized Offers (Use Case 10)
    (
        "PERSONALIZED_OFFERS",
        r"(pre-approved|eligible.*loan|loan eligibility|pre approved loan|special offers|personal loan offer|pre-approved limit)",
        0.92
    ),
    # Bank Policy & RAG FAQ
    (
        "POLICY_INQUIRY",
        r"(policy|turnaround time|rules|charges|grace period|penalty|limit increase|what is the limit|contactless rules)",
        0.80
    )
]

def intent_node(state: AgentState) -> AgentState:
    """
    Classifies the user query intent using pattern-matching & semantic heuristics.
    """
    query_lower = state.user_query.lower()
    detected_intent = None
    max_confidence = 0.5

    for intent, pattern, confidence in INTENT_PATTERNS:
        if re.search(pattern, query_lower):
            detected_intent = intent
            max_confidence = confidence
            break

    # Secondary heuristic fallback
    if not detected_intent:
        if "statement" in query_lower or "summary" in query_lower or "account" in query_lower:
            detected_intent = "ACCOUNT_BALANCE"
            max_confidence = 0.90
        elif "spend" in query_lower or "expense" in query_lower:
            detected_intent = "EXPENSE_TRACKING"
            max_confidence = 0.85
        elif "card" in query_lower and ("lost" in query_lower or "block" in query_lower):
            detected_intent = "CARD_SERVICES"
            max_confidence = 0.90
        elif "fraud" in query_lower or "recognize" in query_lower:
            detected_intent = "FRAUD_SUPPORT"
            max_confidence = 0.90
        else:
            detected_intent = "POLICY_INQUIRY"
            max_confidence = 0.60

    state.intent = detected_intent
    state.confidence = max_confidence
    logger.info(f"[IntentNode] Classified query '{state.user_query}' as {state.intent} (conf: {max_confidence})")
    return state

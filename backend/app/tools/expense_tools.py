from typing import Dict, Any
from ..config.database import db
from ..calculations.expenses import aggregate_expenses_by_category
from ..calculations.obligations import calculate_remaining_funds
from ..banking_systems.core_banking import core_banking
from ..banking_systems.payment_system import payment_system
from ..banking_systems.card_system import card_system
from ..banking_systems.loan_system import loan_system
from ..calculations.balance import calculate_total_balance

def analyze_expenses(customer_id: str, period: str = "current_month") -> Dict[str, Any]:
    """
    Deterministic Tool: Analyzes transactions, categorizes spending, and returns spending trends.
    """
    txns = db.find("transactions", {"customer_id": customer_id})
    analysis = aggregate_expenses_by_category(txns)
    analysis["customer_id"] = customer_id
    analysis["period"] = period
    return analysis

def calculate_remaining_funds_tool(customer_id: str) -> Dict[str, Any]:
    """
    Deterministic Tool: Computes remaining funds = balance - (upcoming EMIs + card dues + bills).
    Directly answers Example Daily Banking Conversation (Section 7 in use case guide).
    """
    accounts = core_banking.get_accounts(customer_id)
    bal_data = calculate_total_balance(accounts)
    available_balance = bal_data["total_available_balance"]

    bills = payment_system.get_upcoming_bills(customer_id)
    cards = card_system.get_credit_cards(customer_id)
    loans = loan_system.get_loans(customer_id)

    res = calculate_remaining_funds(
        available_balance=available_balance,
        upcoming_bills=bills,
        upcoming_emis=loans,
        credit_card_dues=cards
    )
    res["customer_id"] = customer_id
    return res

from typing import Dict, Any, List
from ..banking_systems.core_banking import core_banking
from ..calculations.balance import calculate_total_balance
from ..calculations.obligations import calculate_remaining_funds
from ..banking_systems.payment_system import payment_system
from ..banking_systems.card_system import card_system
from ..banking_systems.loan_system import loan_system

class BankingService:
    @staticmethod
    def get_customer_balance(customer_id: str) -> Dict[str, Any]:
        accounts = core_banking.get_accounts(customer_id)
        return calculate_total_balance(accounts)

    @staticmethod
    def get_remaining_funds_analysis(customer_id: str) -> Dict[str, Any]:
        accounts = core_banking.get_accounts(customer_id)
        bal_data = calculate_total_balance(accounts)
        avail = bal_data["total_available_balance"]

        bills = payment_system.get_upcoming_bills(customer_id)
        cards = card_system.get_credit_cards(customer_id)
        loans = loan_system.get_loans(customer_id)

        return calculate_remaining_funds(avail, bills, loans, cards)

banking_service = BankingService()

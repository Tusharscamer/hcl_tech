from typing import Dict, Any
from ..banking_systems.core_banking import core_banking
from ..calculations.balance import calculate_total_balance

def get_balance(customer_id: str) -> Dict[str, Any]:
    """
    Deterministic Tool: Retrieves available and ledger balance for customer.
    """
    accounts = core_banking.get_accounts(customer_id)
    if not accounts:
        return {
            "found": False,
            "message": "No active banking accounts found for this customer."
        }
    
    calc = calculate_total_balance(accounts)
    primary = core_banking.get_primary_account(customer_id)
    
    return {
        "found": True,
        "customer_id": customer_id,
        "primary_account": primary.get("account_number") if primary else None,
        "available_balance": calc["total_available_balance"],
        "ledger_balance": calc["total_ledger_balance"],
        "accounts": calc["accounts"],
        "currency": "INR"
    }

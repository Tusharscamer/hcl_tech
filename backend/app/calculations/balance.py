from typing import List, Dict, Any

def calculate_total_balance(accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes total available and ledger balances across customer accounts.
    """
    total_available = 0.0
    total_ledger = 0.0
    summary = []

    for acc in accounts:
        if acc.get("status") == "ACTIVE":
            avail = float(acc.get("available_balance", 0.0))
            ledger = float(acc.get("ledger_balance", 0.0))
            total_available += avail
            total_ledger += ledger
            summary.append({
                "account_number": acc.get("account_number"),
                "account_type": acc.get("account_type"),
                "available_balance": avail,
                "ledger_balance": ledger,
                "is_primary": acc.get("is_primary", False)
            })

    return {
        "total_available_balance": total_available,
        "total_ledger_balance": total_ledger,
        "accounts_count": len(summary),
        "accounts": summary
    }

def check_funds_availability(available_balance: float, required_amount: float) -> bool:
    """
    Deterministic check if funds are sufficient.
    """
    return available_balance >= required_amount

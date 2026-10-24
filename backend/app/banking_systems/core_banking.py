from typing import List, Dict, Any, Optional
from ..config.database import db
from ..utils.logger import logger

class CoreBankingSystem:
    """
    Simulates Core Banking System (CBS) for account servicing and ledger inquiries.
    """
    @staticmethod
    def get_accounts(customer_id: str) -> List[Dict[str, Any]]:
        accounts = db.find("accounts", {"customer_id": customer_id})
        logger.info(f"[CoreBankingSystem] Retrieved {len(accounts)} accounts for customer {customer_id}")
        return accounts

    @staticmethod
    def get_primary_account(customer_id: str) -> Optional[Dict[str, Any]]:
        acc = db.find_one("accounts", {"customer_id": customer_id, "is_primary": True})
        if not acc:
            accounts = db.find("accounts", {"customer_id": customer_id})
            return accounts[0] if accounts else None
        return acc

    @staticmethod
    def get_account_by_number(account_number: str) -> Optional[Dict[str, Any]]:
        return db.find_one("accounts", {"account_number": account_number})

    @staticmethod
    def update_balance(account_number: str, new_balance: float) -> bool:
        return db.update_one("accounts", {"account_number": account_number}, {"available_balance": new_balance})

core_banking = CoreBankingSystem()

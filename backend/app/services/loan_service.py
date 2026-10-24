from typing import Dict, Any, List
from ..banking_systems.loan_system import loan_system

class LoanService:
    @staticmethod
    def get_loans(customer_id: str) -> List[Dict[str, Any]]:
        return loan_system.get_loans(customer_id)

    @staticmethod
    def get_eligibility(customer_id: str) -> Dict[str, Any]:
        return loan_system.evaluate_loan_eligibility(customer_id)

loan_service = LoanService()

from typing import Dict, Any
from ..banking_systems.loan_system import loan_system

def check_loan_eligibility(customer_id: str) -> Dict[str, Any]:
    """
    Deterministic Tool: Assesses pre-approved credit and loan eligibility based on bank policy rules.
    """
    return loan_system.evaluate_loan_eligibility(customer_id)

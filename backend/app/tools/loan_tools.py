from typing import Dict, Any
from ..banking_systems.loan_system import loan_system
from ..calculations.emi import generate_amortization_schedule

def get_loan_details(customer_id: str) -> Dict[str, Any]:
    """
    Deterministic Tool: Retrieves active loans, next EMI amount, due date and balance.
    """
    loans = loan_system.get_loans(customer_id)
    if not loans:
        return {
            "found": False,
            "message": "No active loans found for this customer."
        }
    
    primary_loan = loans[0]
    return {
        "found": True,
        "customer_id": customer_id,
        "loan_id": primary_loan.get("loan_id"),
        "loan_type": primary_loan.get("loan_type"),
        "sanctioned_amount": primary_loan.get("sanctioned_amount"),
        "outstanding_balance": primary_loan.get("outstanding_balance"),
        "interest_rate": primary_loan.get("interest_rate"),
        "next_emi_amount": primary_loan.get("emi_amount"),
        "next_emi_date": primary_loan.get("next_emi_date"),
        "remaining_tenure_months": primary_loan.get("remaining_tenure_months"),
        "all_loans": loans
    }

def get_emi_schedule(customer_id: str, loan_id: str) -> Dict[str, Any]:
    """
    Deterministic Tool: Computes month-by-month EMI amortization schedule.
    """
    loan = loan_system.get_loan_by_id(loan_id)
    if not loan:
        return {"found": False, "message": f"Loan {loan_id} not found."}
    
    schedule = generate_amortization_schedule(
        principal=loan["outstanding_balance"],
        annual_interest_rate=loan["interest_rate"],
        tenure_months=loan["remaining_tenure_months"],
        limit_months=6
    )
    return {
        "found": True,
        "loan_id": loan_id,
        "schedule": schedule
    }

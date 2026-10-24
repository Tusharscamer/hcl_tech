from typing import List, Dict, Any, Optional
from ..config.database import db
from ..utils.logger import logger

class LoanSystem:
    """
    Loan Management System (LMS) for EMIs, amortizations, and pre-approvals.
    """
    @staticmethod
    def get_loans(customer_id: str) -> List[Dict[str, Any]]:
        loans = db.find("loans", {"customer_id": customer_id})
        logger.info(f"[LoanSystem] Found {len(loans)} active loans for customer {customer_id}")
        return loans

    @staticmethod
    def get_loan_by_id(loan_id: str) -> Optional[Dict[str, Any]]:
        return db.find_one("loans", {"loan_id": loan_id})

    @staticmethod
    def evaluate_loan_eligibility(customer_id: str) -> Dict[str, Any]:
        user = db.find_one("users", {"customer_id": customer_id})
        if not user:
            return {"eligible": False, "reason": "Customer record not found"}

        score = user.get("credit_score", 0)
        income = user.get("monthly_income", 0.0)

        # Approved Bank Policy Rules:
        # 1. Credit score >= 720
        # 2. Monthly income >= INR 25,000
        is_eligible = score >= 720 and income >= 25000
        max_amount = round(income * 15, 2) if is_eligible else 0.0

        offers = db.find("offers", {"customer_id": customer_id, "status": "AVAILABLE"})

        return {
            "eligible": is_eligible,
            "credit_score": score,
            "monthly_income": income,
            "max_eligible_amount": max_amount,
            "interest_rate": 9.99 if score >= 750 else 11.25,
            "pre_approved_offers": offers,
            "reason": "Meets credit score and monthly income benchmarks" if is_eligible else "Does not meet score/income guidelines"
        }

loan_system = LoanSystem()

from typing import List, Dict, Any

def calculate_remaining_funds(
    available_balance: float,
    upcoming_bills: List[Dict[str, Any]],
    upcoming_emis: List[Dict[str, Any]],
    credit_card_dues: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Deterministic calculation of remaining funds after all upcoming obligations.
    Remaining = Available Balance - Total Obligations.
    """
    obligations = []
    total_obligations = 0.0

    # 1. EMIs
    for loan in upcoming_emis:
        emi = float(loan.get("emi_amount", 0.0))
        total_obligations += emi
        obligations.append({
            "type": "LOAN_EMI",
            "title": f"{loan.get('loan_type', 'Loan')} EMI",
            "due_date": loan.get("next_emi_date"),
            "amount": emi,
            "id": loan.get("loan_id")
        })

    # 2. Credit Card Dues
    for card in credit_card_dues:
        due = float(card.get("total_due", 0.0))
        if due > 0:
            total_obligations += due
            obligations.append({
                "type": "CREDIT_CARD_DUE",
                "title": f"Credit Card ({card.get('card_number', '****')}) Bill",
                "due_date": card.get("statement_due_date"),
                "amount": due,
                "id": card.get("card_id")
            })

    # 3. Scheduled Utility / Subscription Bills
    for bill in upcoming_bills:
        amt = float(bill.get("amount", 0.0))
        # avoid double-counting if bill was credit card / emi
        if bill.get("category") not in ("CREDIT_CARD", "LOAN_EMI"):
            total_obligations += amt
            obligations.append({
                "type": bill.get("category", "BILL"),
                "title": bill.get("biller_name", "Bill"),
                "due_date": bill.get("due_date"),
                "amount": amt,
                "id": bill.get("bill_id")
            })

    remaining_funds = round(available_balance - total_obligations, 2)

    explanation = (
        f"Your available balance is ₹{available_balance:,.2f}. "
        f"Upcoming obligations total ₹{total_obligations:,.2f}, "
        f"leaving an estimated ₹{remaining_funds:,.2f}."
    )

    return {
        "available_balance": available_balance,
        "total_obligations": total_obligations,
        "estimated_remaining_funds": remaining_funds,
        "obligations_count": len(obligations),
        "obligations": obligations,
        "explanation": explanation
    }

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.tools.account_tools import get_balance
from app.tools.transaction_tools import get_transactions
from app.tools.expense_tools import analyze_expenses, calculate_remaining_funds_tool
from app.tools.payment_tools import get_payment_status, get_upcoming_payments
from app.tools.card_tools import get_credit_card_details
from app.tools.loan_tools import get_loan_details
from app.tools.fraud_tools import fraud_verification
from app.tools.offer_tools import check_loan_eligibility

def test_account_tools():
    res = get_balance("C1001")
    assert res["found"] is True
    assert res["available_balance"] >= 125000.0
    print("test_account_tools passed")

def test_transaction_tools():
    res = get_transactions("C1001")
    assert res["total_records"] > 0
    assert len(res["transactions"]) > 0
    print("test_transaction_tools passed")

def test_expense_tools():
    res = analyze_expenses("C1001")
    assert res["total_spent"] > 0
    assert len(res["category_breakdown"]) > 0
    print("test_expense_tools passed")

def test_remaining_funds_tool():
    res = calculate_remaining_funds_tool("C1001")
    assert res["available_balance"] >= 125000.0
    assert res["total_obligations"] > 0
    assert res["estimated_remaining_funds"] == res["available_balance"] - res["total_obligations"]
    print("test_remaining_funds_tool passed")

def test_payment_tools():
    # Test looking for Amazon payment
    res = get_payment_status("C1001", query="Amazon")
    assert res["found"] is True
    assert "Amazon" in res["merchant"]
    assert res["status"] == "COMPLETED"

    # Test upcoming payments
    upcoming = get_upcoming_payments("C1001")
    assert upcoming["count"] > 0
    print("test_payment_tools passed")

def test_card_and_loan_tools():
    card = get_credit_card_details("C1001")
    assert card["found"] is True
    assert card["statement_due_date"] is not None

    loan = get_loan_details("C1001")
    assert loan["found"] is True
    assert loan["next_emi_amount"] > 0
    print("test_card_and_loan_tools passed")

def test_fraud_and_offer_tools():
    # Suspicious transaction TXN123456
    fraud = fraud_verification("TXN123456", customer_id="C1001")
    assert fraud["found"] is True
    assert fraud["is_suspicious"] is True
    assert fraud["risk_score"] >= 60

    elig = check_loan_eligibility("C1001")
    assert elig["eligible"] is True
    assert elig["max_eligible_amount"] > 0
    print("test_fraud_and_offer_tools passed")

if __name__ == "__main__":
    test_account_tools()
    test_transaction_tools()
    test_expense_tools()
    test_remaining_funds_tool()
    test_payment_tools()
    test_card_and_loan_tools()
    test_fraud_and_offer_tools()
    print("All banking tools tests PASSED!")

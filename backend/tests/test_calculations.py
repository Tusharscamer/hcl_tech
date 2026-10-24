import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.calculations.balance import calculate_total_balance, check_funds_availability
from app.calculations.emi import calculate_emi, generate_amortization_schedule
from app.calculations.expenses import aggregate_expenses_by_category
from app.calculations.obligations import calculate_remaining_funds

def test_balance_calculation():
    accounts = [
        {"account_number": "ACC1", "available_balance": 100000.0, "ledger_balance": 100000.0, "status": "ACTIVE"},
        {"account_number": "ACC2", "available_balance": 25000.0, "ledger_balance": 25000.0, "status": "ACTIVE"}
    ]
    res = calculate_total_balance(accounts)
    assert res["total_available_balance"] == 125000.0
    assert res["accounts_count"] == 2
    assert check_funds_availability(125000.0, 50000.0) is True
    assert check_funds_availability(125000.0, 150000.0) is False
    print("test_balance_calculation passed")

def test_emi_calculation():
    # 25 Lakhs at 8.45% for 240 months
    emi = calculate_emi(2500000.0, 8.45, 240)
    assert emi > 20000.0 and emi < 23000.0
    schedule = generate_amortization_schedule(2500000.0, 8.45, 240, limit_months=3)
    assert len(schedule) == 3
    assert schedule[0]["month"] == 1
    print("test_emi_calculation passed")

def test_remaining_funds_calculation():
    available = 125000.0
    bills = [{"bill_id": "B1", "category": "UTILITIES", "amount": 5000.0, "due_date": "2026-10-30"}]
    emis = [{"loan_id": "L1", "loan_type": "HOME_LOAN", "emi_amount": 20000.0, "next_emi_date": "2026-11-05"}]
    cards = [{"card_id": "C1", "card_number": "8821", "total_due": 10000.0, "statement_due_date": "2026-11-05"}]

    res = calculate_remaining_funds(available, bills, emis, cards)
    assert res["total_obligations"] == 35000.0
    assert res["estimated_remaining_funds"] == 90000.0
    assert "₹125,000" in res["explanation"] or "125,000" in res["explanation"]
    print("test_remaining_funds_calculation passed")

def test_expense_aggregation():
    txns = [
        {"type": "DEBIT", "category": "Food", "merchant": "Swiggy", "amount": 8500.0, "status": "COMPLETED"},
        {"type": "DEBIT", "category": "Transport", "merchant": "Uber", "amount": 3200.0, "status": "COMPLETED"},
        {"type": "DEBIT", "category": "Shopping", "merchant": "Amazon", "amount": 12000.0, "status": "COMPLETED"},
        {"type": "DEBIT", "category": "Bills", "merchant": "BESCOM", "amount": 4500.0, "status": "COMPLETED"}
    ]
    res = aggregate_expenses_by_category(txns)
    assert res["total_spent"] == 28200.0
    cats = {c["category"]: c["amount"] for c in res["category_breakdown"]}
    assert cats["Food"] == 8500.0
    assert cats["Transport"] == 3200.0
    assert cats["Shopping"] == 12000.0
    assert cats["Bills"] == 4500.0
    print("test_expense_aggregation passed")

if __name__ == "__main__":
    test_balance_calculation()
    test_emi_calculation()
    test_remaining_funds_calculation()
    test_expense_aggregation()
    print("All calculation tests PASSED!")

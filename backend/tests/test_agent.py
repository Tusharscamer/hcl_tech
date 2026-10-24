import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.agents.graph import agent_graph

def test_10_daily_banking_use_cases():
    test_cases = [
        ("What is my current account balance?", "ACCOUNT_BALANCE", ["get_balance"]),
        ("How much have I spent this month?", "EXPENSE_TRACKING", ["analyze_expenses"]),
        ("When is my credit card payment due?", "CREDIT_CARD_ASSISTANCE", ["get_credit_card_details"]),
        ("Did my UPI payment to Amazon go through?", "UPI_PAYMENT_STATUS", ["get_payment_status"]),
        ("What is my next EMI amount?", "LOAN_EMI_TRACKING", ["get_loan_details"]),
        ("Can I save more this month?", "FINANCE_GUIDANCE", ["analyze_expenses"]),
        ("What payments are due this week?", "BILL_REMINDER", ["get_upcoming_payments"]),
        ("I lost my debit card.", "CARD_SERVICES", ["block_card"]),
        ("I do not recognize this transaction.", "FRAUD_SUPPORT", ["fraud_verification"]),
        ("Am I eligible for a pre-approved loan?", "PERSONALIZED_OFFERS", ["check_loan_eligibility"]),
        ("How much money do I have available after paying all upcoming bills?", "REMAINING_FUNDS", ["get_balance"])
    ]

    for query, expected_intent, expected_tools in test_cases:
        state = agent_graph.run(query, customer_id="C1001")
        assert state.intent == expected_intent, f"Query '{query}' expected {expected_intent}, got {state.intent}"
        for tool in expected_tools:
            assert tool in state.tools_invoked, f"Query '{query}' expected tool {tool} in {state.tools_invoked}"
        assert state.answer is not None and len(state.answer) > 0
        assert state.trace_id.startswith("BANK-")
        print(f"PASS: [{state.intent}] '{query}' -> Trace: {state.trace_id}")

    print("\nALL 10+ USE CASES PASSED ACCORDING TO SPECIFICATION!")

if __name__ == "__main__":
    test_10_daily_banking_use_cases()

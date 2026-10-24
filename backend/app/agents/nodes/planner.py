from ..state import AgentState
from ...utils.logger import logger

def planner_node(state: AgentState) -> AgentState:
    """
    Formulates a deterministic execution plan and identifies tools to invoke.
    """
    intent = state.intent or "POLICY_INQUIRY"
    tools = []
    systems = []
    plan_steps = []

    if intent == "REMAINING_FUNDS":
        tools = ["get_balance", "get_upcoming_payments"]
        systems = ["Core Banking System", "Payment / UPI System", "Credit Card System", "Loan Management System"]
        plan_steps = [
            "1. Retrieve real-time available balance from Core Banking",
            "2. Fetch upcoming bills, credit card dues, and loan EMIs",
            "3. Deterministically compute remaining funds = balance - obligations",
            "4. Formulate explainable response with breakdown"
        ]

    elif intent == "ACCOUNT_BALANCE":
        tools = ["get_balance", "get_transactions"]
        systems = ["Core Banking System"]
        plan_steps = [
            "1. Query Core Banking for available and ledger balance",
            "2. Retrieve recent credits and debits summary",
            "3. Format clean account overview"
        ]

    elif intent == "EXPENSE_TRACKING":
        tools = ["analyze_expenses"]
        systems = ["Core Banking System", "Transaction Analytics Engine"]
        plan_steps = [
            "1. Aggregate monthly debits across categories",
            "2. Compute category proportions and top spending areas",
            "3. Generate structured chart breakdown"
        ]

    elif intent == "CREDIT_CARD_ASSISTANCE":
        tools = ["get_credit_card_details"]
        systems = ["Credit Card System"]
        plan_steps = [
            "1. Fetch credit card statement and billing cycle data",
            "2. Check due date, minimum due and total outstanding",
            "3. Present repayment options"
        ]

    elif intent == "UPI_PAYMENT_STATUS":
        tools = ["get_payment_status"]
        systems = ["Payment / UPI System"]
        plan_steps = [
            "1. Query UPI switch for merchant and reference matching query",
            "2. Verify transaction status and reference number",
            "3. Provide confirmation or turnaround reversal guidance"
        ]

    elif intent == "LOAN_EMI_TRACKING":
        tools = ["get_loan_details"]
        systems = ["Loan Management System"]
        plan_steps = [
            "1. Retrieve active loan accounts and outstanding principal",
            "2. Fetch next EMI due date and installment amount",
            "3. Provide EMI schedule summary"
        ]

    elif intent == "FINANCE_GUIDANCE":
        tools = ["analyze_expenses", "get_balance", "get_upcoming_payments"]
        systems = ["Core Banking System", "Financial Planning Engine"]
        plan_steps = [
            "1. Analyze income vs spending patterns",
            "2. Check upcoming obligations buffer",
            "3. Provide non-binding, actionable savings observations"
        ]

    elif intent == "BILL_REMINDER":
        tools = ["get_upcoming_payments"]
        systems = ["Payment / UPI System", "Bill Desk"]
        plan_steps = [
            "1. Retrieve utility bills, EMIs, and subscriptions due this cycle",
            "2. Sort by nearest due date",
            "3. Highlight auto-pay status and total due"
        ]

    elif intent == "CARD_SERVICES":
        tools = ["block_card"]
        systems = ["Credit Card System", "Core Banking Card Switch"]
        state.requires_confirmation = True
        state.action_type = "BLOCK_CARD"
        plan_steps = [
            "1. Identify active debit/credit card for customer",
            "2. Request security confirmation / trigger instant card lock",
            "3. Initiate replacement card dispatch under bank controls"
        ]

    elif intent == "FRAUD_SUPPORT":
        tools = ["fraud_verification", "raise_dispute"]
        systems = ["Fraud Monitoring System", "Dispute Resolution Center"]
        state.requires_confirmation = True
        state.action_type = "RAISE_DISPUTE"
        plan_steps = [
            "1. Locate transaction from query (or latest flagged transaction)",
            "2. Run automated fraud verification risk scoring",
            "3. Safeguard account and open dispute workflow for Human Review"
        ]

    elif intent == "PERSONALIZED_OFFERS":
        tools = ["check_loan_eligibility"]
        systems = ["CRM / Offer Engine", "Loan Management System"]
        plan_steps = [
            "1. Check customer credit score and salary benchmarks",
            "2. Evaluate pre-approved loan & credit limit rules",
            "3. Present personalized loan offers"
        ]

    else:
        # Policy inquiry & RAG
        tools = ["retrieve_policy_context"]
        systems = ["Knowledge / RAG Layer (Banking Policies & FAQs)"]
        plan_steps = [
            "1. Embed user query into vector space",
            "2. Retrieve relevant policy clauses from indexed PDFs",
            "3. Synthesize factual response grounded in policy"
        ]

    state.tools_to_invoke = tools
    state.systems_queried = systems
    state.plan = plan_steps
    logger.info(f"[PlannerNode] Formulated plan: {len(tools)} tools, {len(systems)} systems.")
    return state

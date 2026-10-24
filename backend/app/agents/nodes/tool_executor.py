import re
from typing import Dict, Any
from ..state import AgentState
from ...tools.account_tools import get_balance
from ...tools.transaction_tools import get_transactions
from ...tools.expense_tools import analyze_expenses, calculate_remaining_funds_tool
from ...tools.payment_tools import get_payment_status, get_upcoming_payments
from ...tools.card_tools import get_credit_card_details, block_card
from ...tools.loan_tools import get_loan_details, get_emi_schedule
from ...tools.fraud_tools import fraud_verification, raise_dispute
from ...tools.offer_tools import check_loan_eligibility
from ...rag.retriever import retrieve_policy_context
from ...utils.logger import logger

def tool_executor_node(state: AgentState) -> AgentState:
    """
    Executes the planned banking tools deterministically using live authorized customer context.
    """
    cid = state.customer_id
    query = state.user_query
    results = {}
    invoked = []

    for tool_name in state.tools_to_invoke:
        logger.info(f"[ToolExecutorNode] Executing deterministic tool: {tool_name} for customer: {cid}")
        try:
            if tool_name == "get_balance":
                res = get_balance(cid)
                results["balance"] = res
                invoked.append("get_balance")

            elif tool_name == "get_transactions":
                res = get_transactions(cid, limit=5)
                results["transactions"] = res
                invoked.append("get_transactions")

            elif tool_name == "analyze_expenses":
                res = analyze_expenses(cid, period="current_month")
                results["expenses"] = res
                invoked.append("analyze_expenses")

            elif tool_name == "get_payment_status":
                # Extract merchant or keyword from query
                query_kw = None
                if "amazon" in query.lower():
                    query_kw = "Amazon"
                elif "swiggy" in query.lower():
                    query_kw = "Swiggy"
                elif "zara" in query.lower():
                    query_kw = "Zara"

                # Check if explicit transaction ID like TXN... or UPI... is mentioned
                match = re.search(r"(TXN\w+|UPI\w+)", query, re.IGNORECASE)
                ref = match.group(1) if match else None

                res = get_payment_status(cid, query=query_kw, reference_number=ref)
                results["payment_status"] = res
                invoked.append("get_payment_status")

            elif tool_name == "get_upcoming_payments":
                res = get_upcoming_payments(cid)
                results["upcoming_payments"] = res
                invoked.append("get_upcoming_payments")

            elif tool_name == "get_credit_card_details":
                res = get_credit_card_details(cid)
                results["credit_card"] = res
                invoked.append("get_credit_card_details")

            elif tool_name == "get_loan_details":
                res = get_loan_details(cid)
                results["loan"] = res
                invoked.append("get_loan_details")

            elif tool_name == "block_card":
                # For safety check: if requires confirmation, prepare payload
                card_type = "DEBIT" if "debit" in query.lower() else "CREDIT" if "credit" in query.lower() else "DEBIT"
                results["card_action_prepared"] = {
                    "card_type": card_type,
                    "action": "BLOCK_CARD"
                }
                # Also execute soft lock preview
                invoked.append("block_card")

            elif tool_name == "fraud_verification":
                # Find transaction ID mentioned or default to latest flagged
                match = re.search(r"(TXN\w+)", query, re.IGNORECASE)
                txn_id = match.group(1) if match else "TXN123456"
                res = fraud_verification(txn_id, customer_id=cid)
                results["fraud_check"] = res
                invoked.append("fraud_verification")

            elif tool_name == "raise_dispute":
                match = re.search(r"(TXN\w+)", query, re.IGNORECASE)
                txn_id = match.group(1) if match else "TXN123456"
                results["dispute_action_prepared"] = {
                    "transaction_id": txn_id,
                    "action": "RAISE_DISPUTE"
                }
                invoked.append("raise_dispute")

            elif tool_name == "check_loan_eligibility":
                res = check_loan_eligibility(cid)
                results["eligibility"] = res
                invoked.append("check_loan_eligibility")

            elif tool_name in ("retrieve_policy_context", "retrieve_policy_tool"):
                rag_res = retrieve_policy_context(query)
                results["rag"] = rag_res
                state.rag_context = rag_res.get("context_text")
                invoked.append("retrieve_policy_tool")

        except Exception as e:
            logger.error(f"[ToolExecutorNode] Error executing {tool_name}: {e}")
            results[tool_name] = {"error": str(e)}

    # If this is a remaining funds inquiry, run remaining funds calculation
    if state.intent == "REMAINING_FUNDS":
        calc_res = calculate_remaining_funds_tool(cid)
        results["remaining_funds"] = calc_res
        if "calculate_remaining_funds" not in invoked:
            invoked.append("calculate_remaining_funds")

    state.tool_results = results
    state.tools_invoked = invoked
    return state

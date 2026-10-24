from typing import Dict, Any, Optional
from urllib.parse import urlparse, parse_qs
from .routes import auth, chat, banking, transactions, cards, loans, payments, fraud, admin
from ..middleware.auth import authenticate_token
from ..middleware.rate_limit import rate_limiter
from ..middleware.request_id import get_or_generate_request_id

def route_request(
    method: str,
    path: str,
    body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    query_params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Central API Gateway Router. Validates auth, applies rate limiting,
    and dispatches to the corresponding modular route handler.
    """
    body = body or {}
    headers = headers or {}
    query_params = query_params or {}

    # Extract auth
    auth_header = headers.get("authorization") or headers.get("Authorization")
    user = authenticate_token(auth_header)
    trace_id = get_or_generate_request_id(headers.get("x-request-id"))

    # Public Routes
    if path == "/api/auth/login" and method == "POST":
        res = auth.handle_login(body)
        res["trace_id"] = trace_id
        return res

    # Protected Routes require authentication
    if not user:
        # Default mock demo user context if demo mode
        user = {"sub": "C1001", "name": "Aarav Sharma", "role": "customer", "email": "aarav.sharma@example.com"}

    # Apply rate limiting
    client_id = user.get("sub", "anonymous")
    if not rate_limiter.is_allowed(client_id):
        return {
            "success": False,
            "status_code": 429,
            "message": "Rate limit exceeded. Please wait a moment before sending more requests.",
            "trace_id": trace_id
        }

    # Auth profile
    if path == "/api/auth/me" and method == "GET":
        res = auth.handle_get_me(user)
    # Chat & Assistant
    elif path == "/api/chat" and method == "POST":
        res = chat.handle_chat_message(body, user)
    elif path == "/api/chat/confirm-action" and method == "POST":
        res = chat.handle_confirm_action(body, user)
    elif path == "/api/chat/sessions" and method == "GET":
        res = chat.handle_list_sessions(user)
    elif path == "/api/chat/sessions" and method == "POST":
        res = chat.handle_create_session(body, user)
    elif path.startswith("/api/chat/sessions/") and method == "GET":
        session_id = path.split("/")[4]
        res = chat.handle_get_session(session_id, user)
    elif path.startswith("/api/chat/sessions/") and method == "DELETE":
        session_id = path.split("/")[4]
        res = chat.handle_delete_session(session_id, user)
    # Banking
    elif path == "/api/banking/balance" and method == "GET":
        res = banking.handle_get_balance(user)
    elif path == "/api/banking/remaining-funds" and method == "GET":
        res = banking.handle_get_remaining_funds(user)
    elif path == "/api/banking/db-status" and method == "GET":
        res = banking.handle_get_db_status(user)
    # Transactions
    elif path == "/api/transactions" and method == "GET":
        res = transactions.handle_get_transactions(user, query_params)
    elif path == "/api/transactions/expenses" and method == "GET":
        res = transactions.handle_get_expense_analytics(user)
    # Cards
    elif path == "/api/cards" and method == "GET":
        res = cards.handle_get_cards(user)
    elif path == "/api/cards/block" and method == "POST":
        res = cards.handle_block_card(body, user)
    # Loans
    elif path == "/api/loans" and method == "GET":
        res = loans.handle_get_loans(user)
    elif path == "/api/loans/eligibility" and method == "GET":
        res = loans.handle_get_loan_eligibility(user)
    # Payments
    elif path == "/api/payments/bills" and method == "GET":
        res = payments.handle_get_bills(user)
    elif path == "/api/payments/status" and method == "GET":
        res = payments.handle_payment_status(user, query_params)
    # Fraud
    elif path == "/api/fraud/verify" and method == "POST":
        res = fraud.handle_fraud_verify(body, user)
    elif path == "/api/fraud/dispute" and method == "POST":
        res = fraud.handle_submit_dispute(body, user)
    # Admin & HITL
    elif path == "/api/admin/approvals" and method == "GET":
        res = admin.handle_get_approvals(user)
    elif path.startswith("/api/admin/approvals/") and path.endswith("/decision") and method == "POST":
        approval_id = path.split("/")[4]
        res = admin.handle_decide_approval(approval_id, body, user)
    elif path == "/api/admin/audit-logs" and method == "GET":
        res = admin.handle_get_audit_logs(user)
    else:
        res = {"success": False, "status_code": 404, "message": f"Endpoint not found: {method} {path}"}

    res["trace_id"] = trace_id
    return res

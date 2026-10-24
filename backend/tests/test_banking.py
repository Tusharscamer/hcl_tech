import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.api.router import route_request

def test_api_endpoints():
    # 1. Login
    login_res = route_request("POST", "/api/auth/login", {"username_or_id": "C1001", "password": "password123"})
    assert login_res["success"] is True
    token = login_res["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Balance endpoint
    bal_res = route_request("GET", "/api/banking/balance", headers=headers)
    assert bal_res["success"] is True
    assert bal_res["data"]["total_available_balance"] >= 125000.0

    # 3. Remaining funds endpoint
    rem_res = route_request("GET", "/api/banking/remaining-funds", headers=headers)
    assert rem_res["success"] is True
    assert rem_res["data"]["estimated_remaining_funds"] > 0

    # 4. Transactions endpoint
    txn_res = route_request("GET", "/api/transactions", headers=headers)
    assert txn_res["success"] is True
    assert len(txn_res["data"]) > 0

    # 5. Cards endpoint
    crd_res = route_request("GET", "/api/cards", headers=headers)
    assert crd_res["success"] is True
    assert len(crd_res["data"]) > 0

    # 6. Loans endpoint
    loan_res = route_request("GET", "/api/loans", headers=headers)
    assert loan_res["success"] is True
    assert len(loan_res["data"]) > 0

    # 7. Chat endpoint
    chat_res = route_request("POST", "/api/chat", {"message": "What is my current account balance?"}, headers=headers)
    assert chat_res["success"] is True
    assert chat_res["data"]["trace_id"].startswith("BANK-")
    assert "ACC100123456" in chat_res["data"]["answer"] or "available balance" in chat_res["data"]["answer"]

    # 8. Admin approvals endpoint
    admin_login = route_request("POST", "/api/auth/login", {"username_or_id": "A9001", "password": "admin123"})
    admin_token = admin_login["data"]["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    appr_res = route_request("GET", "/api/admin/approvals", headers=admin_headers)
    assert appr_res["success"] is True

    audit_res = route_request("GET", "/api/admin/audit-logs", headers=admin_headers)
    assert audit_res["success"] is True
    assert len(audit_res["data"]) > 0

    print("test_api_endpoints passed")

if __name__ == "__main__":
    test_api_endpoints()
    print("All banking API tests PASSED!")

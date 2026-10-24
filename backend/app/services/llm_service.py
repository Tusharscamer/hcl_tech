import json
import urllib.request
from typing import Dict, Any, Optional, List
from ..config.settings import settings
from ..utils.logger import logger

class LLMService:
    """
    AI Generation Service utilizing Google Gemini API.
    Combines verified deterministic banking tool outputs with dynamic LLM generation.
    """
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        # Fast, low-latency models supported by Google API
        self.candidate_models = ["gemini-flash-lite-latest", "gemma-4-26b-a4b-it"]

    def generate_response(
        self,
        user_query: str,
        intent: str,
        tool_results: Dict[str, Any],
        customer_info: Dict[str, Any],
        rag_context: Optional[str] = None,
        chat_history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Calls Gemini AI API to synthesize a personalized, conversational, and query-specific response.
        """
        if not self.api_key:
            return {
                "generated": False,
                "text": None,
                "model": "offline"
            }

        # Format deterministic banking facts concisely for the LLM
        facts = []
        cust_name = customer_info.get("name", "Customer")
        facts.append(f"Customer Name: {cust_name}")

        if "balance" in tool_results:
            b = tool_results["balance"]
            facts.append(f"Primary Account: {b.get('primary_account', 'ACC100123456')}")
            facts.append(f"Available Balance: ₹{b.get('available_balance', 0):,.2f}")
            facts.append(f"Ledger Balance: ₹{b.get('ledger_balance', 0):,.2f}")

        if "transactions" in tool_results:
            t = tool_results["transactions"]
            facts.append(f"Recent Total Credits: ₹{t.get('total_credits', 0):,.2f}")
            facts.append(f"Recent Total Debits: ₹{t.get('total_debits', 0):,.2f}")
            recent_items = [f"{txn.get('merchant')}: ₹{txn.get('amount')}" for txn in t.get("transactions", [])[:4]]
            facts.append(f"Recent Transactions: {', '.join(recent_items)}")

        if "remaining_funds" in tool_results:
            rf = tool_results["remaining_funds"]
            facts.append(f"Upcoming Obligations Total: ₹{rf.get('total_obligations', 0):,.2f}")
            facts.append(f"Estimated Remaining Funds After Bills: ₹{rf.get('estimated_remaining_funds', 0):,.2f}")

        if "expenses" in tool_results:
            exp = tool_results["expenses"]
            facts.append(f"Total Spent This Month: ₹{exp.get('total_spent', 0):,.2f}")
            breakdown = [f"{c['category']}: ₹{c['amount']:,.0f}" for c in exp.get("category_breakdown", [])[:4]]
            facts.append(f"Spending Breakdown: {', '.join(breakdown)}")

        if "credit_card" in tool_results:
            c = tool_results["credit_card"]
            facts.append(f"Credit Card ({c.get('card_number', '****')}): Due on {c.get('statement_due_date')}, Total Due: ₹{c.get('total_due', 0):,.2f}, Min Due: ₹{c.get('minimum_due', 0):,.2f}, Available Limit: ₹{c.get('available_limit', 0):,.2f}")

        if "payment_status" in tool_results:
            p = tool_results["payment_status"]
            facts.append(f"Payment Record: Merchant: {p.get('merchant')}, Amount: ₹{p.get('amount')}, Status: {p.get('status')}, Reference: {p.get('reference_number')}")

        if "loan" in tool_results:
            l = tool_results["loan"]
            facts.append(f"Active Loan: Type: {l.get('loan_type')}, Next EMI: ₹{l.get('next_emi_amount')}, Due Date: {l.get('next_emi_date')}, Outstanding: ₹{l.get('outstanding_balance')}")

        if "upcoming_payments" in tool_results:
            up = tool_results["upcoming_payments"]
            bills = [f"{b.get('biller_name')} (₹{b.get('amount')}, Due: {b.get('due_date')})" for b in up.get("upcoming_bills", [])[:3]]
            facts.append(f"Upcoming Bills ({len(up.get('upcoming_bills', []))}): {', '.join(bills)}, Total: ₹{up.get('total_amount_due')}")

        if "fraud_check" in tool_results:
            fc = tool_results["fraud_check"]
            facts.append(f"Fraud Check: TXN {fc.get('transaction_id')}, Merchant: {fc.get('merchant')}, Amount: ₹{fc.get('amount')}, Suspicious: {fc.get('is_suspicious')}, Risk Score: {fc.get('risk_score')}/100")

        if "eligibility" in tool_results:
            el = tool_results["eligibility"]
            facts.append(f"Loan Eligibility: Pre-Approved: {el.get('eligible')}, Max Amount: ₹{el.get('max_eligible_amount')}, Rate: {el.get('interest_rate')}% p.a.")

        if rag_context:
            facts.append(f"Bank Policy Clauses: {rag_context[:300]}")

        verified_data_block = "\n".join(facts)

        history_block = ""
        if chat_history:
            recent_turns = []
            for h in chat_history[-4:]:
                s_label = "Customer" if h.get("sender") == "user" else "Assistant"
                t_val = h.get("text", "")
                if t_val:
                    recent_turns.append(f"{s_label}: {t_val}")
            if recent_turns:
                history_block = f"Recent Conversation Context:\n" + "\n".join(recent_turns) + "\n\n"

        prompt = (
            "You are Apex Bank's official AI Daily Banking Assistant.\n"
            "Provide a direct, natural, conversational answer to the customer based strictly on the verified data below.\n"
            "Address specifically and directly what the user is asking. Maintain conversational context if they are referencing previous turns.\n"
            "Do not hallucinate numbers or fabricate balances.\n"
            "Keep the response concise (1 to 3 sentences), friendly, and professional.\n\n"
            f"{history_block}"
            f"Verified Core Banking Data:\n{verified_data_block}\n\n"
            f"Customer Query: \"{user_query}\"\n"
            "Assistant Answer:"
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 300
            }
        }

        # Try models in priority order
        for model in self.candidate_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"
            try:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
                with urllib.request.urlopen(req, timeout=8) as response:
                    res_data = json.load(response)
                    candidates = res_data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            ans = parts[0].get("text", "").strip()
                            logger.info(f"[LLMService] Generated response via {model}: {ans[:60]}...")
                            return {
                                "generated": True,
                                "text": ans,
                                "model": model
                            }
            except Exception as e:
                logger.warning(f"[LLMService] Model {model} call failed: {e}. Trying next...")

        return {
            "generated": False,
            "text": None,
            "model": "offline"
        }

llm_service = LLMService()

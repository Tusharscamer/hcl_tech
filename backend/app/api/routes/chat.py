from typing import Dict, Any, List
from ...agents.graph import agent_graph
from ...tools.card_tools import block_card
from ...tools.fraud_tools import raise_dispute
from ...services.chat_session_service import chat_session_service

def handle_chat_message(data: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    message = data.get("message", "")
    customer_id = user.get("sub") or user.get("customer_id", "C1001")
    req_session_id = data.get("session_id")

    if not message.strip():
        return {"success": False, "status_code": 400, "message": "Message cannot be empty."}

    # Ensure a valid session exists
    if not req_session_id or req_session_id == "default":
        session = chat_session_service.get_or_create_default_session(customer_id)
        session_id = session["session_id"]
    else:
        session = chat_session_service.get_session(req_session_id, customer_id)
        if not session:
            session = chat_session_service.create_session(customer_id, title="Banking Chat")
        session_id = session["session_id"]

    # 1. Persist user message to chat history
    chat_session_service.save_user_message(session_id, customer_id, message)

    # 2. Retrieve recent history for conversational memory
    recent_history = chat_session_service.get_session_messages(session_id, customer_id, limit=6)

    # 3. Execute LangGraph Pipeline
    state = agent_graph.run(
        user_query=message,
        customer_id=customer_id,
        session_id=session_id,
        chat_history=recent_history
    )

    # 4. Persist assistant reply to chat history
    chat_session_service.save_assistant_message(
        session_id=session_id,
        customer_id=customer_id,
        text=state.answer or "I have processed your banking query.",
        answer_type=state.answer_type,
        tools_invoked=state.tools_invoked,
        systems_queried=state.systems_queried,
        requires_confirmation=state.requires_confirmation,
        action_type=state.action_type,
        action_payload=state.action_payload,
        structured_data=state.structured_data,
        trace_id=state.trace_id
    )

    response_payload = {
        "session_id": session_id,
        "trace_id": state.trace_id,
        "answer": state.answer,
        "answer_type": state.answer_type,
        "tools_invoked": state.tools_invoked,
        "systems_queried": state.systems_queried,
        "requires_confirmation": state.requires_confirmation,
        "action_type": state.action_type,
        "action_payload": state.action_payload,
        "structured_data": state.structured_data,
        "latency_ms": state.latency_ms
    }

    return {
        "success": True,
        "status_code": 200,
        "data": response_payload
    }

def handle_list_sessions(user: Dict[str, Any]) -> Dict[str, Any]:
    customer_id = user.get("sub") or user.get("customer_id", "C1001")
    sessions = chat_session_service.list_sessions(customer_id)
    if not sessions:
        # Create an initial default session
        default_session = chat_session_service.create_session(customer_id, title="Daily Banking Chat")
        sessions = [default_session]

    return {
        "success": True,
        "status_code": 200,
        "data": sessions
    }

def handle_create_session(data: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    customer_id = user.get("sub") or user.get("customer_id", "C1001")
    title = data.get("title") or "New Banking Conversation"
    new_session = chat_session_service.create_session(customer_id, title=title)
    messages = chat_session_service.get_session_messages(new_session["session_id"], customer_id)

    return {
        "success": True,
        "status_code": 201,
        "data": {
            "session": new_session,
            "messages": messages
        }
    }

def handle_get_session(session_id: str, user: Dict[str, Any]) -> Dict[str, Any]:
    customer_id = user.get("sub") or user.get("customer_id", "C1001")
    session = chat_session_service.get_session(session_id, customer_id)
    if not session:
        return {"success": False, "status_code": 404, "message": "Session not found."}

    messages = chat_session_service.get_session_messages(session_id, customer_id)
    return {
        "success": True,
        "status_code": 200,
        "data": {
            "session": session,
            "messages": messages
        }
    }

def handle_delete_session(session_id: str, user: Dict[str, Any]) -> Dict[str, Any]:
    customer_id = user.get("sub") or user.get("customer_id", "C1001")
    deleted = chat_session_service.delete_session(session_id, customer_id)
    return {
        "success": True,
        "status_code": 200,
        "data": {"deleted": deleted, "session_id": session_id}
    }

def handle_confirm_action(data: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    action_type = data.get("action_type")
    payload = data.get("action_payload", {})
    confirmed = data.get("confirmed", True)
    customer_id = user.get("sub") or user.get("customer_id", "C1001")
    session_id = data.get("session_id")

    if not confirmed:
        return {
            "success": True,
            "status_code": 200,
            "data": {
                "message": "Action was cancelled by customer.",
                "status": "CANCELLED"
            }
        }

    res_data = {}
    if action_type == "BLOCK_CARD":
        card_type = payload.get("card_type", "DEBIT")
        res_data = block_card(customer_id=customer_id, card_type=card_type)

    elif action_type == "RAISE_DISPUTE":
        txn_id = payload.get("transaction_id", "TXN123456")
        reason = payload.get("reason", "Customer flagged unrecognized transaction")
        res_data = raise_dispute(customer_id=customer_id, transaction_id=txn_id, reason=reason)
    else:
        return {"success": False, "status_code": 400, "message": f"Unsupported action type: {action_type}"}

    # If session_id provided, also save action confirmation message to history
    if session_id:
        chat_session_service.save_assistant_message(
            session_id=session_id,
            customer_id=customer_id,
            text=res_data.get("message", "Action completed."),
            answer_type="action_completed",
            tools_invoked=[action_type.lower()],
            systems_queried=["Core Banking Security"],
            trace_id=res_data.get("reference_id") or "CONFIRMED"
        )

    return {"success": True, "status_code": 200, "data": res_data}

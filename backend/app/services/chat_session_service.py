import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from ..config.database import db
from ..utils.logger import logger

class ChatSessionService:
    """
    Manages multi-turn conversation sessions and message history.
    Stores and retrieves sessions from MongoDB Atlas (or local seed mirror).
    """

    @staticmethod
    def get_or_create_default_session(customer_id: str) -> Dict[str, Any]:
        """
        Retrieves the most recent active session for the customer,
        or creates a new session if none exists.
        """
        sessions = db.find("chat_sessions", {"customer_id": customer_id})
        if sessions:
            # Sort by updated_at descending
            sessions.sort(key=lambda x: x.get("updated_at", x.get("created_at", "")), reverse=True)
            return sessions[0]

        return ChatSessionService.create_session(customer_id, title="Daily Banking Chat")

    @staticmethod
    def create_session(customer_id: str, title: Optional[str] = None) -> Dict[str, Any]:
        """
        Creates a new chat session with a welcome message.
        """
        session_id = f"SES-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(timezone.utc).isoformat()
        session_title = title or "New Banking Conversation"

        session_doc = {
            "session_id": session_id,
            "customer_id": customer_id,
            "title": session_title,
            "message_count": 0,
            "created_at": now,
            "updated_at": now
        }
        db.insert_one("chat_sessions", session_doc)

        # Insert initial welcome greeting message
        welcome_msg = {
            "message_id": f"msg-{uuid.uuid4().hex[:8]}",
            "session_id": session_id,
            "customer_id": customer_id,
            "sender": "assistant",
            "text": "Hello! I am your AI Daily Banking Assistant. I can help you check balances, calculate safe-to-spend funds, analyze spending trends, track upcoming EMI and utility bills, block cards, or dispute suspicious transactions.",
            "answer_type": "conversational",
            "tools_invoked": [],
            "systems_queried": ["Knowledge / Core Banking"],
            "requires_confirmation": False,
            "action_type": None,
            "action_payload": None,
            "structured_data": None,
            "trace_id": "INIT-GREETING",
            "created_at": now
        }
        db.insert_one("chat_messages", welcome_msg)

        logger.info(f"[ChatSessionService] Created session {session_id} for customer {customer_id}")
        return session_doc

    @staticmethod
    def list_sessions(customer_id: str) -> List[Dict[str, Any]]:
        """
        Lists all conversation sessions for a customer, sorted newest first.
        """
        sessions = db.find("chat_sessions", {"customer_id": customer_id})
        sessions.sort(key=lambda x: x.get("updated_at", x.get("created_at", "")), reverse=True)
        return sessions

    @staticmethod
    def get_session(session_id: str, customer_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetches session details.
        """
        return db.find_one("chat_sessions", {"session_id": session_id, "customer_id": customer_id})

    @staticmethod
    def get_session_messages(session_id: str, customer_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieves all messages for a given session sorted chronologically.
        """
        messages = db.find("chat_messages", {"session_id": session_id, "customer_id": customer_id})
        messages.sort(key=lambda x: x.get("created_at", ""))
        return messages[-limit:] if limit > 0 else messages

    @staticmethod
    def save_user_message(session_id: str, customer_id: str, text: str) -> Dict[str, Any]:
        """
        Persists a user message and updates session metadata.
        """
        now = datetime.now(timezone.utc).isoformat()
        msg_id = f"msg-{uuid.uuid4().hex[:8]}"
        doc = {
            "message_id": msg_id,
            "session_id": session_id,
            "customer_id": customer_id,
            "sender": "user",
            "text": text,
            "created_at": now
        }
        db.insert_one("chat_messages", doc)

        # Update session title if first query and still default
        session = db.find_one("chat_sessions", {"session_id": session_id, "customer_id": customer_id})
        update_data = {
            "updated_at": now
        }
        if session:
            count = session.get("message_count", 0) + 1
            update_data["message_count"] = count
            if session.get("title") in ("New Banking Conversation", "Daily Banking Chat", None):
                # Use clean summary title from user query
                clean_title = text[:40].strip()
                if len(text) > 40:
                    clean_title += "..."
                update_data["title"] = clean_title

            db.update_one("chat_sessions", {"session_id": session_id, "customer_id": customer_id}, update_data)

        return doc

    @staticmethod
    def save_assistant_message(
        session_id: str,
        customer_id: str,
        text: str,
        answer_type: str = "conversational",
        tools_invoked: Optional[List[str]] = None,
        systems_queried: Optional[List[str]] = None,
        requires_confirmation: bool = False,
        action_type: Optional[str] = None,
        action_payload: Optional[Dict[str, Any]] = None,
        structured_data: Optional[Dict[str, Any]] = None,
        trace_id: str = "DEFAULT"
    ) -> Dict[str, Any]:
        """
        Persists the assistant's response to the database.
        """
        now = datetime.now(timezone.utc).isoformat()
        msg_id = f"msg-{uuid.uuid4().hex[:8]}"
        doc = {
            "message_id": msg_id,
            "session_id": session_id,
            "customer_id": customer_id,
            "sender": "assistant",
            "text": text,
            "answer_type": answer_type,
            "tools_invoked": tools_invoked or [],
            "systems_queried": systems_queried or [],
            "requires_confirmation": requires_confirmation,
            "action_type": action_type,
            "action_payload": action_payload,
            "structured_data": structured_data,
            "trace_id": trace_id,
            "created_at": now
        }
        db.insert_one("chat_messages", doc)

        # Increment message count and touch updated_at
        session = db.find_one("chat_sessions", {"session_id": session_id, "customer_id": customer_id})
        if session:
            count = session.get("message_count", 0) + 1
            db.update_one(
                "chat_sessions",
                {"session_id": session_id, "customer_id": customer_id},
                {"updated_at": now, "message_count": count}
            )

        return doc

    @staticmethod
    def delete_session(session_id: str, customer_id: str) -> bool:
        """
        Deletes a session and all its messages.
        """
        db.delete_many("chat_messages", {"session_id": session_id, "customer_id": customer_id})
        deleted = db.delete_one("chat_sessions", {"session_id": session_id, "customer_id": customer_id})
        logger.info(f"[ChatSessionService] Deleted session {session_id} for customer {customer_id}")
        return deleted

chat_session_service = ChatSessionService()

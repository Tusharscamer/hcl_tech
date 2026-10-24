import time
from typing import Dict, Any
from .state import AgentState
from .nodes.intent import intent_node
from .nodes.planner import planner_node
from .nodes.tool_executor import tool_executor_node
from .nodes.approval import approval_node
from .nodes.response import response_node
from ..services.audit_service import audit_service
from ..utils.trace import generate_trace_id
from ..utils.logger import logger

class BankingAgentGraph:
    """
    LangGraph-style State Graph Orchestrator for Daily Banking Assistant.
    Follows Intent -> Planning -> Tool Execution -> Approval/Oversight -> Response Generation.
    """
    def __init__(self):
        self.nodes = [
            ("intent", intent_node),
            ("planner", planner_node),
            ("tool_executor", tool_executor_node),
            ("approval", approval_node),
            ("response", response_node)
        ]

    def run(self, user_query: str, customer_id: str, session_id: str = "default", chat_history: Any = None) -> AgentState:
        start_time = time.time()
        trace_id = generate_trace_id("BANK")

        state = AgentState(
            trace_id=trace_id,
            customer_id=customer_id,
            session_id=session_id,
            user_query=user_query,
            chat_history=chat_history or []
        )

        logger.info(f"[Graph] Starting execution pipeline for Trace: {trace_id} | Customer: {customer_id}")

        for node_name, node_func in self.nodes:
            try:
                state = node_func(state)
            except Exception as e:
                logger.error(f"[Graph] Error in node {node_name}: {e}")
                state.error = str(e)
                state.status = "FAILED"
                break

        latency_ms = (time.time() - start_time) * 1000.0
        state.latency_ms = latency_ms

        # Audit and Observability Layer Logging (Requirement R8)
        audit_service.log_interaction(
            trace_id=state.trace_id,
            customer_id=state.customer_id,
            user_query=state.user_query,
            tools_invoked=state.tools_invoked,
            systems_queried=state.systems_queried,
            intent=state.intent or "UNKNOWN",
            decision_reasoning=f"Planned {len(state.tools_to_invoke)} tools across systems: {', '.join(state.systems_queried)}",
            action_outcome=state.answer_type,
            latency_ms=latency_ms,
            status=state.status,
            error_message=state.error
        )

        return state

agent_graph = BankingAgentGraph()

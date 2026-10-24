import time
from typing import Dict, Any, Optional
from langgraph.graph import StateGraph, START, END
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
    Official LangGraph Orchestrator for Daily Banking Assistant.
    Follows: START -> intent -> planner -> tool_executor -> approval -> response -> END
    """
    def __init__(self):
        logger.info("[LangGraph] Building LangGraph StateGraph orchestrator...")
        self.workflow = StateGraph(AgentState)

        # Add Core Orchestration Nodes
        self.workflow.add_node("intent", intent_node)
        self.workflow.add_node("planner", planner_node)
        self.workflow.add_node("tool_executor", tool_executor_node)
        self.workflow.add_node("approval", approval_node)
        self.workflow.add_node("response", response_node)

        # Connect Graph Edges
        self.workflow.add_edge(START, "intent")
        self.workflow.add_edge("intent", "planner")
        self.workflow.add_edge("planner", "tool_executor")
        self.workflow.add_edge("tool_executor", "approval")
        self.workflow.add_edge("approval", "response")
        self.workflow.add_edge("response", END)

        # Compile the LangGraph Application
        self.graph = self.workflow.compile()
        logger.info("[LangGraph] Successfully compiled official LangGraph StateGraph pipeline.")

    def run(
        self,
        user_query: str,
        customer_id: str,
        session_id: str = "default",
        chat_history: Optional[Any] = None
    ) -> AgentState:
        """
        Executes user query through compiled LangGraph state machine.
        """
        start_time = time.time()
        trace_id = generate_trace_id("BANK")

        initial_state = AgentState(
            trace_id=trace_id,
            customer_id=customer_id,
            session_id=session_id,
            user_query=user_query,
            chat_history=chat_history or []
        )

        logger.info(f"[LangGraph] Invoking StateGraph for Trace: {trace_id} | Customer: {customer_id}")

        try:
            raw_output = self.graph.invoke(initial_state)

            if isinstance(raw_output, dict):
                final_state = AgentState(**raw_output)
            elif isinstance(raw_output, AgentState):
                final_state = raw_output
            else:
                final_state = initial_state
                final_state.error = f"Unexpected output type from LangGraph: {type(raw_output)}"
        except Exception as e:
            logger.error(f"[LangGraph] Pipeline execution failed: {e}")
            final_state = initial_state
            final_state.error = str(e)
            final_state.status = "FAILED"

        latency_ms = (time.time() - start_time) * 1000.0
        final_state.latency_ms = latency_ms

        # Audit and Observability Layer Logging (Requirement R8)
        audit_service.log_interaction(
            trace_id=final_state.trace_id,
            customer_id=final_state.customer_id,
            user_query=final_state.user_query,
            tools_invoked=final_state.tools_invoked,
            systems_queried=final_state.systems_queried,
            intent=final_state.intent or "UNKNOWN",
            decision_reasoning=f"LangGraph planned {len(final_state.tools_to_invoke)} tools across systems: {', '.join(final_state.systems_queried)}",
            action_outcome=final_state.answer_type,
            latency_ms=latency_ms,
            status=final_state.status,
            error_message=final_state.error
        )

        return final_state

# Global compiled orchestrator instance
agent_graph = BankingAgentGraph()

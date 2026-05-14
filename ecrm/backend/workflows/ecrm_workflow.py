"""
LangGraph agentic workflow for eCRM.

Nodes:
  input_node → classify_node → retrieve_node → respond_node → priority_node → log_node
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END

from backend.agents.classifier import classify_query
from backend.agents.priority import assign_priority
from backend.agents.retriever import retrieve_context
from backend.agents.responder import generate_response
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class TicketState(TypedDict):
    message: str
    customer_id: str
    category: str
    priority: str
    context: str
    response: str
    logs: list


def input_node(state: TicketState) -> TicketState:
    logger.info(f"[input_node] Processing query from {state['customer_id']}")
    state["logs"].append("Input received.")
    return state


def classify_node(state: TicketState) -> TicketState:
    state["category"] = classify_query(state["message"])
    state["logs"].append(f"Classified: {state['category']}")
    return state


def retrieve_node(state: TicketState) -> TicketState:
    state["context"] = retrieve_context(state["message"], state["category"])
    state["logs"].append("Context retrieved.")
    return state


def respond_node(state: TicketState) -> TicketState:
    state["response"] = generate_response(
        state["message"], state["category"],
        state["priority"], state["context"]
    )
    state["logs"].append("Response generated.")
    return state


def priority_node(state: TicketState) -> TicketState:
    state["priority"] = assign_priority(state["message"], state["category"])
    state["logs"].append(f"Priority: {state['priority']}")
    return state


def log_node(state: TicketState) -> TicketState:
    logger.info(f"[log_node] Workflow complete: {state['logs']}")
    state["logs"].append("Workflow complete.")
    return state


def build_workflow():
    graph = StateGraph(TicketState)
    graph.add_node("input", input_node)
    graph.add_node("classify", classify_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("priority", priority_node)
    graph.add_node("respond", respond_node)
    graph.add_node("log", log_node)

    graph.set_entry_point("input")
    graph.add_edge("input", "classify")
    graph.add_edge("classify", "retrieve")
    graph.add_edge("retrieve", "priority")
    graph.add_edge("priority", "respond")
    graph.add_edge("respond", "log")
    graph.add_edge("log", END)

    return graph.compile()


workflow = build_workflow()


def run_workflow(message: str, customer_id: str) -> TicketState:
    initial_state: TicketState = {
        "message": message,
        "customer_id": customer_id,
        "category": "",
        "priority": "",
        "context": "",
        "response": "",
        "logs": []
    }
    return workflow.invoke(initial_state)

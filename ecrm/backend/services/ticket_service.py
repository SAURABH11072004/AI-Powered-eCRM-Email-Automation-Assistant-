import uuid
from datetime import datetime

from backend.workflows.ecrm_workflow import run_workflow
from backend.database.mongo import save_ticket, get_tickets_by_customer
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


def process_query(customer_id: str, message: str) -> dict:
    """Run the full agentic workflow and persist the ticket."""
    result = run_workflow(message=message, customer_id=customer_id)

    ticket = {
        "ticket_id": str(uuid.uuid4()),
        "customer_id": customer_id,
        "message": message,
        "category": result["category"],
        "priority": result["priority"],
        "response": result["response"],
        "logs": result["logs"],
        "timestamp": datetime.utcnow().isoformat()
    }

    save_ticket(ticket)
    logger.info(f"Ticket saved: {ticket['ticket_id']}")
    return ticket


def get_history(customer_id: str) -> list:
    return get_tickets_by_customer(customer_id)

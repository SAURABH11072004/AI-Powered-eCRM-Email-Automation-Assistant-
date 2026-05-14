from pymongo import MongoClient
from backend.utils.config import MONGODB_URI, MONGODB_DB
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

try:
    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=3000)
    db = client[MONGODB_DB]
    tickets_col = db["tickets"]
    logger.info("MongoDB connected.")
except Exception as e:
    logger.warning(f"MongoDB not available: {e}. Using in-memory fallback.")
    db = None
    tickets_col = None

# In-memory fallback for demo / testing
_memory_store: list = []

def save_ticket(data: dict) -> str:
    if tickets_col is not None:
        result = tickets_col.insert_one(data)
        return str(result.inserted_id)
    else:
        _memory_store.append(data)
        return data.get("ticket_id", "local")

def get_tickets_by_customer(customer_id: str) -> list:
    if tickets_col is not None:
        docs = list(tickets_col.find({"customer_id": customer_id}, {"_id": 0}))
        return docs
    return [t for t in _memory_store if t.get("customer_id") == customer_id]

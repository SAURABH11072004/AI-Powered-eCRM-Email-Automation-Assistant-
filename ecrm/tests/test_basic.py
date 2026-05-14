"""
Simple tests that work without real API keys (uses mock data).
Run: pytest tests/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.agents.retriever import FALLBACK_CONTEXT


def test_fallback_context_keys():
    expected = {"Billing", "Technical Support", "Account Issues", "Order Tracking", "General Inquiry"}
    assert set(FALLBACK_CONTEXT.keys()) == expected


def test_fallback_context_not_empty():
    for v in FALLBACK_CONTEXT.values():
        assert len(v) > 10


def test_db_memory_fallback():
    from backend.database.mongo import _memory_store, save_ticket, get_tickets_by_customer
    save_ticket({"customer_id": "TEST001", "ticket_id": "t1", "message": "hello"})
    results = get_tickets_by_customer("TEST001")
    # May be from memory store if Mongo is offline
    assert isinstance(results, list)

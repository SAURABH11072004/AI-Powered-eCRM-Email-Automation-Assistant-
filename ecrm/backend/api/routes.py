from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.ticket_service import process_query, get_history

router = APIRouter()


class QueryRequest(BaseModel):
    customer_id: str
    message: str


@router.get("/health")
def health():
    return {"status": "ok", "service": "eCRM Email Automation Assistant"}


@router.post("/query")
def submit_query(req: QueryRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    ticket = process_query(customer_id=req.customer_id, message=req.message)
    return ticket


@router.get("/history/{customer_id}")
def customer_history(customer_id: str):
    history = get_history(customer_id)
    return {"customer_id": customer_id, "tickets": history}

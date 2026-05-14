from backend.utils.config import PINECONE_API_KEY, PINECONE_INDEX
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

_pinecone_ready = False
_index = None

if PINECONE_API_KEY:
    try:
        from pinecone import Pinecone
        from openai import OpenAI
        from backend.utils.config import OPENAI_API_KEY

        pc = Pinecone(api_key=PINECONE_API_KEY)
        _index = pc.Index(PINECONE_INDEX)
        _oai = OpenAI(api_key=OPENAI_API_KEY)
        _pinecone_ready = True
        logger.info("Pinecone connected.")
    except Exception as e:
        logger.warning(f"Pinecone not available: {e}")

# Fallback FAQ knowledge base
FALLBACK_CONTEXT = {
    "Billing": "Common billing issues include incorrect charges, subscription renewals, and refund requests. Refunds typically take 5-7 business days.",
    "Technical Support": "Common technical issues include login errors, app crashes, and slow performance. Try clearing cache or reinstalling the app.",
    "Account Issues": "Account issues include forgotten passwords, locked accounts, and profile updates. Use the 'Forgot Password' link to reset.",
    "Order Tracking": "Orders usually ship within 2-3 business days. Use your order ID to track at our tracking portal.",
    "General Inquiry": "For general questions, please refer to our FAQ page or contact support at support@company.com.",
}

def retrieve_context(message: str, category: str) -> str:
    """Retrieve relevant context from Pinecone or fallback knowledge base."""
    if _pinecone_ready and _index:
        try:
            embedding = _oai.embeddings.create(
                input=message, model="text-embedding-ada-002"
            ).data[0].embedding
            results = _index.query(vector=embedding, top_k=3, include_metadata=True)
            texts = [m["metadata"].get("text", "") for m in results.get("matches", []) if m.get("score", 0) > 0.7]
            if texts:
                return " ".join(texts)
        except Exception as e:
            logger.warning(f"Pinecone retrieval error: {e}")
    # Fallback
    return FALLBACK_CONTEXT.get(category, "No specific context available.")

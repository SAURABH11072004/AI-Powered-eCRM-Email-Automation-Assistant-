from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY
from backend.prompts.templates import CLASSIFY_PROMPT
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

VALID_CATEGORIES = [
    "Billing", "Technical Support", "Account Issues",
    "Order Tracking", "General Inquiry"
]

def classify_query(message: str) -> str:
    """Classify customer message into a support category."""
    prompt = CLASSIFY_PROMPT.format(message=message)
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20,
            temperature=0
        )
        category = resp.choices[0].message.content.strip()
        if category not in VALID_CATEGORIES:
            category = "General Inquiry"
        logger.info(f"Classified as: {category}")
        return category
    except Exception as e:
        logger.error(f"Classification error: {e}")
        return "General Inquiry"

from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY
from backend.prompts.templates import PRIORITY_PROMPT
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

def assign_priority(message: str, category: str) -> str:
    """Assign High / Medium / Low priority to a ticket."""
    prompt = PRIORITY_PROMPT.format(message=message, category=category)
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0
        )
        priority = resp.choices[0].message.content.strip()
        if priority not in ["High", "Medium", "Low"]:
            priority = "Medium"
        logger.info(f"Priority assigned: {priority}")
        return priority
    except Exception as e:
        logger.error(f"Priority error: {e}")
        return "Medium"

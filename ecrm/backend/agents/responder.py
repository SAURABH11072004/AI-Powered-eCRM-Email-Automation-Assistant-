from openai import OpenAI
from backend.utils.config import OPENAI_API_KEY
from backend.prompts.templates import RESPONSE_PROMPT
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_response(message: str, category: str, priority: str, context: str) -> str:
    """Generate a professional support response."""
    prompt = RESPONSE_PROMPT.format(
        message=message, category=category,
        priority=priority, context=context
    )
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7
        )
        reply = resp.choices[0].message.content.strip()
        logger.info("Response generated.")
        return reply
    except Exception as e:
        logger.error(f"Response generation error: {e}")
        return "Thank you for contacting us. Our team will get back to you shortly."

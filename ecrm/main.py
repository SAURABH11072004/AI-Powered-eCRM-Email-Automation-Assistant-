from fastapi import FastAPI
from backend.api.routes import router
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(title="AI-Powered eCRM Email Automation Assistant", version="1.0.0")
app.include_router(router)

@app.on_event("startup")
async def startup():
    logger.info("eCRM Assistant started.")

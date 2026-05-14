import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY   = os.getenv("OPENAI_API_KEY", "")
MONGODB_URI      = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB       = os.getenv("MONGODB_DB", "ecrm_db")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
PINECONE_INDEX   = os.getenv("PINECONE_INDEX", "ecrm-index")

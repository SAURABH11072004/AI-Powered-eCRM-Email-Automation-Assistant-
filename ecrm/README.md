# AI-Powered eCRM Email Automation Assistant

A production-style AI customer support automation system using **LangGraph**, **LangChain**, **OpenAI**, **FastAPI**, and **MongoDB**.

---

## Features
- AI query classification (Billing, Technical Support, etc.)
- Automatic priority assignment (High / Medium / Low)
- Context retrieval via Pinecone (with fallback knowledge base)
- AI response generation using GPT-3.5-turbo
- Agentic multi-step workflow with LangGraph
- REST API with FastAPI
- Clean HTML/JS frontend
- MongoDB persistence (in-memory fallback for demo)

---

## Project Structure
```
AI-Powered-eCRM-Email-Automation-Assistant/
├── backend/
│   ├── agents/         # classifier, priority, retriever, responder
│   ├── workflows/      # LangGraph workflow
│   ├── database/       # MongoDB connection
│   ├── api/            # FastAPI routes
│   ├── prompts/        # Prompt templates
│   ├── utils/          # Logger, config
│   └── services/       # Ticket service
├── frontend/           # HTML UI
├── tests/              # Basic tests
├── .env.example
├── requirements.txt
├── app.py
└── main.py
```

---

## Setup

### 1. Clone & install
```bash
git clone <your-repo>
cd AI-Powered-eCRM-Email-Automation-Assistant
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in your API keys in .env
```

### 3. Run the server
```bash
python app.py
```
API available at: `http://localhost:8000`

### 4. Open the frontend
Open `frontend/index.html` in your browser.

---

## API Endpoints

### Health check
```
GET /health
```

### Submit a customer query
```
POST /query
Content-Type: application/json

{
  "customer_id": "CUST001",
  "message": "My payment failed but I was charged twice!"
}
```

### Get customer history
```
GET /history/CUST001
```

---

## LangGraph Workflow
```
Input → Classify → Retrieve Context → Assign Priority → Generate Response → Log
```

---

## Tech Stack
| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, Python |
| AI/LLM | OpenAI GPT-3.5, LangChain, LangGraph |
| Vector DB | Pinecone |
| Database | MongoDB (in-memory fallback) |
| Frontend | HTML/CSS/JavaScript |

---

## Notes
- Works without Pinecone/MongoDB (uses fallback in-memory store)
- Requires `OPENAI_API_KEY` in `.env` for live responses
- Run `pytest tests/` for basic tests

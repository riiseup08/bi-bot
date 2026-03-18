from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import json, os
from typing import Optional
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION — set via Railway environment variables
# ─────────────────────────────────────────────────────────────────────────────
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_BASE_URL = "https://api.minimax.io/v1"
MODEL_NAME = os.getenv("MODEL_NAME", "MiniMax-Text-01")

SYSTEM_PROMPT = """
You are a senior data analyst with 10+ years of experience,
specializing in Power BI, DAX, Power Query (M language), data
modeling, and business intelligence. You are also proficient in
SQL, Excel, Python (pandas, matplotlib), and ETL processes.

Your role is to assist as a personal BI advisor:
- Help design and optimize Power BI reports and dashboards
- Write and explain DAX formulas and measures
- Debug and optimize Power Query (M) transformations
- Advise on data modeling best practices (star schema, relationships)
- Review and improve SQL queries for BI use cases
- Suggest visualizations that best communicate the data story
- Explain BI concepts clearly, from beginner to advanced level

Always be direct, practical, and professional. Give concrete
examples, code snippets, and step-by-step guidance when relevant.
"""

# ─────────────────────────────────────────────────────────────────────────────
# APP INIT
# ─────────────────────────────────────────────────────────────────────────────
app = FastAPI(title="MiniMax FastAPI Bot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory conversation store
conversation_store: dict = {}

# ─────────────────────────────────────────────────────────────────────────────
# MINIMAX CLIENT
# ─────────────────────────────────────────────────────────────────────────────
def get_client():
    if not MINIMAX_API_KEY:
        raise HTTPException(status_code=500, detail="MINIMAX_API_KEY not set. Add it in Railway environment variables.")
    return OpenAI(api_key=MINIMAX_API_KEY, base_url=MINIMAX_BASE_URL)

# ─────────────────────────────────────────────────────────────────────────────
# SCHEMAS
# ─────────────────────────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"
    stream: Optional[bool] = False

class ChatResponse(BaseModel):
    session_id: str
    message: str
    model: str
    timestamp: str

class ClearRequest(BaseModel):
    session_id: Optional[str] = "default"

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def get_history(session_id: str) -> list:
    if session_id not in conversation_store:
        conversation_store[session_id] = []
    return conversation_store[session_id]

def build_messages(history: list) -> list:
    """Build full message list with system prompt prepended."""
    return [{"role": "system", "content": SYSTEM_PROMPT}] + history

# ─────────────────────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def root():
    with open(os.path.join("static", "index.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model": MODEL_NAME,
        "api_key_set": bool(MINIMAX_API_KEY),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id or "default"
    history    = get_history(session_id)
    client     = get_client()

    history.append({"role": "user", "content": req.message})

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=build_messages(history),
            max_tokens=1000,
            temperature=0.3,
        )
        assistant_msg = response.choices[0].message.content
        history.append({"role": "assistant", "content": assistant_msg})

        return ChatResponse(
            session_id=session_id,
            message=assistant_msg,
            model=MODEL_NAME,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        history.pop()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat/stream")
async def chat_stream(req: ChatRequest):
    session_id = req.session_id or "default"
    history    = get_history(session_id)
    client     = get_client()

    history.append({"role": "user", "content": req.message})

    async def token_generator():
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model=MODEL_NAME,
                messages=build_messages(history),
                max_tokens=1000,
                temperature=0.3,
                stream=True,
            )
            for chunk in stream:
                token = chunk.choices[0].delta.content or ""
                if token:
                    full_response += token
                    yield f"data: {json.dumps({'token': token})}\n\n"

            history.append({"role": "assistant", "content": full_response})
            yield f"data: {json.dumps({'done': True, 'model': MODEL_NAME})}\n\n"

        except Exception as e:
            history.pop()
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )

@app.get("/history/{session_id}")
async def get_conversation_history(session_id: str):
    history = get_history(session_id)
    return {"session_id": session_id, "message_count": len(history), "messages": history}

@app.post("/clear")
async def clear_history(req: ClearRequest):
    session_id = req.session_id or "default"
    conversation_store[session_id] = []
    return {"status": "cleared", "session_id": session_id}

@app.get("/sessions")
async def list_sessions():
    return {
        "sessions": [
            {"session_id": sid, "message_count": len(msgs)}
            for sid, msgs in conversation_store.items()
        ]
    }

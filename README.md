# BI Bot 📊

A conversational **Business Intelligence assistant** powered by [Groq](https://groq.com/) and served with [FastAPI](https://fastapi.tiangolo.com/). Ask questions about Power BI, DAX, Power Query (M), SQL, data modeling, and Python analytics — and get expert answers in real time.

---

## Features

- 🤖 **Senior BI Analyst persona** — 10+ years of expertise baked into the system prompt
- ⚡ **Streaming responses** — server-sent events (SSE) so answers appear token-by-token
- 💬 **Multi-session memory** — each browser tab gets its own conversation history
- 🎨 **Dark-mode chat UI** — built-in frontend served directly from the API
- 🔌 **REST API** — easily integrate with your own front-end or tooling
- 🚀 **Railway-ready** — one-click deploy with the included `railway.json` and `Procfile`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.10+, FastAPI, Uvicorn |
| LLM Provider | [Groq](https://console.groq.com/) |
| Default Model | `llama-3.3-70b-versatile` |
| Frontend | Vanilla HTML/CSS/JS (served as a static file) |
| Deployment | Railway (Nixpacks builder) |

---

## Quick Start (local)

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/keys)

### 1. Clone the repository

```bash
git clone https://github.com/riiseup08/bi-bot.git
cd bi-bot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

```bash
export GROQ_API_KEY="your_groq_api_key_here"
# Optional — override the default model
export MODEL_NAME="llama-3.3-70b-versatile"
```

### 4. Run the server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Open your browser at **http://localhost:8000** to start chatting.

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | — | Your Groq API key |
| `MODEL_NAME` | No | `llama-3.3-70b-versatile` | Groq model to use |

---

## Available Models

| Model | Notes |
|-------|-------|
| `llama-3.3-70b-versatile` | Best quality — **recommended** |
| `llama-3.1-8b-instant` | Fastest, lightest |
| `mixtral-8x7b-32768` | Long context (32 k tokens) |
| `gemma2-9b-it` | Google Gemma 2 |

---

## API Reference

### `GET /`
Serves the chat UI.

### `GET /health`
Returns service status, current model, and whether the API key is set.

```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile",
  "provider": "Groq",
  "api_key_set": true,
  "timestamp": "2024-01-01T00:00:00"
}
```

### `POST /chat`
Send a message and receive a complete response.

**Request body:**
```json
{
  "message": "Write a DAX measure for YoY growth",
  "session_id": "my-session",
  "stream": false
}
```

**Response:**
```json
{
  "session_id": "my-session",
  "message": "...",
  "model": "llama-3.3-70b-versatile",
  "timestamp": "2024-01-01T00:00:00"
}
```

### `POST /chat/stream`
Same as `/chat` but streams the response as **Server-Sent Events**:

```
data: {"token": "Here"}
data: {"token": " is"}
data: {"token": " your measure..."}
data: {"done": true, "model": "llama-3.3-70b-versatile"}
```

### `GET /history/{session_id}`
Retrieve the full conversation history for a session.

### `POST /clear`
Clear the conversation history for a session.

```json
{ "session_id": "my-session" }
```

### `GET /sessions`
List all active sessions and their message counts.

### `GET /models`
List all supported Groq models.

---

## Deploy to Railway

1. Fork or push this repository to GitHub.
2. Create a new project on [Railway](https://railway.app/) and connect the repo.
3. Add the `GROQ_API_KEY` environment variable in **Railway → Variables**.
4. Railway auto-detects the Nixpacks builder and starts the server using the command in `railway.json`.

The service will be live at the Railway-provided URL within a minute.

---

## Project Structure

```
bi-bot/
├── main.py            # FastAPI application (routes, Groq client, streaming)
├── static/
│   └── index.html     # Chat UI frontend
├── requirements.txt   # Python dependencies
├── Procfile           # Process definition (Heroku-compatible)
├── railway.json       # Railway deployment config
└── README.md
```

---

## License

This project is open source. Feel free to use, modify, and distribute it.

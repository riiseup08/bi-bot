# bi-bot

A specialized chat interface for interacting with a personalized data analyst assistant powered by Groq LLM.

## Features

- Chat interface for seamless interaction with a data analyst assistant
- Specialized in Power BI, DAX, Power Query, SQL, and ETL processes
- No visualization or import capabilities - pure conversational data analysis
- Streaming responses for real-time interaction
- Session management for maintaining conversation history

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/riiseup08/bi-bot.git
   cd bi-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - `fastapi>=0.110.0` - Web framework
   - `uvicorn[standard]>=0.27.0` - ASGI server
   - `groq>=0.4.0` - Groq API client
   - `pydantic>=2.0.0` - Data validation

## Configuration

Set up your environment variables:

```bash
export GROQ_API_KEY=your_groq_api_key_here
export MODEL_NAME=llama-3.3-70b-versatile  # Optional, defaults to this
```

Or create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
MODEL_NAME=llama-3.3-70b-versatile
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The application will be available at: `http://localhost:8000`

## API Endpoints

- `GET /` - Web interface (HTML chat)
- `GET /health` - Health check
- `POST /chat` - Send a chat message
- `POST /chat/stream` - Stream chat responses
- `GET /history/{session_id}` - Get conversation history
- `POST /clear` - Clear conversation history
- `GET /sessions` - List all active sessions
- `GET /models` - Available Groq models

## Usage

1. Open your browser to `http://localhost:8000`
2. Start typing your data analysis questions
3. The BI assistant will respond with expert guidance on:
   - Power BI design and optimization
   - DAX formulas and measures
   - Power Query (M) transformations
   - Data modeling best practices
   - SQL queries for BI
   - Excel and Python analysis
   - ETL processes

## Architecture

- **Backend:** FastAPI (Python)
- **LLM:** Groq API (llama-3.3-70b-versatile)
- **Frontend:** Static HTML/CSS/JavaScript in `/static`
- **Session Storage:** In-memory conversation store
- **Server:** Uvicorn ASGI

## Troubleshooting

**Error: GROQ_API_KEY not set**
- Make sure you have set the `GROQ_API_KEY` environment variable
- Verify your API key is valid on the Groq platform

**Port 8000 already in use**
- Run on a different port: `uvicorn main:app --reload --port 8001`

## License

This project is open source.
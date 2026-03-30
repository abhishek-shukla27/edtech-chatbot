# EduBot – EdTech Customer Support Chatbot

AI-powered customer support chatbot for **LearnSphere** EdTech platform, built with FastAPI + Groq (Llama 3.3 70B).

## Features
- 💬 Conversational AI chat with full message history
- 📚 Course catalog & pricing information
- 💳 Payment methods, EMI, and refund policy handling
- 🎓 Certificate and enrollment queries
- 🚀 Powered by Llama 3.3 70B via Groq API
- 🌐 Polished dark-themed UI served from FastAPI

## Project Structure
```
edtech-chatbot/
├── main.py              # FastAPI backend
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
└── static/
    └── index.html       # Frontend UI
```

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Groq API key
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your key
GROQ_API_KEY=your_groq_api_key_here
```

Or export directly:
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at: https://console.groq.com

### 3. Run the server
```bash
uvicorn main:app --reload --port 8000
```

### 4. Open in browser
Visit: **http://localhost:8000**

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves the chat UI |
| `/chat` | POST | Send a message and get AI response |
| `/health` | GET | Health check |

### `/chat` Request Body
```json
{
  "messages": [
    { "role": "user", "content": "What courses do you offer?" }
  ]
}
```

### `/chat` Response
```json
{
  "reply": "We offer courses in Programming, Data Science...",
  "tokens_used": 342
}
```

## Tech Stack
- **Backend**: FastAPI + Uvicorn
- **AI Model**: Llama 3.3 70B via Groq API
- **Frontend**: Vanilla HTML/CSS/JS (no build step)
- **Fonts**: Sora + JetBrains Mono

# 🐳 Dockerized AI API

> FastAPI + LangChain chat API containerized with Docker — deployable anywhere

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-green)
![Docker](https://img.shields.io/badge/Docker-containerized-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3.7-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5--turbo-orange)

---

## 📌 What Is This?

A production-ready AI chat API built with FastAPI and LangChain, containerized with Docker. Any frontend (React, mobile, Streamlit) can connect to it via HTTP requests. Includes session memory, auto-generated API docs, and Docker Hub deployment.

---

## 🗺️ Simple Flow

```
Client (any frontend)
        ↓  POST /chat
FastAPI endpoint
        ↓
LangChain ConversationChain
+ session memory
        ↓  OpenAI API call
Response
        ↑  JSON response
Client
```

---

## 🏗️ Architecture

```
dockerized_ai_api/
├── main.py               ← FastAPI app — all endpoints
├── chains/
│   ├── chat_chain.py     ← LangChain conversation chain
│   └── memory.py         ← Session memory per user
├── models/
│   └── schemas.py        ← Pydantic request/response models
├── Dockerfile            ← Container build instructions
├── .dockerignore         ← Files excluded from container
├── docker-compose.yml    ← Run with one command
├── requirements.txt
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Root — check if API is running |
| GET | `/health` | Health check |
| POST | `/chat` | Send message, get AI response |
| POST | `/clear-memory` | Clear session conversation history |
| GET | `/sessions` | List all active sessions |

---

## 📦 Request / Response

**POST /chat:**
```json
Request:
{
  "message": "What is LangChain?",
  "session_id": "user123",
  "temperature": 0.7
}

Response:
{
  "response": "LangChain is a framework...",
  "session_id": "user123",
  "status": "ok"
}
```

---

## 🧠 Key Concepts

| Concept | What It Does |
|---|---|
| **FastAPI** | Modern Python web framework for building REST APIs |
| **@app.post()** | Decorator that creates a POST endpoint |
| **Pydantic BaseModel** | Validates request/response data automatically |
| **Session Memory** | Each session_id gets its own conversation history |
| **Docker** | Packages app + dependencies into portable container |
| **docker-compose** | Runs app with environment variables in one command |
| **CORS Middleware** | Allows any frontend to call the API |

---

## 🐳 Docker Commands

```bash
# Build image
docker build -t ai-chat-api .

# Run container
docker run -p 8000:8000 --env-file .env ai-chat-api

# Run with docker-compose
docker-compose up

# Push to Docker Hub
docker tag ai-chat-api YOUR_DOCKERHUB_USERNAME/ai-chat-api
docker push YOUR_DOCKERHUB_USERNAME/ai-chat-api
```

---

## ⚙️ Local Setup (Without Docker)

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

---

## 🌐 Why No Streamlit?

This is a **backend API project** — FastAPI IS the interface. Any frontend can connect:
- React frontend → POST /chat
- Mobile app → POST /chat
- Streamlit app → POST /chat
- Postman / curl → POST /chat

The `/docs` endpoint provides an interactive UI for testing directly in the browser.

---

## 📦 Tech Stack

- **FastAPI** — REST API framework
- **Uvicorn** — ASGI server for FastAPI
- **LangChain** — Conversation chain with memory
- **OpenAI** — GPT-3.5-turbo
- **Docker** — Containerization
- **Pydantic** — Data validation
- **python-dotenv** — Environment variables

---

## 👤 Author

**Venkata Reddy Bommavaram**
- 📧 bommavaramvenkat2003@gmail.com
- 💼 [LinkedIn](https://linkedin.com/in/venkatareddy1203)
- 🐙 [GitHub](https://github.com/venkata1236)
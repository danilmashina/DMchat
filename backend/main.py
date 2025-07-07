from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Создаём FastAPI-приложение
app = FastAPI()

# Настройка CORS (для общения с frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или ['http://localhost:3000'] или твой домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель запроса
class ChatRequest(BaseModel):
    message: str

# Основной обработчик POST-запроса
@app.post("/chat")
def chat_with_ai(request: ChatRequest):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise HTTPException(status_code=401, detail="API ключ не найден в переменных окружения")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://danilmashina.github.io/DMchat/",
        "X-Title": "NeuroToday",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {"role": "user", "content": request.message}
        ]
    }

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обращении к OpenRouter: {str(e)}")

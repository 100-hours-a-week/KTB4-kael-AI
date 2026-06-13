"""KoGPT2 Autoregressive 챗봇 — 서버 진입점.

실행:  python main.py   (또는  uvicorn main:app --reload)
브라우저:  http://localhost:8000
"""

import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import chat_router

app = FastAPI(title="KoGPT2 Chatbot")

# API 라우터를 먼저 등록 → /api/* 가 정적파일 마운트보다 우선 매칭됨
app.include_router(chat_router.router)

# static/ 을 "/" 에 마운트 (html=True → index.html 자동 서빙, 같은 origin이라 CORS 불필요)
_STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=_STATIC_DIR, html=True), name="static")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

"""채팅 라우터: 다음 단어 예측 / 문장 생성 엔드포인트."""

from fastapi import APIRouter

from app.controllers import chat_controller

router = APIRouter(prefix="/api")


@router.post("/next-word")
def next_word(data: dict):
    """입력 문장의 다음 단어 1개를 반환 (요건 1 시연)."""
    return chat_controller.predict_next_word(data)


@router.post("/chat")
def chat(data: dict):
    """입력 문장을 이어 완성된 문장을 반환 (요건 2)."""
    return chat_controller.chat(data)

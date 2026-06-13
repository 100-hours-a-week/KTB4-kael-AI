"""채팅 컨트롤러: 입력 검증 후 generator 호출."""

from fastapi import HTTPException

from app.model import generator

_MAX_INPUT_LEN = 500  # 입력 문장 최대 길이


def _get_params(data: dict) -> dict:
    """요청 본문에서 생성 파라미터를 꺼내고 기본값/범위를 적용."""
    text = (data.get("text") or "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="입력 문장이 비어 있습니다.")
    if len(text) > _MAX_INPUT_LEN:
        raise HTTPException(status_code=400, detail=f"입력은 {_MAX_INPUT_LEN}자 이하여야 합니다.")

    return {
        "text": text,
        "max_new_tokens": min(int(data.get("max_new_tokens", 40)), 100),
        "temperature": max(0.1, min(float(data.get("temperature", 0.8)), 2.0)),
        "top_k": max(1, min(int(data.get("top_k", 50)), 100)),
    }


def predict_next_word(data: dict) -> dict:
    """요건 1: 다음 단어(토큰) 1개만 예측."""
    p = _get_params(data)
    word = generator.next_word(p["text"], temperature=p["temperature"], top_k=p["top_k"])
    return {"input": p["text"], "next_word": word}


def chat(data: dict) -> dict:
    """요건 2: autoregressive 반복으로 문장 완성."""
    p = _get_params(data)
    full_text, generated = generator.generate(
        p["text"],
        max_new_tokens=p["max_new_tokens"],
        temperature=p["temperature"],
        top_k=p["top_k"],
    )
    return {"input": p["text"], "generated": generated, "full_text": full_text}

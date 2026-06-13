# KoGPT2 Autoregressive 챗봇

사전학습 모델 **KoGPT2**(`skt/kogpt2-base-v2`)를 사용해, 입력 문장의 **다음 단어를 예측**하고 이를 **재귀 반복(autoregressive)**하여 문장을 완성하는 한국어 챗봇. FastAPI로 웹 서비스한다.

- **GPU 불필요** — 사전학습 모델을 CPU로 추론만 한다 (파인튜닝 없음).
- 첫 실행 시 모델(~500MB)을 자동 다운로드하므로 인터넷 연결이 필요하다.

---

## 실행 방법

```bash
cd 05_pretrained_nlp/chatbot
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
pip install -r requirements.txt
python main.py                   # 첫 실행 시 모델 다운로드 (수 분 소요)
```

브라우저에서 **http://localhost:8000** 접속.

---

## 파일 구조

```
chatbot/
├── main.py                      # 진입점: FastAPI 앱 + 정적파일 마운트 + uvicorn 실행
├── requirements.txt
├── app/
│   ├── routers/
│   │   └── chat_router.py       # POST /api/next-word, POST /api/chat
│   ├── controllers/
│   │   └── chat_controller.py   # 입력 검증 + 파라미터 처리
│   └── model/
│       └── generator.py         # KoGPT2 로드 + autoregressive 토큰 루프 (핵심)
└── static/
    ├── index.html               # 반응형 채팅 UI
    ├── style.css
    └── script.js
```

> 기존 `02_FastAPI` 과제의 **Route → Controller → Model 3계층** 컨벤션을 따른다.

---

## 파이프라인 흐름

```
[웹 입력 문장]
  → 토크나이저 (문장 → 토큰 ID)
  → 모델 forward (마지막 위치의 다음 토큰 logits)
  → 샘플링 (temperature + top-k)
  → 토큰 추가
  → ⟳ 반복 (EOS 또는 max_new_tokens 까지)   ← autoregressive
  → 디코딩 (토큰 → 문장)
  → 웹 응답
```

`generator.py`의 두 함수가 과제 요건에 직접 대응한다.

| 함수 | 역할 | 요건 |
|------|------|------|
| `predict_next_token` | 다음 토큰 1개 예측 (logits → top-k 샘플링) | 1. 다음 단어 생성 |
| `generate` | `predict_next_token`을 EOS/최대길이까지 반복 | 2. autoregressive 문장 생성 |

---

## API

| 메서드 | 경로 | 설명 | 요청 본문 |
|--------|------|------|-----------|
| POST | `/api/next-word` | 다음 단어 1개 반환 (요건 1 시연) | `{"text": "오늘 날씨가"}` |
| POST | `/api/chat` | 완성된 문장 반환 (요건 2) | `{"text": "오늘 날씨가", "temperature": 0.8, "max_new_tokens": 40, "top_k": 50}` |

예시:

```bash
curl -X POST localhost:8000/api/next-word \
  -H "Content-Type: application/json" -d '{"text":"오늘 날씨가"}'

curl -X POST localhost:8000/api/chat \
  -H "Content-Type: application/json" -d '{"text":"오늘 날씨가"}'
```

생성 파라미터:
- **temperature**: 낮을수록 보수적, 높을수록 다양 (기본 0.8)
- **top_k**: 확률 상위 k개 토큰 중에서 샘플링 (기본 50)
- **max_new_tokens**: 최대 생성 토큰 수 (기본 40)

---

## 회고

<details>
<summary>펼쳐보기</summary>

- `generate()` 한 줄로 끝내지 않고 토큰 루프를 직접 구현해, "다음 토큰 예측 → 이어붙임 → 반복"이라는 autoregressive 개념을 코드로 드러냈다.
- 사전학습 모델 추론만으로도 한국어 문장 생성이 가능해 GPU·파인튜닝 없이 로컬에서 동작한다.
- 정적파일을 `/`에 마운트해 같은 origin에서 서빙하므로 CORS 설정이 필요 없었다.

</details>

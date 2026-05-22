# 02_FastAPI — 커뮤니티 서비스 백엔드

FastAPI로 커뮤니티 서비스 REST API를 구현하는 과제입니다.
동일한 기능을 세 가지 방식으로 단계별로 구현합니다.

---

## 버전 구성

| 폴더 | 데이터 저장 방식 | 상태 |
|------|----------------|------|
| `code_vanila/` | Python 리스트 (메모리) | ✅ 완료 |
| `code_DB/` | SQLite / SQLAlchemy | 🔜 예정 |
| `code_AI/` | DB + AI 기능 추가 | 🔜 예정 |

---

## 공통 기능

- 회원가입 / 로그인
- 게시글 CRUD
- 댓글 작성 / 삭제
- 좋아요 추가 / 취소
- 프론트엔드 (`index.html`) — 브라우저에서 직접 테스트 가능

---

## 실행 방법

각 버전의 폴더 안에서 실행합니다.

```bash
cd code_vanila        # 또는 code_DB, code_AI
source .venv/bin/activate
uvicorn main:app --reload
```

- 프론트엔드: `http://localhost:8000`
- API 문서: `http://localhost:8000/docs`

---

## 폴더 구조

```
02_FastAPI/
├── index.html                    # 공통 프론트엔드
├── requirements.txt              # 공통 패키지 목록 (vanila 기준)
├── README.md
│
├── code_vanila/                  # v1: 메모리 기반
│   ├── main.py
│   ├── routers/
│   ├── controllers/
│   └── models/
│
├── code_DB/                      # v2: DB 연동 (예정)
│   ├── main.py
│   ├── routers/
│   ├── controllers/
│   ├── models/
│   └── database.py               # DB 연결 설정
│
└── code_AI/                      # v3: AI 기능 추가 (예정)
    ├── main.py
    ├── routers/
    ├── controllers/
    ├── models/
    └── ai/                       # AI 관련 모듈
```

---

## 설계 원칙

모든 버전에서 **Route-Controller-Model** 패턴을 사용합니다.

```
요청 → Router → Controller → Model → 응답
```

- `routers/` : URL과 함수 연결
- `controllers/` : 비즈니스 로직
- `models/` : 데이터 접근 (버전마다 구현 방식이 달라지는 부분)

버전이 올라갈수록 `models/`만 바뀌고 `routers/`, `controllers/`는 최대한 유지합니다.

---

## 학습 노트

- [01_FastAPI_시작하기](./FastAPI_구현_정리_note/01_FastAPI_시작하기.md)
- [02_컨트롤러_확장하기](./FastAPI_구현_정리_note/02_컨트롤러_확장하기.md)

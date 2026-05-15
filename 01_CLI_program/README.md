# 학습 노트 검색 CLI

부트캠프에서 공부하며 작성한 마크다운 노트를 터미널에서 바로 검색하고 조회하는 CLI 도구입니다.

---

## 기능

| 명령어 | 설명 |
|--------|------|
| `list` | 노트 목록을 주차 순서로 출력 |
| `search` | 키워드가 포함된 노트와 해당 줄 출력 |
| `show` | 특정 노트의 전체 내용 출력 |

---

## 사용법

```bash
# 노트 목록 보기
python3 main.py list

# 키워드 검색
python3 main.py search "argparse"

# 노트 내용 보기
python3 main.py show week1_CLI.md
```

### 실행 예시

```
$ python3 main.py list
=== 노트 목록 ===

1. week1_CLI.md  —  CLI 프로그램
2. week2_Python.md  —  파이썬 기초

$ python3 main.py search "argparse"
=== 'argparse' 검색 결과 ===

[week1_CLI.md]
  5번째 줄: argparse로 터미널 인자를 파싱할 수 있다
```

---

## 파일 구조 
01_CLI_assignment/
├── main.py         # CLI 메인 코드
├── template.md     # 노트 기본 템플릿
└── README.md

## 앞으로 추가할 기능
- [ ] `organize` — 간단한 메모를 Claude API로 노트 형식에 맞게 자동 정리
- [ ] 날짜 필터 — 특정 주차 노트만 검색
- [ ] 내 노트 기반 Q&A

# 유엔젤 고령자 특화 에이전틱 AI 시스템

> 실세계 능동행동형 에이전틱 AI 기술개발 — 유엔젤 공동기관 6

고령자의 정서·안전·생활을 지원하는 멀티에이전트 컴포넌트 라이브러리와
자동 구성 오케스트레이션 엔진입니다.

## 시스템 개요

- **LLM:** Google Gemini 1.5 Flash (무료 티어)
- **컴포넌트:** 20종 (정서지원 5 / 생활보조 5 / 관계·사회 3 / 인지·건강 2 / 안전·위기 3 / LLM연계 2)
- **목표 실행률:** 자동 구성 정상 실행률 95% 이상

## 설치 및 실행

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# .env 파일에 GOOGLE_API_KEY 입력

# 테스트 실행
python -m pytest tests/ -v

# FastAPI 서버 실행
uvicorn server.main:app --reload --port 8000
```

## 아키텍처

```
Context 입력
    │
    ▼
Rule Engine (위기 6종 즉각 대응)
    │ 위기 아님
    ▼
Score Engine (14종 동적 선택)
    │
    ▼
Orchestrator (LangChain + Gemini)
    │
    ▼
컴포넌트 실행 + 발화 템플릿 선택
    │
    ▼
Feedback Engine (결과 학습 → 가중치 갱신)
```

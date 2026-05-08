# 유엔젤 고령자 특화 에이전틱 AI 시스템

> **프로젝트명:** 실세계 능동행동형 에이전틱 AI 기술개발 — 유엔젤 공동기관 6  
> **목표:** 고령자 특화 멀티에이전트 컴포넌트 라이브러리 + 자동 구성 오케스트레이션 엔진

고령자의 정서·안전·생활을 실시간으로 파악하고, 상황에 맞는 AI 에이전트 컴포넌트를 자동으로 선택·실행하는 시스템입니다.

---

## 성능 목표

| 단계 | 컴포넌트 수 | 자동 구성 실행률 |
|------|------------|----------------|
| 1단계 (2차년도) | 10종 | 75% 이상 |
| **2단계 (3차년도)** | **20종** | **95% 이상** |

현재 시나리오 테스트 기준 **10/10 (100%)** 달성

---

## 시스템 아키텍처

```
외부 입력 (ETRI·EICT·숙명여대 API / 생체·환경 센서)
    │
    ▼
┌─────────────────────────────────────────────────────┐
│                    Context 객체                      │
│  emotion_vector / memory_data / bio_data / env_data │
│  crisis_flags                                        │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│      Rule Engine        │  위기 조건 6종 즉각 판별
│  낙상/무반응/SOS/심박/   │  → 해당 컴포넌트 즉시 실행
│  고독사위험/위기발화     │
└────────────┬────────────┘
             │ 위기 아님
             ▼
┌─────────────────────────┐
│      Score Engine       │  감정매칭×0.4 + 기억관련도×0.3
│  17종 동적 컴포넌트      │  + 환경적합도×0.2 + 미사용보너스×0.1
│  점수 계산 및 순위 선정  │  → 상위 3개 후보 선발
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      Orchestrator       │  최고 점수 컴포넌트 실행
│  LangChain + Gemini     │  발화 템플릿 선택 (100종)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│    Feedback Engine      │  어르신 반응 평가 (+1.0 ~ -1.0)
│  가중치 자동 갱신 (lr=0.01)│  개인화 프로파일 SQLite 저장
└─────────────────────────┘
```

---

## 컴포넌트 20종

### 정서지원 (5종)
| 컴포넌트 | 설명 |
|----------|------|
| `empathy_dialog` | 감정 공감 대화 — 슬픔·외로움·불안 감지 시 |
| `emotion_reflection` | 감정 거울 반영 — 자기 인식 유도 |
| `mood_change` | 부정 감정 전환 — 활동·취미 제안 |
| `stabilization` | 안정화 — 야간 불안 시 호흡·심리 안정 안내 |
| `positive_sharing` | 긍정 경험 나누기 — 감사·좋은 일 공유 유도 |

### 생활보조 (5종)
| 컴포넌트 | 설명 |
|----------|------|
| `medication_reminder` | 복약 알림 — 시간 기반 트리거 (08·12·18시) |
| `meal_guide` | 식사 안내 — 식사 미감지 시 개입 |
| `sleep_monitor` | 수면 모니터링 — 야간 이상 패턴 감지 |
| `weather_info` | 날씨 안내 — 외출 전 날씨 정보 제공 |
| `schedule_manager` | 일정 관리 — 당일 일정 안내 및 준비 도움 |

### 관계·사회 (3종)
| 컴포넌트 | 설명 |
|----------|------|
| `family_contact` | 가족 연락 유도 — EICT 기억 데이터 기반 |
| `network_maintain` | 사회 관계망 유지 — 고립 위험 시 독려 |
| `encouragement` | 격려 — 자기효능감 강화 |

### 인지·건강 (2종)
| 컴포넌트 | 설명 |
|----------|------|
| `cognitive_stimulation` | 인지 자극 — 퀴즈·회상 대화 |
| `physical_activity` | 신체 활동 — 낙상 위험 낮은 스트레칭·걷기 권장 |

### 안전·위기 — Rule Engine 전용 (3종)
| 컴포넌트 | 설명 |
|----------|------|
| `anomaly_detection` | 이상 감지 — 낙상·무반응·심박 이상 즉각 대응 |
| `isolation_risk` | 고독사 위험 — isolation_risk_score ≥ 0.9 |
| `escalation` | 긴급 에스컬레이션 — 위기 발화·SOS 시 보호자 알림 |

### LLM 연계 (2종)
| 컴포넌트 | 설명 |
|----------|------|
| `play_agent` | 자유 대화·놀이 — Gemini 직접 호출, 긍정 상태 시 |
| `generative_agent` | 맥락 기반 생성 대화 — 감정 상태 맞춤 응답 |

---

## 핵심 데이터 스키마 (Context 객체)

```python
context = {
    "user_id": "elder_001",
    "timestamp": "2026-05-08T14:30:00",

    # ETRI 제공 — 정서 인지
    "emotion_vector": {
        "sadness": 0.7, "loneliness": 0.8,
        "anxiety": 0.3, "calm": 0.1, "joy": 0.0
    },

    # EICT + 숙명여대 제공 — 장기기억·라포
    "memory_data": {
        "recent_topics": ["손녀", "날씨", "무릎 통증"],
        "rapport_score": 0.75,
        "last_positive_response": "family_contact"
    },

    # 생체·환경 데이터
    "bio_data": {"heart_rate": 72, "no_movement_minutes": 45, "fall_detected": False},
    "env_data": {"time_of_day": "afternoon", "weather": "sunny", "location": "home"},

    # 위기 플래그
    "crisis_flags": {
        "crisis_utterance": False, "sos_activated": False, "isolation_risk_score": 0.3
    }
}
```

---

## 설치 및 실행

### 요구사항
- Python 3.11+
- Google Gemini API 키 ([aistudio.google.com](https://aistudio.google.com) 에서 무료 발급)

### 설치

```bash
git clone https://github.com/hkgorill/uangel-agent.git
cd uangel-agent

python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# .env 파일에 GOOGLE_API_KEY=발급받은키 입력
```

### 테스트 실행

```bash
python -m pytest tests/ -v
```

```
시나리오 테스트 결과: 10/10 통과 (100.0%)
[PASS] 낙상 감지 시나리오
[PASS] 우울 감지 시나리오
[PASS] 외로움 표현 시나리오
[PASS] 야간 불안 시나리오
...
13 passed in 12.39s
```

### FastAPI 서버 실행

```bash
uvicorn server.main:app --reload --port 8000
```

---

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| `POST` | `/intervention` | 컨텍스트 수신 → 컴포넌트 선택·실행 |
| `POST` | `/feedback` | 어르신 반응 평가 → 가중치 자동 갱신 |
| `GET` | `/profile/{user_id}` | 개인화 가중치 프로파일 조회 |
| `GET` | `/logs` | 개입 이력 조회 |
| `GET` | `/feedback` | 피드백 이력 조회 |
| `GET` | `/status` | 시스템 상태 확인 |

### 개입 요청 예시

```bash
curl -X POST http://localhost:8000/intervention \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "elder_001",
    "emotion_vector": {"sadness": 0.7, "loneliness": 0.8, "anxiety": 0.3, "calm": 0.1, "joy": 0.0},
    "memory_data": {"recent_topics": ["손녀", "날씨"], "rapport_score": 0.75, "last_positive_response": "family_contact"},
    "bio_data": {"heart_rate": 72, "no_movement_minutes": 45, "fall_detected": false},
    "env_data": {"time_of_day": "afternoon", "weather": "sunny", "location": "home"},
    "crisis_flags": {"crisis_utterance": false, "sos_activated": false, "isolation_risk_score": 0.3}
  }'
```

```json
{
  "component": "family_contact",
  "utterance": "가족 생각이 나시나요? 연락해 보시겠어요?",
  "mode": "score",
  "score": 0.935,
  "log_id": 1,
  "candidates": [["family_contact", 0.935], ["empathy_dialog", 0.81], ["generative_agent", 0.785]]
}
```

### 피드백 전송 예시

```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "log_id": 1,
    "user_id": "elder_001",
    "component": "family_contact",
    "reaction": "continued_conversation"
  }'
```

| reaction 값 | 의미 | 가중치 변화 |
|---|---|---|
| `continued_conversation` | 대화 지속 | +1.0 |
| `positive_emotion_change` | 긍정 감정 변화 | +0.8 |
| `no_response` | 무반응 | 0.0 |
| `negative_reaction` | 거부·부정 반응 | -1.0 |

---

## 프로젝트 구조

```
uangel-agent/
├── core/
│   ├── rule_engine.py       # 위기 즉각 대응 6종 조건 판별
│   ├── score_engine.py      # 동적 컴포넌트 점수 계산 및 순위
│   ├── orchestrator.py      # 오케스트레이션 메인 엔진
│   └── feedback_engine.py   # 반응 학습 및 가중치 갱신
│
├── components/              # 20종 행동 컴포넌트
│   ├── base_component.py
│   ├── emotional/           # 정서지원 5종
│   ├── daily/               # 생활보조 5종
│   ├── social/              # 관계·사회 3종
│   ├── cognitive/           # 인지·건강 2종
│   ├── safety/              # 안전·위기 3종
│   └── llm/                 # LLM 연계 2종
│
├── templates/
│   ├── template_pool.py
│   └── data/templates_v1.json   # 발화 템플릿 100종
│
├── api/
│   └── mock_clients.py      # ETRI·EICT·숙명여대 Mock API
│
├── server/
│   └── main.py              # FastAPI 서버
│
├── data/
│   └── db.py                # SQLite ORM (개입이력·피드백·프로파일)
│
└── tests/
    ├── scenarios/           # 시나리오 JSON 10종
    ├── test_rule_engine.py
    ├── test_score_engine.py
    └── test_orchestrator.py
```

---

## LLM 교체 가이드

`components/llm/` 내 한 줄만 변경하면 LLM을 교체할 수 있습니다.

```python
# 현재: Google Gemini (개발·테스트)
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 옵션 1: Claude (실증·운영)
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-sonnet-4-6")

# 옵션 2: GPT-4o
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
```

---

## 개발 환경

- **Python** 3.11 / WSL2 Ubuntu
- **LLM** Google Gemini 2.5 Flash (무료 티어, 분당 5회)
- **Framework** LangChain 0.3 / FastAPI / SQLAlchemy
- **DB** SQLite (로컬 개발) → 운영 시 교체 가능

---

*작성일: 2026-05-08 | 담당: 유엔젤 공동기관 6*

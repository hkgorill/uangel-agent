# 유엔젤 고령자 특화 에이전틱 AI 시스템 개발 작업계획서

> **프로젝트명:** 실세계 능동행동형 에이전틱 AI 기술개발 — 유엔젤 공동기관 6  
> **목표:** 고령자 특화 멀티에이전트 컴포넌트 라이브러리 + 자동 구성 오케스트레이션 엔진 개발  
> **개발 환경:** Python 3.11 / WSL2 Ubuntu / Claude Code  
> **LLM:** Google Gemini 1.5 Flash (무료 티어) → 실증 단계에서 교체 가능  
> **최종 성능 목표:** 에이전트 자동 구성 정상 실행률 95% 이상, 컴포넌트 20종

---

## 1. 프로젝트 디렉토리 구조

```
~/uangel-agent/
├── .env                         # API 키 (GOOGLE_API_KEY)
├── .gitignore
├── README.md
├── requirements.txt
│
├── core/                        # 핵심 엔진 모듈
│   ├── __init__.py
│   ├── rule_engine.py           # Rule Engine (위기 즉각 대응 6종)
│   ├── score_engine.py          # Score Engine (동적 선택 14종)
│   ├── orchestrator.py          # 오케스트레이션 메인 엔진
│   └── feedback_engine.py       # 피드백 · 자기개선 엔진
│
├── components/                  # 20종 행동 컴포넌트
│   ├── __init__.py
│   ├── base_component.py        # 컴포넌트 공통 인터페이스
│   ├── emotional/               # 정서지원 5종
│   │   ├── empathy_dialog.py
│   │   ├── emotion_reflection.py
│   │   ├── mood_change.py
│   │   ├── stabilization.py
│   │   └── positive_sharing.py
│   ├── daily/                   # 생활보조 5종
│   │   ├── medication_reminder.py
│   │   ├── meal_guide.py
│   │   ├── sleep_monitor.py
│   │   ├── weather_info.py
│   │   └── schedule_manager.py
│   ├── social/                  # 관계·사회 3종
│   │   ├── family_contact.py
│   │   ├── network_maintain.py
│   │   └── encouragement.py
│   ├── cognitive/               # 인지·건강 2종
│   │   ├── cognitive_stimulation.py
│   │   └── physical_activity.py
│   ├── safety/                  # 안전·위기 3종 (Rule Engine 전용)
│   │   ├── anomaly_detection.py
│   │   ├── isolation_risk.py
│   │   └── escalation.py
│   └── llm/                     # LLM 연계 2종
│       ├── play_agent.py
│       └── generative_agent.py
│
├── templates/                   # 발화 템플릿 풀
│   ├── template_pool.py         # 템플릿 로드·선택 로직
│   └── data/
│       └── templates_v1.json    # 100종 이상 발화 템플릿
│
├── api/                         # 외부 API 연동
│   ├── __init__.py
│   ├── etri_client.py           # ETRI 정서 인지 API
│   ├── eict_client.py           # EICT 장기기억 API
│   ├── sookmyung_client.py      # 숙명여대 라포 API
│   └── mock_clients.py          # 개발용 Mock API (실API 연동 전)
│
├── server/                      # FastAPI 서버
│   ├── __init__.py
│   └── main.py                  # API 엔드포인트
│
├── data/                        # 로컬 데이터 저장
│   ├── db.py                    # SQLite 연동
│   └── uangel.db                # 로컬 개발 DB
│
└── tests/                       # 테스트
    ├── test_rule_engine.py
    ├── test_score_engine.py
    ├── test_orchestrator.py
    └── scenarios/               # 시나리오 테스트 케이스
        ├── scenario_01_fall.json
        ├── scenario_02_depression.json
        └── ...
```

---

## 2. 환경 설정

### .env 파일
```env
GOOGLE_API_KEY=여기에_Gemini_API_키_입력
```

### requirements.txt
```
langchain==0.3.25
langchain-google-genai
google-generativeai
fastapi
uvicorn
python-dotenv
numpy
requests
sqlalchemy
```

### 패키지 설치
```bash
cd ~/uangel-agent
source .venv/bin/activate
pip install -r requirements.txt
```

### Gemini 연결 확인
```bash
python -c "
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')
response = llm.invoke('안녕하세요. 한 문장으로 자기소개 해줘')
print(response.content)
print('--- Gemini 연결 성공! ---')
"
```

### LLM 모델 정보
| 항목 | 내용 |
|------|------|
| 모델명 | gemini-1.5-flash |
| 무료 한도 | 분당 15회, 일 1,500회 |
| 향후 교체 | 코드 한 줄 변경으로 Claude 등 다른 LLM 전환 가능 |

---

## 3. 개발 단계별 계획

### Phase 0. 환경 세팅 ✅ (완료)
- [x] WSL2 Ubuntu Python 3.11 설치
- [x] 가상환경 생성 (.venv)
- [x] Gemini 패키지 설치 (langchain-google-genai)
- [x] .env GOOGLE_API_KEY 설정
- [x] Gemini 연결 확인

---

### Phase 1. 기반 구조 구축 (1~2주)

**목표:** 뼈대 코드 완성 + Mock API로 전체 흐름 동작 확인

#### Task 1-1. 프로젝트 초기화
```
Claude Code 지시:
"uangel-agent 프로젝트 디렉토리 구조를 위의 설계대로 생성하고,
각 __init__.py 와 requirements.txt 를 작성해줘.
LLM은 Google Gemini 1.5 Flash 사용 기준으로 작성해줘"
```

#### Task 1-2. 컴포넌트 기반 클래스 설계
```
Claude Code 지시:
"components/base_component.py 를 작성해줘.
모든 컴포넌트가 상속받을 BaseComponent 클래스를 만들고,
필수 메서드는 execute(context), get_score_factors() 로 해줘"
```

#### Task 1-3. Mock API 클라이언트 구현
```
Claude Code 지시:
"api/mock_clients.py 를 작성해줘.
ETRI 정서벡터, EICT 장기기억, 숙명여대 라포 데이터를
실제 API 없이 테스트할 수 있는 Mock 데이터를 반환하게 해줘.
정서 상태는 emotion_vector(슬픔/외로움/불안/평온/기쁨),
기억 데이터는 recent_topics(최근 대화 주제 리스트)로 구성해줘"
```

#### Task 1-4. Rule Engine 구현
```
Claude Code 지시:
"core/rule_engine.py 를 작성해줘.
위기 판단 조건 6가지를 구현해줘:
1. 낙상 감지 (fall_detected == True)
2. 4시간 이상 무반응 (no_movement_minutes >= 240)
3. 위기 발화 감지 (crisis_utterance == True)
4. 심박수 이상 (heart_rate > 120 or heart_rate < 40)
5. 고독사 위험 (isolation_risk_score >= 0.9)
6. 긴급 SOS (sos_activated == True)
조건 충족 시 해당 컴포넌트 이름을 즉각 반환하고,
미충족 시 None 반환"
```

#### Task 1-5. Score Engine 구현
```
Claude Code 지시:
"core/score_engine.py 를 작성해줘.
14종 동적 컴포넌트 각각에 대해 아래 공식으로 점수 계산:
  점수 = 감정매칭×0.4 + 기억관련도×0.3 + 환경적합도×0.2 + 미사용보너스×0.1
가중치는 추후 피드백으로 갱신될 수 있게 self.weights 딕셔너리로 관리하고,
rank_components(context) 메서드로 점수 순위 리스트를 반환해줘"
```

#### Task 1-6. 오케스트레이터 메인 엔진
```
Claude Code 지시:
"core/orchestrator.py 를 작성해줘.
LLM은 Google Gemini 1.5 Flash 사용:
  from langchain_google_genai import ChatGoogleGenerativeAI
  llm = ChatGoogleGenerativeAI(model='gemini-1.5-flash')

실행 흐름:
1. Rule Engine 먼저 평가 → 위기면 즉각 실행
2. 위기 아니면 Score Engine으로 상위 3개 컴포넌트 선택
3. LangChain Agent로 최종 컴포넌트 실행 및 발화 템플릿 선택
4. 실행 결과 로그 저장"
```

---

### Phase 2. 컴포넌트 20종 구현 (2~4주)

**목표:** 각 카테고리별 컴포넌트 완성 + 발화 템플릿 풀 100종 구축

#### Task 2-1. 정서지원 5종 구현
```
Claude Code 지시:
"components/emotional/ 하위 5개 컴포넌트를 구현해줘.
각각 BaseComponent 상속, execute(context) 구현,
발화 템플릿 풀에서 상황에 맞는 문장 선택 로직 포함"
```

#### Task 2-2. 생활보조 5종 구현
```
Claude Code 지시:
"components/daily/ 하위 5개 컴포넌트 구현.
복약알림은 시간 기반 트리거,
식사안내는 식사 미감지 시 개입,
수면모니터링은 야간 이상 패턴 감지 시 개입"
```

#### Task 2-3. 관계·사회 / 인지·건강 5종 구현
```
Claude Code 지시:
"components/social/ 3종, components/cognitive/ 2종 구현.
가족연락 유도는 EICT 기억 데이터에서 가족 관련 이력 참조,
인지자극은 간단한 퀴즈·회상 대화 유도"
```

#### Task 2-4. 안전·위기 3종 구현 (Rule Engine 전용)
```
Claude Code 지시:
"components/safety/ 3종 구현.
escalation.py 는 보호자 연락처로 알림 발송 로직 포함
(실제 발송은 Mock, 인터페이스만 구현)"
```

#### Task 2-5. LLM 연계 2종 구현
```
Claude Code 지시:
"components/llm/ 하위 2개 컴포넌트 구현.
Google Gemini 1.5 Flash 를 직접 호출해 자유 대화·놀이 기능 구현.
from langchain_google_genai import ChatGoogleGenerativeAI 사용"
```

#### Task 2-6. 발화 템플릿 풀 구축
```
Claude Code 지시:
"templates/data/templates_v1.json 을 작성해줘.
고령자 대상 정서 상태별 발화 문장 100종 이상.
카테고리: 공감/안정/격려/일상/위기/가족/건강
각 문장은 tone(따뜻함/차분함/활기참), situation, text 필드 포함"
```

---

### Phase 3. Feedback Engine + 자기개선 (1~2주)

**목표:** 개입 결과를 학습해 가중치 자동 갱신하는 구조 완성

#### Task 3-1. Feedback Engine 구현
```
Claude Code 지시:
"core/feedback_engine.py 를 작성해줘.
개입 후 어르신 반응 평가 기준:
  +1.0: 대화 지속 (continued_conversation)
  +0.8: 긍정 정서 변화 (positive_emotion_change)
   0.0: 무반응 (no_response)
  -1.0: 거부·부정 반응 (negative_reaction)
평가 결과로 ScoreEngine의 컴포넌트별 가중치를 소폭 갱신 (lr=0.01)
개인별 선호도 프로파일을 SQLite에 저장"
```

#### Task 3-2. 데이터 저장 구조
```
Claude Code 지시:
"data/db.py 를 작성해줘.
SQLite 기반, 테이블 3개:
1. intervention_log: 개입 이력 (시간, 컴포넌트, 발화, 어르신ID)
2. user_profile: 어르신별 개인화 가중치 프로파일
3. feedback_log: 반응 평가 기록
SQLAlchemy ORM 사용"
```

---

### Phase 4. 시나리오 테스트 (1주)

**목표:** 10종 시나리오로 정상 실행률 75% 이상 확인 (1단계 목표)

#### Task 4-1. 테스트 시나리오 작성
```
Claude Code 지시:
"tests/scenarios/ 하위에 시나리오 JSON 파일 10개 작성해줘.
각 시나리오는 input(context 데이터)과 expected_component(기대 컴포넌트)로 구성.
포함할 시나리오:
01_낙상감지, 02_우울감지, 03_외로움표현, 04_야간불안,
05_반복발화, 06_무반응4시간, 07_식사미감지, 08_가족언급,
09_복약시간, 10_긍정상태일상대화"
```

#### Task 4-2. 자동화 테스트 실행기
```
Claude Code 지시:
"tests/test_orchestrator.py 를 작성해줘.
scenarios/ 의 JSON 10개를 순서대로 실행하고,
expected_component 와 실제 실행 컴포넌트를 비교해서
정상 실행률(%)을 출력하는 테스트 코드 작성"
```

---

### Phase 5. FastAPI 서버 + 컨소시엄 연동 준비 (1주)

**목표:** 타 기관 API 수신 엔드포인트 완성

#### Task 5-1. FastAPI 서버 구현
```
Claude Code 지시:
"server/main.py 를 작성해줘.
엔드포인트:
POST /intervention  : 외부 컨텍스트 수신 → 오케스트레이터 실행 → 결과 반환
GET  /status        : 시스템 상태 확인
GET  /logs          : 최근 개입 이력 조회
요청 스키마: user_id, emotion_vector, memory_data, env_data, bio_data"
```

---

## 4. 핵심 데이터 스키마 (Context 객체)

오케스트레이터가 받는 표준 입력 구조입니다.

```python
context = {
    "user_id": "elder_001",
    "timestamp": "2026-05-08T14:30:00",

    # ETRI 제공 (정서 인지)
    "emotion_vector": {
        "sadness": 0.7,
        "loneliness": 0.8,
        "anxiety": 0.3,
        "calm": 0.1,
        "joy": 0.0
    },

    # EICT + 숙명여대 제공 (장기기억 · 라포)
    "memory_data": {
        "recent_topics": ["손녀", "날씨", "무릎 통증"],
        "rapport_score": 0.75,
        "last_positive_response": "family_contact_agent"
    },

    # 생체 · 환경 데이터
    "bio_data": {
        "heart_rate": 72,
        "no_movement_minutes": 45,
        "fall_detected": False
    },
    "env_data": {
        "time_of_day": "afternoon",
        "weather": "sunny",
        "location": "home"
    },

    # 위기 플래그
    "crisis_flags": {
        "crisis_utterance": False,
        "sos_activated": False,
        "isolation_risk_score": 0.3
    }
}
```

---

## 5. LLM 교체 가이드

현재는 Gemini 무료 티어로 개발하고, 향후 필요 시 아래 한 줄만 교체하면 됩니다.

```python
# 현재: Google Gemini (무료 개발용)
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# 향후 교체 옵션 1: Claude (실증·운영)
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-sonnet-4-6")

# 향후 교체 옵션 2: GPT-4
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
```

나머지 코드는 전혀 수정 없이 동작합니다.

---

## 6. 성능 목표 및 측정 기준

| 단계 | 컴포넌트 수 | 자동 구성 실행률 | 협업 성공률 |
|------|------------|----------------|-----------|
| 1단계 완료 (2차년도) | 10종 | 75% 이상 | 75% 이상 |
| 2단계 완료 (3차년도) | 20종 | **95% 이상** | **95% 이상** |

**측정 방법:** 시나리오 JSON 기반 자동화 테스트 → `정상 실행 건수 / 전체 시나리오 수 × 100`

---

## 7. Claude Code 사용 원칙

### 작업 지시 방법
각 Task의 `Claude Code 지시:` 블록을 **그대로 Claude Code에 붙여넣어** 실행합니다.

### 개발 순서 원칙
1. **항상 Task 순서대로** 진행 (의존성 있음)
2. 각 Task 완료 후 **간단한 실행 테스트** 확인 후 다음 단계
3. 오류 발생 시 에러 메시지 전체를 Claude Code에 붙여넣어 수정 요청

### 전체 흐름 테스트
```bash
# 가상환경 활성화
source .venv/bin/activate

# 전체 시나리오 테스트 실행
python -m pytest tests/ -v

# FastAPI 서버 실행
uvicorn server.main:app --reload --port 8000
```

---

## 8. 지금 바로 시작 — Phase 1 Task 1-1

Claude Code에 아래 내용을 그대로 붙여넣으세요:

```
uangel-agent 프로젝트 디렉토리 구조를 아래와 같이 생성해줘.

core/, components/emotional/, components/daily/, components/social/,
components/cognitive/, components/safety/, components/llm/,
templates/data/, api/, server/, data/, tests/scenarios/

각 디렉토리에 __init__.py 생성하고,
requirements.txt 는 아래 패키지로 작성해줘:
langchain==0.3.25
langchain-google-genai
google-generativeai
fastapi
uvicorn
python-dotenv
numpy
requests
sqlalchemy

README.md 는 프로젝트 개요를 한국어로 간단히 작성해줘.
LLM은 Google Gemini 1.5 Flash 사용 기준으로 명시해줘.
```

---

*작성일: 2026-05-08 | 버전: v1.1 (Gemini API 적용) | 담당: 유엔젤 공동기관 6*

# 컨소시엄 연동 아키텍처

## 유엔젤의 역할

유엔젤 에이전틱 AI는 컨소시엄 내에서 **"무엇을 말할지 결정하는 뇌"** 역할에 집중한다.  
데이터 수집·변환은 케어앱/게이트웨이가 담당하며, 유엔젤은 조립된 컨텍스트를 받아 발화 텍스트를 반환한다.

---

## 전체 데이터 흐름

```
[어르신]
  │ 음성
  ▼
[사운더스트리]  ── STT → 텍스트 → 감정 분석 요청
                                        │
[ETRI]     ── 감정 벡터 (emotion_vector) ─┐
[EICT]     ── 장기기억 (memory_data)      ─┤
[숙명여대]  ── 라포 점수 (rapport_score)   ─┤
[IoT 기기] ── 심박/낙상/무활동             ─┤
                                          │
                                 [케어앱 / 게이트웨이]
                                     context 조립
                                          │
                                          ▼
                                 [유엔젤 POST /intervention]
                                 Rule Engine → Score Engine
                                 → 컴포넌트 선택 → 발화 생성
                                          │
                                 [케어앱 / 게이트웨이]
                                          │
                                 [사운더스트리] ── TTS
                                          │
                                     [어르신] 음성 출력
```

---

## 역할 분담표

| 역할 | 담당 기관 |
|------|-----------|
| 음성 → 텍스트 (STT) | 사운더스트리 |
| 텍스트 감정 분석 | ETRI |
| 장기기억 조회 | EICT |
| 라포 측정 | 숙명여대 |
| 생체·환경 데이터 수집 | IoT 기기 |
| 데이터 수집 및 context 조립 | 케어앱 / 게이트웨이 |
| **개입 컴포넌트 결정** | **유엔젤** |
| **발화 텍스트 생성** | **유엔젤** |
| 피드백 수집 및 전달 | 케어앱 / 게이트웨이 |
| 텍스트 → 음성 (TTS) | 사운더스트리 |

---

## 유엔젤 API 인터페이스

### 입력 — POST /intervention

케어앱/게이트웨이가 각 기관 API 호출 결과를 조립해 전달한다.

```json
{
  "user_id": "elder_003",
  "emotion_vector": {
    "sadness": 0.4, "loneliness": 0.9, "anxiety": 0.2,
    "calm": 0.1, "joy": 0.0
  },
  "memory_data": {
    "recent_topics": ["손녀", "아들"],
    "rapport_score": 0.7,
    "last_positive_response": "family_contact"
  },
  "bio_data": {
    "heart_rate": 70, "no_movement_minutes": 60, "fall_detected": false
  },
  "env_data": {
    "time_of_day": "afternoon", "weather": "sunny", "location": "home"
  },
  "crisis_flags": {
    "crisis_utterance": false, "sos_activated": false, "isolation_risk_score": 0.5
  }
}
```

### 출력

```json
{
  "component": "family_contact",
  "utterance": "손녀 분 이야기를 하셨네요. 오늘 전화 한번 해보시는 건 어떨까요?",
  "mode": "score",
  "score": 0.855,
  "log_id": 42
}
```

- `utterance`: 케어앱이 사운더스트리 TTS에 전달할 발화 텍스트
- `log_id`: 이후 피드백 전송 시 사용

### 피드백 — POST /feedback

어르신 반응을 케어매니저가 입력하면 유엔젤이 가중치를 자동 갱신한다.

```json
{
  "log_id": 42,
  "user_id": "elder_003",
  "component": "family_contact",
  "reaction": "positive_emotion_change"
}
```

---

## 시나리오 예시 — 외로움 감지 전체 흐름

1. 어르신이 "아들이 보고 싶다"고 발화
2. **사운더스트리** STT → 텍스트 변환
3. **ETRI** 감정 분석 → `loneliness: 0.9`
4. **EICT** 장기기억 조회 → `recent_topics: ["손녀", "아들"]`
5. **숙명여대** 라포 측정 → `rapport_score: 0.7`
6. **케어앱** 데이터 조립 → 유엔젤 `/intervention` 호출
7. **유엔젤** Rule Engine (위기 없음) → Score Engine → `family_contact` 선택 (score: 0.855)
8. **유엔젤** 발화 생성 → `"손녀 분 이야기를 하셨네요. 오늘 전화 한번 해보시는 건 어떨까요?"`
9. **케어앱** utterance 수신 → **사운더스트리** TTS → 어르신에게 음성 출력
10. 어르신이 아들에게 전화 → 기분 호전
11. **케어매니저** → 유엔젤 `/feedback` 전송 (`positive_emotion_change`)
12. **유엔젤** 가중치 자동 갱신 → 다음 유사 상황에서 `family_contact` 더 잘 선택

---

## api/ 디렉터리 현황

`api/etri_client.py`, `api/eict_client.py`, `api/sookmyung_client.py`는 유엔젤이 직접 외부 API를 호출해야 하는 시나리오에 대비한 준비 코드다.  
현재 컨소시엄 협의 기준으로는 케어앱/게이트웨이가 데이터를 조립해 전달하므로 직접 호출하지 않는다.  
향후 협의 결과에 따라 활성화할 수 있다.

from components.base_component import BaseComponent
from templates.template_pool import get_template
from datetime import datetime


class MedicationReminder(BaseComponent):
    name = "medication_reminder"
    category = "daily"
    description = "복약 시간 알림."

    _MEDICATION_HOURS = [8, 12, 18]  # 복약 시간대 (시)

    def execute(self, context: dict) -> dict:
        utterance = get_template("일상", tone="따뜻함", situation="복약")
        return self._build_result(utterance)

    _MED_KEYWORDS = ["약", "혈압", "혈당", "복약", "처방", "알약", "비타민"]

    def get_score_factors(self, context: dict) -> dict:
        now_hour = datetime.now().hour
        near = any(abs(now_hour - h) <= 1 for h in self._MEDICATION_HOURS)
        env_suitability = 0.95 if near else 0.1
        topics = context.get("memory_data", {}).get("recent_topics", [])
        has_med_topic = any(k in t for t in topics for k in self._MED_KEYWORDS)
        # 복약 관련 대화 + 복약 시간대가 겹칠 때 강한 신호
        emotion_match = 0.6 if (near and has_med_topic) else (0.4 if has_med_topic else 0.3)
        memory_relevance = 0.9 if has_med_topic else 0.5
        return {
            "emotion_match": emotion_match,
            "memory_relevance": memory_relevance,
            "env_suitability": env_suitability,
        }

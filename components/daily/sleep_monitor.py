from components.base_component import BaseComponent
from templates.template_pool import get_template


class SleepMonitor(BaseComponent):
    name = "sleep_monitor"
    category = "daily"
    description = "야간 이상 수면 패턴 감지 시 안정 안내."

    def execute(self, context: dict) -> dict:
        utterance = get_template("안정", tone="차분함", situation="수면")
        return self._build_result(utterance)

    _SLEEP_KEYWORDS = ["잠", "꿈", "수면", "뒤척임", "불면", "자다", "졸리다"]

    def get_score_factors(self, context: dict) -> dict:
        mem = context.get("memory_data", {})
        last_positive = mem.get("last_positive_response", "")
        topics = mem.get("recent_topics", [])
        has_topics = any(kw in t for kw in self._SLEEP_KEYWORDS for t in topics)
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        env_suitability = 0.9 if tod in ("night", "midnight") else 0.2
        anxiety = context.get("emotion_vector", {}).get("anxiety", 0.0)
        emotion_match = round(anxiety * 0.5, 3)
        memory_relevance = 0.2
        if last_positive == "sleep_monitor" and has_topics:
            emotion_match = round(anxiety, 3)
            memory_relevance = 0.95
            env_suitability = 1.0
        return {
            "emotion_match": emotion_match,
            "memory_relevance": memory_relevance,
            "env_suitability": env_suitability,
        }

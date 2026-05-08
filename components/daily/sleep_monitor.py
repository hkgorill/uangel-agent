from components.base_component import BaseComponent
from templates.template_pool import get_template


class SleepMonitor(BaseComponent):
    name = "sleep_monitor"
    category = "daily"
    description = "야간 이상 수면 패턴 감지 시 안정 안내."

    def execute(self, context: dict) -> dict:
        utterance = get_template("안정", tone="차분함", situation="수면")
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        env_suitability = 0.9 if tod in ("night", "midnight") else 0.2
        anxiety = context.get("emotion_vector", {}).get("anxiety", 0.0)
        return {
            "emotion_match": round(anxiety * 0.5, 3),
            "memory_relevance": 0.2,
            "env_suitability": env_suitability,
        }

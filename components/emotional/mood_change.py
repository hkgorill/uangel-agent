from components.base_component import BaseComponent
from templates.template_pool import get_template


class MoodChange(BaseComponent):
    name = "mood_change"
    category = "emotional"
    description = "부정 감정을 긍정으로 전환하는 활동을 제안한다."

    def execute(self, context: dict) -> dict:
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        situation = "아침" if tod == "morning" else "취미"
        utterance = get_template("격려", tone="활기참", situation=situation)
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        ev = context.get("emotion_vector", {})
        neg = ev.get("sadness", 0) + ev.get("loneliness", 0)
        return {
            "emotion_match": round(min(1.0, neg), 3),
            "memory_relevance": 0.3,
            "env_suitability": 0.6,
        }

from components.base_component import BaseComponent
from templates.template_pool import get_template


class MealGuide(BaseComponent):
    name = "meal_guide"
    category = "daily"
    description = "식사 미감지 시 식사 안내."

    def execute(self, context: dict) -> dict:
        utterance = get_template("일상", tone="따뜻함", situation="식사미감지")
        return self._build_result(utterance)

    _MEAL_KEYWORDS = ["밥", "식사", "점심", "저녁", "아침", "식욕", "먹", "배", "음식"]

    def get_score_factors(self, context: dict) -> dict:
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        meal_times = {"morning": 0.9, "afternoon": 0.8, "evening": 0.95}
        env_suitability = meal_times.get(tod, 0.5)
        topics = context.get("memory_data", {}).get("recent_topics", [])
        has_meal_topic = any(k in t for t in topics for k in self._MEAL_KEYWORDS)
        return {
            "emotion_match": 0.5 if has_meal_topic else 0.2,
            "memory_relevance": 0.85 if has_meal_topic else 0.4,
            "env_suitability": env_suitability,
        }

from components.base_component import BaseComponent
from templates.template_pool import get_template


class Encouragement(BaseComponent):
    name = "encouragement"
    category = "social"
    description = "긍정 정서와 자기효능감 강화 격려."

    def execute(self, context: dict) -> dict:
        utterance = get_template("격려", tone="따뜻함", situation="격려일반")
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        sadness = context.get("emotion_vector", {}).get("sadness", 0.0)
        return {
            "emotion_match": round(sadness * 0.6, 3),
            "memory_relevance": 0.3,
            "env_suitability": 0.8,
        }

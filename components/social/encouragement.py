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
        mem = context.get("memory_data", {})
        last_positive = mem.get("last_positive_response", "")
        rapport = mem.get("rapport_score", 0.5)
        sadness = context.get("emotion_vector", {}).get("sadness", 0.0)
        emotion_match = round(sadness * 0.6, 3)
        memory_relevance = 0.3
        env_suitability = 0.8
        if last_positive == "encouragement":
            emotion_match = min(1.0, round(sadness + 0.2, 3))
            memory_relevance = min(1.0, round(rapport + 0.2, 3))
            env_suitability = 0.85
        return {
            "emotion_match": emotion_match,
            "memory_relevance": memory_relevance,
            "env_suitability": env_suitability,
        }

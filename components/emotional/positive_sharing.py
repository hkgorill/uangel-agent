from components.base_component import BaseComponent
from templates.template_pool import get_template


class PositiveSharing(BaseComponent):
    name = "positive_sharing"
    category = "emotional"
    description = "긍정적 경험·감사 나누기 대화 유도."

    def execute(self, context: dict) -> dict:
        utterance = get_template("격려", tone="따뜻함", situation="긍정")
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        joy = context.get("emotion_vector", {}).get("joy", 0.0)
        calm = context.get("emotion_vector", {}).get("calm", 0.0)
        return {
            "emotion_match": round((joy + calm) / 2, 3),
            "memory_relevance": 0.4,
            "env_suitability": 0.8,
        }

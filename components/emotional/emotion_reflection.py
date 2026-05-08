from components.base_component import BaseComponent
from templates.template_pool import get_template


class EmotionReflection(BaseComponent):
    name = "emotion_reflection"
    category = "emotional"
    description = "어르신의 감정을 거울처럼 반영해 자기 인식을 돕는다."

    def execute(self, context: dict) -> dict:
        utterance = get_template("공감", tone="차분함", situation="공감일반")
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        ev = context.get("emotion_vector", {})
        anxiety = ev.get("anxiety", 0.0)
        return {
            "emotion_match": round(anxiety, 3),
            "memory_relevance": 0.4,
            "env_suitability": 0.7,
        }

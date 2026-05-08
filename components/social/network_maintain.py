from components.base_component import BaseComponent
from templates.template_pool import get_template


class NetworkMaintain(BaseComponent):
    name = "network_maintain"
    category = "social"
    description = "사회적 관계망 유지 독려."

    def execute(self, context: dict) -> dict:
        utterance = get_template("가족", tone="차분함", situation="연락독촉")
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        isolation = context.get("crisis_flags", {}).get("isolation_risk_score", 0.0)
        return {
            "emotion_match": round(isolation * 0.8, 3),
            "memory_relevance": 0.5,
            "env_suitability": 0.6,
        }

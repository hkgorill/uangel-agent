from components.base_component import BaseComponent
from templates.template_pool import get_template


class IsolationRisk(BaseComponent):
    name = "isolation_risk"
    category = "safety"
    description = "고독사 위험 감지 시 개입."

    def execute(self, context: dict) -> dict:
        utterance = get_template("위기", tone="따뜻함", situation="고독")
        return self._build_result(utterance, action="ALERT_GUARDIAN")

    def get_score_factors(self, context: dict) -> dict:
        return {"emotion_match": 0.0, "memory_relevance": 0.0, "env_suitability": 0.0}

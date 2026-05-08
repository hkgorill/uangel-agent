from components.base_component import BaseComponent
from templates.template_pool import get_template


class AnomalyDetection(BaseComponent):
    name = "anomaly_detection"
    category = "safety"
    description = "낙상·무반응·심박 이상 감지 시 즉각 대응."

    def execute(self, context: dict) -> dict:
        bio = context.get("bio_data", {})
        if bio.get("fall_detected"):
            utterance = get_template("위기", situation="낙상")
            action = "ALERT_GUARDIAN"
        elif bio.get("no_movement_minutes", 0) >= 240:
            utterance = get_template("위기", situation="무반응")
            action = "ALERT_GUARDIAN"
        else:
            utterance = get_template("위기", situation="응급")
            action = "ALERT_GUARDIAN"
        return self._build_result(utterance, action=action)

    def get_score_factors(self, context: dict) -> dict:
        return {"emotion_match": 0.0, "memory_relevance": 0.0, "env_suitability": 0.0}

from components.base_component import BaseComponent
from templates.template_pool import get_template


class PhysicalActivity(BaseComponent):
    name = "physical_activity"
    category = "cognitive"
    description = "낙상 위험 낮은 가벼운 신체 활동 권장."

    def execute(self, context: dict) -> dict:
        no_movement = context.get("bio_data", {}).get("no_movement_minutes", 0)
        if no_movement > 120:
            utterance = get_template("건강", tone="활기참", situation="걷기")
        else:
            utterance = get_template("건강", tone="활기참", situation="스트레칭")
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        no_movement = context.get("bio_data", {}).get("no_movement_minutes", 0)
        env_suitability = min(1.0, no_movement / 180.0)
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        if tod in ("night", "midnight"):
            env_suitability *= 0.2
        return {
            "emotion_match": 0.3,
            "memory_relevance": 0.2,
            "env_suitability": round(env_suitability, 3),
        }

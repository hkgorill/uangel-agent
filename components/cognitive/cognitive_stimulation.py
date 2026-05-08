from components.base_component import BaseComponent
from templates.template_pool import get_template


class CognitiveStimulation(BaseComponent):
    name = "cognitive_stimulation"
    category = "cognitive"
    description = "퀴즈·회상 대화로 인지 기능 자극."

    def execute(self, context: dict) -> dict:
        topics = context.get("memory_data", {}).get("recent_topics", [])
        if topics:
            utterance = get_template("인지", situation="회상")
        else:
            utterance = get_template("인지", tone="활기참", situation="퀴즈")
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        rapport = context.get("memory_data", {}).get("rapport_score", 0.5)
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        env_suitability = 0.8 if tod in ("morning", "afternoon") else 0.3
        return {
            "emotion_match": 0.5,
            "memory_relevance": round(rapport, 3),
            "env_suitability": env_suitability,
        }

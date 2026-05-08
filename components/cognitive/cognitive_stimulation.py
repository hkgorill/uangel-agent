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
        mem = context.get("memory_data", {})
        rapport = mem.get("rapport_score", 0.5)
        last_positive = mem.get("last_positive_response", "")
        topics = mem.get("recent_topics", [])
        _COGNITIVE_KEYWORDS = ["옛날 노래", "추억", "퀴즈", "기억", "노래", "옛날"]
        has_topics = any(kw in t for kw in _COGNITIVE_KEYWORDS for t in topics)
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        env_suitability = 0.8 if tod in ("morning", "afternoon") else 0.3
        emotion_match = 0.5
        memory_relevance = round(rapport, 3)
        if last_positive == "cognitive_stimulation":
            memory_relevance = min(1.0, rapport + 0.15)
            emotion_match = 0.65
        if has_topics:
            memory_relevance = min(1.0, memory_relevance + 0.1)
        return {
            "emotion_match": round(emotion_match, 3),
            "memory_relevance": round(memory_relevance, 3),
            "env_suitability": env_suitability,
        }

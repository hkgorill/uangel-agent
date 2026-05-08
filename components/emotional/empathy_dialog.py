from components.base_component import BaseComponent
from templates.template_pool import get_template


class EmpathyDialog(BaseComponent):
    name = "empathy_dialog"
    category = "emotional"
    description = "어르신의 감정에 공감하며 대화를 이어나간다."

    def execute(self, context: dict) -> dict:
        ev = context.get("emotion_vector", {})
        dominant = max(ev, key=ev.get) if ev else "외로움"
        situation_map = {"sadness": "슬픔", "loneliness": "외로움", "anxiety": "불안"}
        situation = situation_map.get(dominant, "공감일반")
        utterance = get_template("공감", tone="따뜻함", situation=situation)
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        ev = context.get("emotion_vector", {})
        neg = ev.get("sadness", 0) + ev.get("loneliness", 0) + ev.get("anxiety", 0)
        emotion_match = min(1.0, neg / 1.5)
        topics = context.get("memory_data", {}).get("recent_topics", [])
        memory_relevance = 0.5
        return {
            "emotion_match": round(emotion_match, 3),
            "memory_relevance": memory_relevance,
            "env_suitability": 0.8,
        }

from components.base_component import BaseComponent
from templates.template_pool import get_template


class FamilyContact(BaseComponent):
    name = "family_contact"
    category = "social"
    description = "가족 연락 유도."

    def execute(self, context: dict) -> dict:
        topics = context.get("memory_data", {}).get("recent_topics", [])
        family_keywords = ["손녀", "아들", "딸", "손자", "가족", "며느리", "사위"]
        has_family = any(k in t for t in topics for k in family_keywords)
        situation = "가족언급" if has_family else "가족일반"
        utterance = get_template("가족", tone="따뜻함", situation=situation)
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        topics = context.get("memory_data", {}).get("recent_topics", [])
        family_keywords = ["손녀", "아들", "딸", "손자", "가족", "며느리", "사위", "전화"]
        has_family = any(k in t for t in topics for k in family_keywords)
        memory_relevance = 0.95 if has_family else 0.2
        loneliness = context.get("emotion_vector", {}).get("loneliness", 0.0)
        last_positive = context.get("memory_data", {}).get("last_positive_response", "")
        # 과거에 가족 연락이 효과적이었다면 감정 매칭 가중
        emotion_boost = 0.15 if last_positive == "family_contact" else 0.0
        emotion_match = min(1.0, loneliness + emotion_boost)
        env_suitability = (0.85 if (has_family and last_positive == "family_contact")
                           else (0.8 if has_family else 0.7))
        return {
            "emotion_match": round(emotion_match, 3),
            "memory_relevance": memory_relevance,
            "env_suitability": env_suitability,
        }

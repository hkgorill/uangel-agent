from components.base_component import BaseComponent
from templates.template_pool import get_template


class Stabilization(BaseComponent):
    name = "stabilization"
    category = "emotional"
    description = "불안 상태를 안정시키는 호흡·심리 안정 안내."

    def execute(self, context: dict) -> dict:
        utterance = get_template("안정", tone="차분함", situation="심호흡")
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        anxiety = context.get("emotion_vector", {}).get("anxiety", 0.0)
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        # 야간 불안이 핵심 트리거 — 밤에는 안정화가 가장 적합
        env_suitability = 1.0 if tod in ("night", "midnight") else 0.3
        # 불안 수준이 기억 관련도를 대리 (어르신이 안정을 필요로 한다는 신호)
        return {
            "emotion_match": round(anxiety, 3),
            "memory_relevance": round(anxiety, 3),
            "env_suitability": env_suitability,
        }

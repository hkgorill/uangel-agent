"""Score Engine — 14종 동적 컴포넌트 점수 계산 및 순위 반환."""

import logging
import time

logger = logging.getLogger(__name__)

# 동적 컴포넌트 목록 (Rule Engine 전용 3종 제외)
DYNAMIC_COMPONENTS = [
    "empathy_dialog",
    "emotion_reflection",
    "mood_change",
    "stabilization",
    "positive_sharing",
    "medication_reminder",
    "meal_guide",
    "sleep_monitor",
    "weather_info",
    "schedule_manager",
    "family_contact",
    "network_maintain",
    "encouragement",
    "cognitive_stimulation",
    "physical_activity",
    "play_agent",
    "generative_agent",
]


class ScoreEngine:
    def __init__(self):
        self.weights = {
            "emotion_match": 0.4,
            "memory_relevance": 0.3,
            "env_suitability": 0.2,
            "unused_bonus": 0.1,
        }
        self._last_used: dict[str, float] = {}

    def _unused_bonus(self, component_name: str) -> float:
        last = self._last_used.get(component_name)
        if last is None:
            return 1.0
        elapsed_hours = (time.time() - last) / 3600
        return min(1.0, elapsed_hours / 24.0)

    def compute_score(self, component_name: str, factors: dict) -> float:
        w = self.weights
        score = (
            factors.get("emotion_match", 0.0) * w["emotion_match"]
            + factors.get("memory_relevance", 0.0) * w["memory_relevance"]
            + factors.get("env_suitability", 0.0) * w["env_suitability"]
            + self._unused_bonus(component_name) * w["unused_bonus"]
        )
        return round(score, 4)

    def rank_components(self, context: dict, registry: dict) -> list[tuple[str, float]]:
        """registry: {component_name: BaseComponent 인스턴스}
        Returns: [(component_name, score), ...] 내림차순
        """
        scores = []
        for name, comp in registry.items():
            if name not in DYNAMIC_COMPONENTS:
                continue
            try:
                factors = comp.get_score_factors(context)
            except Exception as e:
                logger.warning("Score factor error for %s: %s", name, e)
                factors = {}
            score = self.compute_score(name, factors)
            scores.append((name, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    def update_weights(self, delta: dict):
        """피드백 엔진이 호출 — 가중치 소폭 갱신."""
        lr = 0.01
        for key, adjustment in delta.items():
            if key in self.weights:
                self.weights[key] = round(
                    max(0.0, min(1.0, self.weights[key] + lr * adjustment)), 4
                )

    def mark_used(self, component_name: str):
        self._last_used[component_name] = time.time()

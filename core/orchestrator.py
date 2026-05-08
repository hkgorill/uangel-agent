"""오케스트레이션 메인 엔진."""

import logging
from datetime import datetime

from core.rule_engine import RuleEngine
from core.score_engine import ScoreEngine

logger = logging.getLogger(__name__)


class Orchestrator:
    def __init__(self, registry: dict):
        self.registry = registry
        self.rule_engine = RuleEngine()
        self.score_engine = ScoreEngine()

    def run(self, context: dict) -> dict:
        """컨텍스트를 받아 적절한 컴포넌트를 선택·실행하고 결과를 반환한다."""
        # 1. Rule Engine — 위기 즉각 대응
        crisis_components = self.rule_engine.evaluate(context)
        if crisis_components:
            logger.info("Crisis intervention: %s", crisis_components)
            if len(crisis_components) == 1:
                return self._execute_component(crisis_components[0], context, mode="rule")
            return self._execute_composite(crisis_components, context)

        # 2. Score Engine — 상위 3개 후보 선택
        ranked = self.score_engine.rank_components(context, self.registry)
        top3 = ranked[:3]
        logger.info("Score top3: %s", top3)

        if not top3:
            return {"error": "No suitable component found", "success": False}

        # 3. 최고 점수 컴포넌트 실행
        best_name, best_score = top3[0]
        result = self._execute_component(best_name, context, mode="score")
        result["score"] = best_score
        result["candidates"] = top3
        return result

    def _execute_composite(self, names: list[str], context: dict) -> dict:
        """복수 컴포넌트를 순서대로 실행하고 결과를 합산한다."""
        results = []
        utterances = []
        for name in names:
            comp = self.registry.get(name)
            if not comp:
                logger.warning("Composite: component not found — %s", name)
                continue
            r = comp.execute(context)
            results.append(r)
            if r.get("utterance"):
                utterances.append(r["utterance"])
            self.score_engine.mark_used(name)
            logger.info("Composite executed: %s | utterance: %s", name, r.get("utterance", ""))

        ts = datetime.now().isoformat()
        user_id = context.get("user_id", "unknown")
        return {
            "component": names[0],
            "components": names,
            "utterance": " ".join(utterances),
            "results": results,
            "mode": "rule",
            "timestamp": ts,
            "user_id": user_id,
            "success": any(r.get("success") for r in results),
        }

    def _execute_component(self, name: str, context: dict, mode: str) -> dict:
        comp = self.registry.get(name)
        if not comp:
            logger.error("Component not found: %s", name)
            return {"error": f"Component '{name}' not in registry", "success": False}
        result = comp.execute(context)
        result["mode"] = mode
        result["timestamp"] = datetime.now().isoformat()
        result["user_id"] = context.get("user_id", "unknown")
        self.score_engine.mark_used(name)
        logger.info("Executed: %s | utterance: %s", name, result.get("utterance", ""))
        return result

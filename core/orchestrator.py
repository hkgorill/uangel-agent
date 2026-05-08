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
        crisis_component = self.rule_engine.evaluate(context)
        if crisis_component:
            logger.info("Crisis intervention: %s", crisis_component)
            return self._execute_component(crisis_component, context, mode="rule")

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

"""Rule Engine — 위기 상황 즉각 대응 6종 조건 판별."""

import logging

logger = logging.getLogger(__name__)

_RULES: list = []


def _rule(fn):
    _RULES.append(fn)
    return fn


@_rule
def _fall_detected(ctx: dict) -> list[str]:
    if ctx.get("bio_data", {}).get("fall_detected") is True:
        return ["anomaly_detection", "escalation", "family_contact"]
    return []


@_rule
def _no_movement(ctx: dict) -> list[str]:
    if ctx.get("bio_data", {}).get("no_movement_minutes", 0) >= 240:
        return ["anomaly_detection", "escalation"]
    return []


@_rule
def _crisis_utterance(ctx: dict) -> list[str]:
    if ctx.get("crisis_flags", {}).get("crisis_utterance") is True:
        return ["escalation", "empathy_dialog", "family_contact"]
    return []


@_rule
def _heart_rate_abnormal(ctx: dict) -> list[str]:
    hr = ctx.get("bio_data", {}).get("heart_rate", 72)
    if hr > 120 or hr < 40:
        return ["anomaly_detection", "escalation"]
    return []


@_rule
def _isolation_risk(ctx: dict) -> list[str]:
    if ctx.get("crisis_flags", {}).get("isolation_risk_score", 0.0) >= 0.9:
        return ["isolation_risk", "escalation", "family_contact"]
    return []


@_rule
def _sos_activated(ctx: dict) -> list[str]:
    if ctx.get("crisis_flags", {}).get("sos_activated") is True:
        return ["escalation", "family_contact"]
    return []


class RuleEngine:
    def evaluate(self, context: dict) -> list[str]:
        """위기 조건 검사. 실행할 컴포넌트 목록 반환. 위기 없으면 빈 리스트."""
        for rule_fn in _RULES:
            components = rule_fn(context)
            if components:
                logger.info("Rule triggered: %s → %s", rule_fn.__name__, components)
                return components
        return []

"""Rule Engine — 위기 상황 즉각 대응 6종 조건 판별."""

import logging

logger = logging.getLogger(__name__)

# (조건 체크 함수, 반환할 컴포넌트 이름) 순서 쌍
_RULES: list[tuple] = []


def _rule(fn):
    _RULES.append(fn)
    return fn


@_rule
def _fall_detected(ctx: dict) -> str | None:
    if ctx.get("bio_data", {}).get("fall_detected") is True:
        return "anomaly_detection"
    return None


@_rule
def _no_movement(ctx: dict) -> str | None:
    if ctx.get("bio_data", {}).get("no_movement_minutes", 0) >= 240:
        return "anomaly_detection"
    return None


@_rule
def _crisis_utterance(ctx: dict) -> str | None:
    if ctx.get("crisis_flags", {}).get("crisis_utterance") is True:
        return "escalation"
    return None


@_rule
def _heart_rate_abnormal(ctx: dict) -> str | None:
    hr = ctx.get("bio_data", {}).get("heart_rate", 72)
    if hr > 120 or hr < 40:
        return "anomaly_detection"
    return None


@_rule
def _isolation_risk(ctx: dict) -> str | None:
    if ctx.get("crisis_flags", {}).get("isolation_risk_score", 0.0) >= 0.9:
        return "isolation_risk"
    return None


@_rule
def _sos_activated(ctx: dict) -> str | None:
    if ctx.get("crisis_flags", {}).get("sos_activated") is True:
        return "escalation"
    return None


class RuleEngine:
    def evaluate(self, context: dict) -> str | None:
        """위기 조건 검사. 해당 컴포넌트명 또는 None 반환."""
        for rule_fn in _RULES:
            result = rule_fn(context)
            if result:
                logger.info("Rule triggered: %s → %s", rule_fn.__name__, result)
                return result
        return None

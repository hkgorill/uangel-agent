import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.rule_engine import RuleEngine


def _base_context():
    return {
        "user_id": "test",
        "emotion_vector": {},
        "memory_data": {},
        "bio_data": {"heart_rate": 72, "no_movement_minutes": 0, "fall_detected": False},
        "env_data": {},
        "crisis_flags": {"crisis_utterance": False, "sos_activated": False, "isolation_risk_score": 0.0},
    }


re = RuleEngine()


def test_fall_detected():
    ctx = _base_context()
    ctx["bio_data"]["fall_detected"] = True
    result = re.evaluate(ctx)
    assert "anomaly_detection" in result
    assert "escalation" in result
    assert "family_contact" in result


def test_no_movement():
    ctx = _base_context()
    ctx["bio_data"]["no_movement_minutes"] = 250
    result = re.evaluate(ctx)
    assert "anomaly_detection" in result
    assert "escalation" in result


def test_crisis_utterance():
    ctx = _base_context()
    ctx["crisis_flags"]["crisis_utterance"] = True
    result = re.evaluate(ctx)
    assert "escalation" in result
    assert "empathy_dialog" in result
    assert "family_contact" in result


def test_heart_rate_high():
    ctx = _base_context()
    ctx["bio_data"]["heart_rate"] = 130
    result = re.evaluate(ctx)
    assert "anomaly_detection" in result
    assert "escalation" in result


def test_heart_rate_low():
    ctx = _base_context()
    ctx["bio_data"]["heart_rate"] = 35
    result = re.evaluate(ctx)
    assert "anomaly_detection" in result
    assert "escalation" in result


def test_isolation_risk():
    ctx = _base_context()
    ctx["crisis_flags"]["isolation_risk_score"] = 0.95
    result = re.evaluate(ctx)
    assert "isolation_risk" in result
    assert "escalation" in result
    assert "family_contact" in result


def test_sos():
    ctx = _base_context()
    ctx["crisis_flags"]["sos_activated"] = True
    result = re.evaluate(ctx)
    assert "escalation" in result
    assert "family_contact" in result


def test_no_crisis():
    ctx = _base_context()
    assert re.evaluate(ctx) == []

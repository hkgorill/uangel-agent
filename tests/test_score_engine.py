import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from core.score_engine import ScoreEngine


se = ScoreEngine()


def _factors(emotion=0.5, memory=0.5, env=0.5):
    return {"emotion_match": emotion, "memory_relevance": memory, "env_suitability": env}


def test_score_range():
    score = se.compute_score("empathy_dialog", _factors())
    assert 0.0 <= score <= 1.0


def test_higher_emotion_match_gives_higher_score():
    low = se.compute_score("test_comp_a", _factors(emotion=0.1))
    high = se.compute_score("test_comp_b", _factors(emotion=0.9))
    assert high > low


def test_rank_returns_sorted():
    from components.emotional.empathy_dialog import EmpathyDialog
    from components.emotional.stabilization import Stabilization
    registry = {
        "empathy_dialog": EmpathyDialog(),
        "stabilization": Stabilization(),
    }
    ctx = {
        "emotion_vector": {"sadness": 0.8, "loneliness": 0.7, "anxiety": 0.1, "calm": 0.1, "joy": 0.0},
        "memory_data": {"recent_topics": [], "rapport_score": 0.5},
        "bio_data": {"no_movement_minutes": 10},
        "env_data": {"time_of_day": "afternoon"},
        "crisis_flags": {"isolation_risk_score": 0.0},
    }
    ranked = se.rank_components(ctx, registry)
    scores = [s for _, s in ranked]
    assert scores == sorted(scores, reverse=True)


def test_update_weights():
    original = dict(se.weights)
    se.update_weights({"emotion_match": 1.0})
    assert se.weights["emotion_match"] > original["emotion_match"]

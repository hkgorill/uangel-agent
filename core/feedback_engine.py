"""Feedback Engine — 개입 결과 학습 및 가중치 자동 갱신."""

import logging
from data.db import InterventionLog, FeedbackLog, UserProfile, get_session

logger = logging.getLogger(__name__)

REACTION_SCORES = {
    "continued_conversation": 1.0,
    "positive_emotion_change": 0.8,
    "no_response": 0.0,
    "negative_reaction": -1.0,
}


class FeedbackEngine:
    def __init__(self, score_engine):
        self.score_engine = score_engine

    def record_intervention(self, user_id: str, component: str, utterance: str) -> int:
        """개입 이력 저장 후 log_id 반환."""
        with get_session() as session:
            log = InterventionLog(
                user_id=user_id,
                component=component,
                utterance=utterance,
            )
            session.add(log)
            session.flush()
            log_id = log.id
        return log_id

    def record_feedback(self, log_id: int, user_id: str, component: str, reaction: str):
        """반응 평가 기록 + 가중치 갱신."""
        score = REACTION_SCORES.get(reaction, 0.0)
        with get_session() as session:
            fb = FeedbackLog(
                intervention_log_id=log_id,
                user_id=user_id,
                component=component,
                reaction=reaction,
                score=score,
            )
            session.add(fb)
            self._update_user_profile(session, user_id, component, score)

        # Score Engine 글로벌 가중치 소폭 갱신
        adjustment = score * 0.1
        self.score_engine.update_weights({
            "emotion_match": adjustment,
            "memory_relevance": adjustment,
        })
        logger.info("Feedback recorded: %s / %s / %.1f", component, reaction, score)

    def _update_user_profile(self, session, user_id: str, component: str, score: float):
        profile = session.query(UserProfile).filter_by(
            user_id=user_id, component=component
        ).first()
        lr = 0.01
        if profile:
            profile.weight = round(
                max(0.0, min(1.0, profile.weight + lr * score)), 4
            )
        else:
            session.add(UserProfile(
                user_id=user_id,
                component=component,
                weight=round(0.5 + lr * score, 4),
            ))

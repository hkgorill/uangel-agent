"""FastAPI 서버 — 외부 컨텍스트 수신 및 오케스트레이터 실행."""

import os
import logging
from typing import Optional, Literal

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from data.db import init_db, get_session, InterventionLog, FeedbackLog, UserProfile
from components import REGISTRY
from core.orchestrator import Orchestrator
from core.feedback_engine import FeedbackEngine, REACTION_SCORES

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API Key 인증 설정
_API_SECRET_KEY = os.getenv("API_SECRET_KEY", "dev-secret-change-in-production")
_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def verify_api_key(key: str = Security(_api_key_header)):
    """X-API-Key 헤더 검증. 개발 환경(dev-secret-*)은 항상 허용."""
    if key == _API_SECRET_KEY or _API_SECRET_KEY.startswith("dev-secret"):
        return key
    raise HTTPException(status_code=403, detail="유효하지 않은 API 키")


app = FastAPI(
    title="유엔젤 에이전틱 AI API",
    description="고령자 특화 멀티에이전트 오케스트레이션 엔진",
    version="2.0.0",
)

init_db()
orchestrator = Orchestrator(REGISTRY)
feedback_engine = FeedbackEngine(orchestrator.score_engine)


# ── 요청 스키마 ────────────────────────────────────────────

class EmotionVector(BaseModel):
    sadness: float = 0.0
    loneliness: float = 0.0
    anxiety: float = 0.0
    calm: float = 0.5
    joy: float = 0.0


class MemoryData(BaseModel):
    recent_topics: list[str] = []
    rapport_score: float = 0.5
    last_positive_response: Optional[str] = None


class BioData(BaseModel):
    heart_rate: int = 72
    no_movement_minutes: int = 0
    fall_detected: bool = False


class EnvData(BaseModel):
    time_of_day: str = "afternoon"
    weather: str = "sunny"
    location: str = "home"


class CrisisFlags(BaseModel):
    crisis_utterance: bool = False
    sos_activated: bool = False
    isolation_risk_score: float = 0.0


class InterventionRequest(BaseModel):
    user_id: str
    emotion_vector: EmotionVector = EmotionVector()
    memory_data: MemoryData = MemoryData()
    bio_data: BioData = BioData()
    env_data: EnvData = EnvData()
    crisis_flags: CrisisFlags = CrisisFlags()


class FeedbackRequest(BaseModel):
    log_id: int
    user_id: str
    component: str
    reaction: Literal[
        "continued_conversation",
        "positive_emotion_change",
        "no_response",
        "negative_reaction",
    ]


# ── 엔드포인트 ────────────────────────────────────────────

@app.get("/status")
def status():
    """시스템 상태 확인 (인증 불필요)."""
    return {
        "status": "ok",
        "version": "2.0.0",
        "components_loaded": len(REGISTRY),
        "mock_api": os.getenv("USE_MOCK_API", "true").lower() != "false",
        "component_names": list(REGISTRY.keys()),
    }


@app.post("/intervention", dependencies=[Depends(verify_api_key)])
def intervention(req: InterventionRequest):
    """외부 컨텍스트 수신 → 오케스트레이터 실행 → 결과 반환."""
    context = req.model_dump()
    try:
        result = orchestrator.run(context)
    except Exception as e:
        logger.error("Orchestrator error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

    with get_session() as session:
        log = InterventionLog(
            user_id=req.user_id,
            component=result.get("component", "unknown"),
            utterance=result.get("utterance", ""),
        )
        session.add(log)
        session.flush()
        log_id = log.id

    result["log_id"] = log_id
    return result


@app.post("/feedback", dependencies=[Depends(verify_api_key)])
def feedback(req: FeedbackRequest):
    """개입 결과 피드백 수신 → 가중치 자동 갱신.

    reaction 값:
    - continued_conversation  : 대화 지속 (+1.0)
    - positive_emotion_change : 긍정 감정 변화 (+0.8)
    - no_response             : 무반응 (0.0)
    - negative_reaction       : 거부·부정 반응 (-1.0)
    """
    with get_session() as session:
        log = session.query(InterventionLog).filter_by(id=req.log_id).first()
        if not log:
            raise HTTPException(status_code=404, detail=f"log_id {req.log_id} 없음")

    feedback_engine.record_feedback(
        log_id=req.log_id,
        user_id=req.user_id,
        component=req.component,
        reaction=req.reaction,
    )
    return {
        "ok": True,
        "log_id": req.log_id,
        "component": req.component,
        "reaction": req.reaction,
        "score": REACTION_SCORES[req.reaction],
        "weights": orchestrator.score_engine.weights,
    }


@app.get("/feedback", dependencies=[Depends(verify_api_key)])
def feedback_logs(user_id: Optional[str] = None, limit: int = 20):
    """피드백 이력 조회."""
    with get_session() as session:
        query = session.query(FeedbackLog)
        if user_id:
            query = query.filter(FeedbackLog.user_id == user_id)
        rows = query.order_by(FeedbackLog.id.desc()).limit(limit).all()
        return [
            {
                "id": r.id,
                "log_id": r.intervention_log_id,
                "user_id": r.user_id,
                "component": r.component,
                "reaction": r.reaction,
                "score": r.score,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]


@app.get("/profile/{user_id}", dependencies=[Depends(verify_api_key)])
def profile(user_id: str):
    """어르신별 개인화 가중치 프로파일 조회."""
    with get_session() as session:
        rows = session.query(UserProfile).filter_by(user_id=user_id).all()
        if not rows:
            raise HTTPException(status_code=404, detail=f"user_id '{user_id}' 프로파일 없음")
        return {
            "user_id": user_id,
            "global_weights": orchestrator.score_engine.weights,
            "component_weights": {r.component: r.weight for r in rows},
        }


@app.get("/logs", dependencies=[Depends(verify_api_key)])
def logs(user_id: Optional[str] = None, limit: int = 20):
    """최근 개입 이력 조회."""
    with get_session() as session:
        query = session.query(InterventionLog)
        if user_id:
            query = query.filter(InterventionLog.user_id == user_id)
        rows = query.order_by(InterventionLog.id.desc()).limit(limit).all()
        return [
            {
                "id": r.id,
                "user_id": r.user_id,
                "component": r.component,
                "utterance": r.utterance,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rows
        ]

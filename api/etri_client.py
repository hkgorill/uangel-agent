"""ETRI 정서 인지 API 클라이언트."""

import os
import logging
import requests

logger = logging.getLogger(__name__)

ETRI_API_URL = os.getenv("ETRI_API_URL", "")
ETRI_API_KEY = os.getenv("ETRI_API_KEY", "")


class ETRIClient:
    """ETRI 정서 인지 실제 API 클라이언트.

    환경변수 설정:
        ETRI_API_URL: ETRI API 엔드포인트
        ETRI_API_KEY: ETRI 발급 API 키
    """

    def get_emotion_vector(self, user_id: str, text: str = "") -> dict:
        headers = {"Authorization": f"Bearer {ETRI_API_KEY}"}
        payload = {"user_id": user_id, "text": text}
        try:
            resp = requests.post(
                f"{ETRI_API_URL}/emotion",
                json=payload,
                headers=headers,
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "sadness":   float(data.get("sadness", 0.0)),
                "loneliness": float(data.get("loneliness", 0.0)),
                "anxiety":   float(data.get("anxiety", 0.0)),
                "calm":      float(data.get("calm", 0.5)),
                "joy":       float(data.get("joy", 0.0)),
            }
        except Exception as e:
            logger.error("ETRI API error: %s", e)
            raise

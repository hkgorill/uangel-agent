"""EICT 장기기억 API 클라이언트."""

import os
import logging
import requests

logger = logging.getLogger(__name__)

EICT_API_URL = os.getenv("EICT_API_URL", "")
EICT_API_KEY = os.getenv("EICT_API_KEY", "")


class EICTClient:
    """EICT 장기기억 실제 API 클라이언트.

    환경변수 설정:
        EICT_API_URL: EICT API 엔드포인트
        EICT_API_KEY: EICT 발급 API 키
    """

    def get_memory_data(self, user_id: str) -> dict:
        headers = {"Authorization": f"Bearer {EICT_API_KEY}"}
        try:
            resp = requests.get(
                f"{EICT_API_URL}/memory/{user_id}",
                headers=headers,
                timeout=5,
            )
            resp.raise_for_status()
            data = resp.json()
            return {
                "recent_topics":          data.get("recent_topics", []),
                "rapport_score":          float(data.get("rapport_score", 0.5)),
                "last_positive_response": data.get("last_positive_response"),
            }
        except Exception as e:
            logger.error("EICT API error: %s", e)
            raise

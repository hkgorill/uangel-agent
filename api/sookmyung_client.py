"""숙명여대 라포 API 클라이언트."""

import os
import logging
import requests

logger = logging.getLogger(__name__)

SOOKMYUNG_API_URL = os.getenv("SOOKMYUNG_API_URL", "")
SOOKMYUNG_API_KEY = os.getenv("SOOKMYUNG_API_KEY", "")


class SookmyungClient:
    """숙명여대 라포 측정 실제 API 클라이언트.

    환경변수 설정:
        SOOKMYUNG_API_URL: 숙명여대 API 엔드포인트
        SOOKMYUNG_API_KEY: 발급 API 키
    """

    def get_rapport_score(self, user_id: str) -> float:
        headers = {"Authorization": f"Bearer {SOOKMYUNG_API_KEY}"}
        try:
            resp = requests.get(
                f"{SOOKMYUNG_API_URL}/rapport/{user_id}",
                headers=headers,
                timeout=5,
            )
            resp.raise_for_status()
            return float(resp.json().get("rapport_score", 0.5))
        except Exception as e:
            logger.error("Sookmyung API error: %s", e)
            raise

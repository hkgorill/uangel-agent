"""개발용 Mock API 클라이언트 — 실제 API 연동 전 테스트에 사용."""

import random
from datetime import datetime


class MockETRIClient:
    """ETRI 정서 인지 API Mock."""

    def get_emotion_vector(self, user_id: str, text: str = "") -> dict:
        base = {
            "sadness": round(random.uniform(0.1, 0.9), 2),
            "loneliness": round(random.uniform(0.1, 0.9), 2),
            "anxiety": round(random.uniform(0.0, 0.5), 2),
            "calm": round(random.uniform(0.1, 0.8), 2),
            "joy": round(random.uniform(0.0, 0.5), 2),
        }
        return base


class MockEICTClient:
    """EICT 장기기억 API Mock."""

    _topics_pool = [
        ["손녀", "날씨", "무릎 통증"],
        ["정원 가꾸기", "옛날 노래", "친구"],
        ["아들", "텔레비전", "밥"],
        ["병원", "약", "수면"],
    ]

    def get_memory_data(self, user_id: str) -> dict:
        return {
            "recent_topics": random.choice(self._topics_pool),
            "rapport_score": round(random.uniform(0.4, 0.95), 2),
            "last_positive_response": random.choice(
                ["family_contact", "empathy_dialog", "meal_guide", None]
            ),
        }


class MockSookmyungClient:
    """숙명여대 라포 API Mock."""

    def get_rapport_score(self, user_id: str) -> float:
        return round(random.uniform(0.3, 0.95), 2)


etri_client = MockETRIClient()
eict_client = MockEICTClient()
sookmyung_client = MockSookmyungClient()

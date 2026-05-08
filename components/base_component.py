from abc import ABC, abstractmethod
from typing import Any
import logging

logger = logging.getLogger(__name__)


class BaseComponent(ABC):
    """모든 행동 컴포넌트의 공통 인터페이스."""

    name: str = ""
    category: str = ""
    description: str = ""

    def __init__(self):
        self.last_executed_at: float | None = None

    @abstractmethod
    def execute(self, context: dict) -> dict:
        """컴포넌트를 실행하고 결과를 반환한다.

        Returns:
            {
                "component": str,        # 컴포넌트 이름
                "utterance": str,        # 발화 문장
                "action": str | None,    # 부가 액션 (알림 발송 등)
                "success": bool
            }
        """

    @abstractmethod
    def get_score_factors(self, context: dict) -> dict:
        """Score Engine이 사용할 점수 인자를 반환한다.

        Returns:
            {
                "emotion_match": float,      # 0.0 ~ 1.0
                "memory_relevance": float,   # 0.0 ~ 1.0
                "env_suitability": float,    # 0.0 ~ 1.0
            }
        """

    def _build_result(self, utterance: str, action: str | None = None, success: bool = True) -> dict:
        import time
        self.last_executed_at = time.time()
        return {
            "component": self.name,
            "utterance": utterance,
            "action": action,
            "success": success,
        }

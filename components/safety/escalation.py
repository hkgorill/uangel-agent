import logging
from components.base_component import BaseComponent
from templates.template_pool import get_template

logger = logging.getLogger(__name__)


class Escalation(BaseComponent):
    name = "escalation"
    category = "safety"
    description = "위기 발화 또는 SOS 시 보호자 즉각 연락."

    def execute(self, context: dict) -> dict:
        user_id = context.get("user_id", "unknown")
        utterance = get_template("위기", situation="SOS")
        # 실제 연락 발송은 Mock — 인터페이스만 구현
        self._send_guardian_alert(user_id, context)
        return self._build_result(utterance, action="GUARDIAN_NOTIFIED")

    def get_score_factors(self, context: dict) -> dict:
        return {"emotion_match": 0.0, "memory_relevance": 0.0, "env_suitability": 0.0}

    def _send_guardian_alert(self, user_id: str, context: dict):
        logger.warning(
            "[MOCK ALERT] 보호자 알림 발송 — user_id=%s, crisis_flags=%s",
            user_id,
            context.get("crisis_flags"),
        )

from components.base_component import BaseComponent
from templates.template_pool import get_template


class ScheduleManager(BaseComponent):
    name = "schedule_manager"
    category = "daily"
    description = "일정 안내 및 준비 도움."

    def execute(self, context: dict) -> dict:
        utterance = get_template("일상", tone="따뜻함", situation="일정")
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        env_suitability = 0.8 if tod == "morning" else 0.4
        return {
            "emotion_match": 0.2,
            "memory_relevance": 0.5,
            "env_suitability": env_suitability,
        }

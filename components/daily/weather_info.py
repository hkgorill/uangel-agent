from components.base_component import BaseComponent
from templates.template_pool import get_template


class WeatherInfo(BaseComponent):
    name = "weather_info"
    category = "daily"
    description = "날씨 정보 안내."

    def execute(self, context: dict) -> dict:
        weather = context.get("env_data", {}).get("weather", "맑음")
        situation = "날씨흐림" if weather in ("cloudy", "rainy") else "날씨"
        utterance = get_template("일상", situation=situation)
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        tod = context.get("env_data", {}).get("time_of_day", "afternoon")
        env_suitability = 0.7 if tod == "morning" else 0.3
        return {
            "emotion_match": 0.2,
            "memory_relevance": 0.2,
            "env_suitability": env_suitability,
        }

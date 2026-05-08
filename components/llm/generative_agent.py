import logging
from components.base_component import BaseComponent

logger = logging.getLogger(__name__)


class GenerativeAgent(BaseComponent):
    name = "generative_agent"
    category = "llm"
    description = "Gemini를 이용한 맥락 기반 생성 대화."

    def __init__(self):
        super().__init__()
        self._llm = None

    def _get_llm(self):
        if self._llm is None:
            from langchain_google_genai import ChatGoogleGenerativeAI
            self._llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        return self._llm

    def execute(self, context: dict) -> dict:
        ev = context.get("emotion_vector", {})
        dominant_emotion = max(ev, key=ev.get) if ev else "평온"
        emotion_kr = {
            "sadness": "슬픔", "loneliness": "외로움",
            "anxiety": "불안", "calm": "평온", "joy": "기쁨"
        }.get(dominant_emotion, dominant_emotion)
        prompt = (
            f"당신은 고령자를 위한 공감 AI입니다. "
            f"지금 어르신의 감정 상태는 '{emotion_kr}'입니다. "
            f"그 감정에 맞는 따뜻하고 공감적인 말 한 문장을 건네주세요."
        )
        try:
            llm = self._get_llm()
            response = llm.invoke(prompt)
            utterance = response.content.strip()
        except Exception as e:
            logger.error("GenerativeAgent LLM error: %s", e)
            utterance = "오늘 하루도 함께여서 좋아요. 무슨 이야기든 들어드릴게요."
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        rapport = context.get("memory_data", {}).get("rapport_score", 0.5)
        ev = context.get("emotion_vector", {})
        emotion_intensity = max(ev.values()) if ev else 0.5
        return {
            "emotion_match": round(emotion_intensity, 3),
            "memory_relevance": round(rapport, 3),
            "env_suitability": 0.7,
        }

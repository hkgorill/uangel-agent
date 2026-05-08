import os
import logging
from components.base_component import BaseComponent

logger = logging.getLogger(__name__)


class PlayAgent(BaseComponent):
    name = "play_agent"
    category = "llm"
    description = "Gemini를 이용한 자유 대화·놀이 기능."

    def __init__(self):
        super().__init__()
        self._llm = None

    def _get_llm(self):
        if self._llm is None:
            from langchain_google_genai import ChatGoogleGenerativeAI
            self._llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        return self._llm

    def execute(self, context: dict) -> dict:
        topics = context.get("memory_data", {}).get("recent_topics", [])
        topic_str = ", ".join(topics) if topics else "일상 이야기"
        prompt = (
            f"당신은 고령자를 위한 친근한 AI 친구입니다. "
            f"어르신이 좋아하시는 주제({topic_str})와 관련된 "
            f"즐겁고 따뜻한 말 한 마디를 한 문장으로 건네주세요."
        )
        try:
            llm = self._get_llm()
            response = llm.invoke(prompt)
            utterance = response.content.strip()
        except Exception as e:
            logger.error("PlayAgent LLM error: %s", e)
            utterance = "오늘도 즐거운 하루 보내고 계신가요? 함께 이야기해요!"
        return self._build_result(utterance)

    def get_score_factors(self, context: dict) -> dict:
        rapport = context.get("memory_data", {}).get("rapport_score", 0.5)
        joy = context.get("emotion_vector", {}).get("joy", 0.0)
        calm = context.get("emotion_vector", {}).get("calm", 0.0)
        positive_state = joy + calm
        # 긍정 상태일 때 놀이·대화 컴포넌트가 가장 적합
        env_suitability = 0.95 if positive_state >= 0.8 else 0.7
        return {
            "emotion_match": round((joy + calm) / 2, 3),
            "memory_relevance": round(rapport, 3),
            "env_suitability": env_suitability,
        }

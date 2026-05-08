"""컴포넌트 레지스트리 — 이름으로 인스턴스 조회."""

from components.emotional.empathy_dialog import EmpathyDialog
from components.emotional.emotion_reflection import EmotionReflection
from components.emotional.mood_change import MoodChange
from components.emotional.stabilization import Stabilization
from components.emotional.positive_sharing import PositiveSharing

from components.daily.medication_reminder import MedicationReminder
from components.daily.meal_guide import MealGuide
from components.daily.sleep_monitor import SleepMonitor
from components.daily.weather_info import WeatherInfo
from components.daily.schedule_manager import ScheduleManager

from components.social.family_contact import FamilyContact
from components.social.network_maintain import NetworkMaintain
from components.social.encouragement import Encouragement

from components.cognitive.cognitive_stimulation import CognitiveStimulation
from components.cognitive.physical_activity import PhysicalActivity

from components.safety.anomaly_detection import AnomalyDetection
from components.safety.isolation_risk import IsolationRisk
from components.safety.escalation import Escalation

from components.llm.play_agent import PlayAgent
from components.llm.generative_agent import GenerativeAgent

_all_classes = [
    EmpathyDialog, EmotionReflection, MoodChange, Stabilization, PositiveSharing,
    MedicationReminder, MealGuide, SleepMonitor, WeatherInfo, ScheduleManager,
    FamilyContact, NetworkMaintain, Encouragement,
    CognitiveStimulation, PhysicalActivity,
    AnomalyDetection, IsolationRisk, Escalation,
    PlayAgent, GenerativeAgent,
]

REGISTRY: dict = {cls().name: cls() for cls in _all_classes}

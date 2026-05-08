"""발화 템플릿 풀 — JSON 파일 로드 및 상황 맞춤 선택."""

import json
import random
from pathlib import Path

_DATA_PATH = Path(__file__).parent / "data" / "templates_v1.json"
_templates: list[dict] = []


def _load():
    global _templates
    if not _templates and _DATA_PATH.exists():
        with open(_DATA_PATH, encoding="utf-8") as f:
            _templates = json.load(f)


def get_template(category: str, tone: str | None = None, situation: str | None = None) -> str:
    _load()
    pool = [t for t in _templates if t.get("category") == category]
    if tone:
        filtered = [t for t in pool if t.get("tone") == tone]
        if filtered:
            pool = filtered
    if situation:
        filtered = [t for t in pool if situation in t.get("situation", "")]
        if filtered:
            pool = filtered
    if not pool:
        return "안녕하세요. 오늘 하루는 어떠세요?"
    return random.choice(pool)["text"]

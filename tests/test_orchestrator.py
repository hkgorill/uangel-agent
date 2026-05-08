"""시나리오 기반 자동화 테스트 — 정상 실행률 측정."""

import sys
import os
import json
import glob

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data.db import init_db
from components import REGISTRY
from core.orchestrator import Orchestrator

init_db()
orchestrator = Orchestrator(REGISTRY)

SCENARIO_DIR = os.path.join(os.path.dirname(__file__), "scenarios")


def load_scenarios():
    paths = sorted(glob.glob(os.path.join(SCENARIO_DIR, "scenario_*.json")))
    scenarios = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            scenarios.append(json.load(f))
    return scenarios


def test_all_scenarios():
    scenarios = load_scenarios()
    assert len(scenarios) > 0, "No scenario files found"

    total = len(scenarios)
    passed = 0
    results = []

    for s in scenarios:
        desc = s["description"]
        context = s["input"]
        expected = s["expected_component"]
        expected_mode = s.get("expected_mode")

        result = orchestrator.run(context)
        actual = result.get("component")
        actual_mode = result.get("mode")
        ok = actual == expected

        # mode 확인 (rule/score)
        if expected_mode and actual_mode != expected_mode:
            ok = False

        if ok:
            passed += 1
        results.append({
            "description": desc,
            "expected": f"{expected}({expected_mode})",
            "actual": f"{actual}({actual_mode})",
            "pass": ok,
        })

    rate = passed / total * 100
    print(f"\n{'='*60}")
    print(f"시나리오 테스트 결과: {passed}/{total} 통과 ({rate:.1f}%)")
    print(f"{'='*60}")
    for r in results:
        status = "PASS" if r["pass"] else "FAIL"
        print(f"[{status}] {r['description']}")
        if not r["pass"]:
            print(f"       expected={r['expected']}, actual={r['actual']}")

    assert rate >= 75.0, f"실행률 {rate:.1f}% — 목표 75% 미달"

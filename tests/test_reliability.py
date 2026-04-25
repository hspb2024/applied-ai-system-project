"""
Reliability test suite for the Glitch Detective AI coach.
Runs scripted scenarios and validates response quality.

Usage:
    python tests/test_reliability.py

Requires ANTHROPIC_API_KEY to be set in your environment.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from ai_coach import get_coaching_hint

SCENARIOS = [
    {
        "name": "Binary searcher (good strategy)",
        "history": [50, 75, 62],
        "low": 1,
        "high": 100,
        "attempts_left": 5,
    },
    {
        "name": "Random guesser (no pattern)",
        "history": [10, 90, 33, 77],
        "low": 1,
        "high": 100,
        "attempts_left": 4,
    },
    {
        "name": "Small stepper (tiny increments)",
        "history": [10, 11, 12, 13],
        "low": 1,
        "high": 100,
        "attempts_left": 4,
    },
    {
        "name": "First guess only (minimal history)",
        "history": [42],
        "low": 1,
        "high": 100,
        "attempts_left": 7,
    },
    {
        "name": "Easy mode guesser",
        "history": [10, 15],
        "low": 1,
        "high": 20,
        "attempts_left": 4,
    },
]


def check_response(hint: str) -> list:
    """Return a list of failed quality checks (empty list = all passed)."""
    failures = []
    if not hint or not hint.strip():
        failures.append("Response is empty")
    if len(hint) < 10:
        failures.append(f"Response too short ({len(hint)} chars)")
    if len(hint) > 600:
        failures.append(f"Response suspiciously long ({len(hint)} chars)")
    # Guardrail: the coach should not raise an exception or return raw error text
    if "Traceback" in hint or "Exception" in hint:
        failures.append("Response contains raw exception text")
    return failures


def run():
    results = []

    for scenario in SCENARIOS:
        print(f"\n--- {scenario['name']} ---")
        print(f"  History: {scenario['history']}  |  Range: {scenario['low']}-{scenario['high']}  |  Attempts left: {scenario['attempts_left']}")

        hint = get_coaching_hint(
            history=scenario["history"],
            low=scenario["low"],
            high=scenario["high"],
            attempts_left=scenario["attempts_left"],
        )

        print(f"  Hint: {hint!r}")

        failures = check_response(hint)
        if failures:
            print(f"  FAIL: {failures}")
            results.append((scenario["name"], "FAIL", failures))
        else:
            print(f"  PASS")
            results.append((scenario["name"], "PASS", []))

    print("\n" + "=" * 48)
    print("RELIABILITY REPORT")
    print("=" * 48)
    passed = sum(1 for _, status, _ in results if status == "PASS")
    total = len(results)
    print(f"Passed: {passed}/{total}\n")

    for name, status, failures in results:
        mark = "PASS" if status == "PASS" else "FAIL"
        print(f"  [{mark}] {name}")
        for f in failures:
            print(f"         -> {f}")

    print()
    if passed < total:
        sys.exit(1)


if __name__ == "__main__":
    run()

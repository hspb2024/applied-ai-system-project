import logging
from pathlib import Path

log_path = Path(__file__).parent / "glitch_detective.log"
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def _detect_strategy(history: list, low: int, high: int) -> str:
    """Classify the player's guessing pattern."""
    if len(history) < 2:
        return "first_guess"

    steps = [abs(history[i] - history[i - 1]) for i in range(1, len(history))]
    avg_step = sum(steps) / len(steps)
    total_range = high - low

    # Tiny increments: average step is less than 5% of the total range
    if avg_step < total_range * 0.05:
        return "small_steps"

    # Binary search: first guess near midpoint AND steps are decreasing
    mid = (low + high) / 2
    first_near_mid = abs(history[0] - mid) < total_range * 0.25
    steps_decreasing = all(steps[i] >= steps[i + 1] for i in range(len(steps) - 1)) if len(steps) > 1 else True
    if first_near_mid and steps_decreasing:
        return "binary_search"

    # Random: high variance in step sizes
    mean_step = avg_step
    variance = sum((s - mean_step) ** 2 for s in steps) / len(steps)
    if variance > (total_range * 0.15) ** 2:
        return "random"

    return "general"


def get_coaching_hint(history: list, low: int, high: int, attempts_left: int) -> str:
    """
    Analyze the player's guess history and return a strategic coaching tip.
    Uses rule-based pattern detection — no API required.
    """
    if not history:
        return ""

    strategy = _detect_strategy(history, low, high)
    total_range = high - low

    logger.info(
        "coach_call history=%s range=(%d,%d) attempts_left=%d strategy=%s",
        history, low, high, attempts_left, strategy,
    )

    if strategy == "first_guess":
        mid = (low + high) // 2
        if history[0] == mid:
            hint = (
                f"Great opening move — starting in the middle of {low}-{high} is the optimal first guess. "
                "Keep halving the remaining range each time!"
            )
        elif history[0] < low + total_range * 0.25 or history[0] > high - total_range * 0.25:
            hint = (
                "Starting near the edges leaves a lot of range uncovered. "
                f"Next time, try opening with {(low + high) // 2} — the midpoint gives you the most information."
            )
        else:
            hint = (
                "Solid first guess. Now use the hint to cut the remaining range in half — "
                "that's the fastest way to narrow it down."
            )

    elif strategy == "binary_search":
        hint = (
            "You're using binary search — the most efficient strategy here! "
            f"With {attempts_left} attempts left, keep halving the remaining range and you'll get there."
        )

    elif strategy == "small_steps":
        ideal_jump = total_range // (attempts_left + len(history))
        hint = (
            f"Your steps are too small for the range {low}-{high}. "
            f"With {attempts_left} attempts left, you need to jump at least {max(ideal_jump, 5)} numbers at a time. "
            "Be bold — small steps won't get you there in time."
        )

    elif strategy == "random":
        hint = (
            "Your guesses look scattered — try a more structured approach. "
            "Pick the midpoint of what's still possible and cut the range in half each time. "
            f"With {attempts_left} attempts left, every guess needs to count."
        )

    else:
        if attempts_left <= 2:
            hint = (
                f"Only {attempts_left} attempt(s) left — think carefully. "
                "Narrow down the exact range that's still possible and aim for the middle of it."
            )
        else:
            hint = (
                f"You have {attempts_left} attempts remaining. "
                "Think about what range is still possible after each hint and always aim for the middle of it."
            )

    logger.info("coach_response hint=%r strategy=%s", hint, strategy)
    return hint

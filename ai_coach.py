import logging
from pathlib import Path

log_path = Path(__file__).parent / "glitch_detective.log"
logging.basicConfig(
    filename=log_path,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def _detect_strategy(history: list, low: int, high: int, outcomes: list) -> str:
    """Classify the player's guessing pattern."""
    if len(history) < 2:
        return "first_guess"

    steps = [abs(history[i] - history[i - 1]) for i in range(1, len(history))]
    avg_step = sum(steps) / len(steps)
    total_range = high - low

    # Wrong direction: player moved opposite to what the last hint said
    if len(outcomes) >= 2:
        prev_outcome = outcomes[-2]
        direction = history[-1] - history[-2]
        if prev_outcome == "Too High" and direction > 0:
            return "wrong_direction"
        if prev_outcome == "Too Low" and direction < 0:
            return "wrong_direction"

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


def get_coaching_hint(history: list, low: int, high: int, attempts_left: int, outcomes: list = None) -> str:
    """
    Analyze the player's guess history and return a strategic coaching tip.
    Uses rule-based pattern detection — no API required.
    """
    if not history:
        return ""

    strategy = _detect_strategy(history, low, high, outcomes or [])
    total_range = high - low

    logger.info(
        "coach_call history=%s range=(%d,%d) attempts_left=%d strategy=%s",
        history, low, high, attempts_left, strategy,
    )

    if strategy == "wrong_direction":
        hint = (
            "That guess moved in the opposite direction of the hint you were given. "
            "Pay close attention to the feedback after each guess and adjust accordingly. "
            f"With {attempts_left} attempts remaining, moving in the right direction is essential."
        )

    elif strategy == "first_guess":
        mid = (low + high) // 2
        if history[0] == mid:
            hint = (
                f"Great opening move. Starting at the midpoint of {low} to {high} is the optimal first guess. "
                "Continue halving the remaining range each time to stay on the right track."
            )
        elif history[0] < low + total_range * 0.25 or history[0] > high - total_range * 0.25:
            hint = (
                "Starting near the edges leaves a large portion of the range uncovered. "
                f"Next time, consider opening with {mid}. The midpoint gives you the most useful information right away."
            )
        else:
            hint = (
                "That is a solid first guess. Use the hint you received to cut the remaining range in half. "
                "That is the fastest way to narrow things down."
            )

    elif strategy == "binary_search":
        hint = (
            "You are employing binary search, which is the optimal strategy for this scenario! "
            f"With {attempts_left} attempts remaining, just continue dividing the current range in half and you will get there."
        )

    elif strategy == "small_steps":
        ideal_jump = total_range // (attempts_left + len(history))
        hint = (
            f"You are making steps that are too small for the range of {low} to {high}. "
            f"With {attempts_left} attempts remaining, you need to jump at least {max(ideal_jump, 5)} numbers per guess. "
            "Take bigger steps, or you will not be able to reach the answer in time."
        )

    elif strategy == "random":
        hint = (
            "It looks like your guesses are all over the place. "
            "Consider taking a more systematic approach. Select the midpoint of the current range and divide it in half each time. "
            f"With {attempts_left} attempts remaining, every guess needs to count."
        )

    else:
        if attempts_left <= 2:
            hint = (
                f"You only have {attempts_left} attempt(s) remaining. Think carefully. "
                "Identify the range that is still possible and aim for the midpoint."
            )
        else:
            hint = (
                f"You have {attempts_left} attempts remaining. "
                "Consider what range is still possible after each hint and always aim for the middle of it."
            )

    logger.info("coach_response hint=%r strategy=%s", hint, strategy)
    return hint

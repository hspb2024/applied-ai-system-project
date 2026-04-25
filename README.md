# Game Glitch Investigator — Applied AI System

## Original Project

This project builds on **Game Glitch Investigator** from Module 1. The original was a broken number-guessing game built with Streamlit. The goal was to find and fix bugs — including flipped hints, off-by-one scoring, and broken state management. Once the game was fixed, we are able to reflect on the usage of AI to assist in our works.

---

## What This Project Does

**Game Glitch Investigator: AI Coach Edition** adds a live strategy coach to the original game. After each guess, the **Glitch Detective** analyzes the player's guess history, classifies their strategy (binary search, random guessing, small increments), and gives a personalized coaching tip. It also includes a reliability testing suite to make sure the coach behaves consistently.

---

## How It's Organized

The system has three layers:

- **Game Layer** (`app.py` + `logic_utils.py`): Handles input, game state, scoring, and win/loss logic. No AI here.
- **AI Coach Layer** (`ai_coach.py`): After each valid guess, analyzes the guess history using rule-based pattern detection and returns a coaching tip. Every call is logged to `glitch_detective.log`.
- **Testing Layer** (`tests/test_reliability.py`): Runs the AI coach through scripted scenarios and checks that responses are valid.

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/hspb2024/applied-ai-system-project.git
cd applied-ai-system-project
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate       # Mac/Linux
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

### 5. Run unit tests (optional)

```bash
pytest tests/test_game_logic.py
```

### 6. Run AI reliability tests (optional)

```bash
python tests/test_reliability.py
```

---

## Sample Interactions

**Example 1 — Random guesser**
Guesses: `[10, 90, 33, 77]` | Range: 1–100 | 4 attempts left

> "Your guesses look scattered — try a more structured approach. Pick the midpoint of what's still possible and cut the range in half each time. With 4 attempts left, every guess needs to count."

---

**Example 2 — Small stepper**
Guesses: `[10, 11, 12, 13]` | Range: 1–100 | 4 attempts left

> "Your steps are too small for the range 1-100. With 4 attempts left, you need to jump at least 12 numbers at a time. Be bold — small steps won't get you there in time."

---

**Example 3 — Good binary search**
Guesses: `[50, 75, 62]` | Range: 1–100 | 5 attempts left

> "You're using binary search — the most efficient strategy here! With 5 attempts left, keep halving the remaining range and you'll get there."

---

## Design Decisions

**Why rule-based AI instead of a language model API?**
The coaching task is pattern recognition — detecting binary search, random guessing, or small steps. That doesn't require a language model. A rule-based system does it reliably, instantly, and with no API cost or dependency. It also runs offline.

**Why keep game logic and AI coach separate?**
`logic_utils.py` handles deterministic game logic (win/loss/score) while `ai_coach.py` handles strategy analysis. Keeping them separate means the game works even if the coach breaks, and each piece can be tested independently.

**Trade-offs**
- Rule-based hints are deterministic — the same input always produces the same output. This makes testing easier but means the coach can't handle unusual patterns it wasn't designed for.
- A language model would handle edge cases more flexibly, but adds cost, latency, and an external dependency.

---

## Testing Summary

**Unit tests:** 18 tests across `test_game_logic.py` — all pass. Covers input parsing, difficulty ranges, guess outcomes, and scoring.

**Reliability tests:** 5 scenarios run through the AI coach (binary searcher, random guesser, small stepper, first guess only, easy mode). Each response is checked for: non-empty output, reasonable length, and no raw error text. All 5 passed. Because the coach is rule-based with no external dependency, it runs reliably every time with no network or API failures possible.

---

## Reflection

This project made it clear that building with AI is more about design than the model itself. How you structure your logic, how you handle edge cases, and how the output fits into the user experience matter more than picking the most powerful tool.

Adding logging was the most practical lesson. Being able to see every AI call in `glitch_detective.log` meant I could actually verify the system was working — not just assume it was. The reliability tests did the same thing: they gave me evidence instead of just a feeling.

If I extended this further, I'd add an end-of-game summary where the Glitch Detective gives a full breakdown of the player's strategy across all their guesses.

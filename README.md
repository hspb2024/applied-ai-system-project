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

![System Architecture](assets/architecturedesign.png)

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

## Ethics and Critical Reflection

**What are the limitations or biases in your system?**
The Glitch Detective only recognizes four strategy patterns. Any behavior outside those gets generic advice. The detection thresholds were chosen manually and may not work well across all difficulty levels. There is also a bias toward binary search — the coach always nudges players toward it, even if a different approach might be more enjoyable.

**Could your AI be misused, and how would you prevent that?**
The game itself is low-risk, but the log file records every guess history. In a real app, logs should be stored securely and never include personally identifying information. The rule-based system is fully transparent and deterministic, which makes it easier to audit than a black-box model.

**What surprised you during reliability testing?**
The random guesser scenario was initially misclassified as binary search because the step sizes passed a loose threshold. Fixing it required rewriting the detection logic. It was a good reminder that even simple rule-based systems need edge case testing — not just the obvious happy-path scenarios.

**Collaboration with AI during this project**
Claude Code was used throughout to write code, debug errors, and organize the project. One helpful suggestion was separating game logic from the AI coach so the game keeps working even if the coach fails. One flawed suggestion involved an initial strategy detection algorithm that misclassified certain guess patterns — catching and fixing that bug through testing was one of the most valuable parts of the project.


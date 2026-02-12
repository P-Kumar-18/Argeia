# Argeia

Argeia is a schedule and procrastination tracker focused on understanding **behavior over time**, not just managing tasks.

Instead of only tracking *what* needs to be done, Argeia models:
- when tasks were planned
- when they were actually started
- how long they were worked on
- and where procrastination occurs (late start, no start, early stop)

This project is being developed incrementally with a strong emphasis on **clean architecture, testability, and real-world design practices**.

---

## 🚀 Current Features
- Define tasks with planned start and end times
- Track actual task execution (start / completion)
- Detect procrastination signals:
  - start delay
  - underwork
  - timeout
- Analytical signal layer exposing absolute deviations
- Pattern detection layer that interprets repeated signals over time:
  - window-level confirmation
  - pattern polarity (positive / negative)
  - pattern strength (low / high)
- Behavior evaluation layer that:
  - derives sustained improvement across windows
  - determines degradation severity
  - produces structured proposals for the state engine
- Behavioral state engine modeling long-term engagement:
  - Stable → Drifting → Strained → Disengaged
- Behavior evaluator that integrates patterns with the state engine
- Asymmetric behavior model:
  - degradation can occur quickly
  - recovery requires sustained improvement
- Comprehensive unit tests covering signals, patterns, and state transitions

---

## 🧪 Procrastination Model

Argeia currently identifies procrastination through three independent signals:

- **Start Delay** — starting later than scheduled
- **Timeout** — never starting after the planned window ends
- **Underwork** — completing a task earlier than planned

Signals are treated as factual measurements and do not encode severity or judgment.

Each signal is isolated, testable, and designed to be combined later into higher-level insights.

These signals are evaluated over time and combined into higher-level behavioral patterns.
Pattern evidence is interpreted by the behavior evaluation layer, which produces structured proposals (degradation or recovery) for the state engine.

State transitions are intentionally slow-moving and proposal-driven, designed to be fair to one-off mistakes..

Patterns are detected at two levels:
- window-level patterns identify consistent behavior within a bounded set of tasks
- sustained patterns evaluate improvement consistency across multiple windows

Confirmed negative patterns may influence state degradation.
Positive patterns require sustained confirmation across windows before recovery is allowed, ensuring recovery is intentionally slower than degradation.

---

## 🧠 Behavior Model Overview

Argeia models procrastination as a progression of behavioral layers:

Events → Signals → Patterns → Behavior Evaluation → State Engine → Score

- **Signals** measure raw deviations from planned behavior.
- **Patterns** interpret signals over time to detect consistent trends.
- **States** represent long-term engagement and are updated conservatively.

Degradation proposals may move state quickly, while recovery proposals always move state one step at a time and require sustained positive behavior.
This design prevents overreacting to one-off mistakes or short-term improvements.

The behavior evaluation layer resolves conflicts (e.g., simultaneous positive and negative evidence) before proposals reach the state engine.
The state engine does not inspect patterns directly.

---

## 🧱 Project Structure

```
argeia/
├── app/
│   ├── __init__.py                   # Flask app factory
│   ├── main.py                       # Application entry point
│   ├── routes.py                     # Web routes
│   ├── tracker.py                    # Core task & procrastination logic
│   ├── signals.py                    # Analytical signal extraction
│   ├── pattern_detection.py          # Pattern detection
│   ├── behavior_evaluator.py         # Behavior evaluator and state integration
│   └── state_engine.py               # Behavioral state transition engine
├── tests/
│   ├── test_behavior_evaluator.py    # Tests for Behavior Evaluator
│   ├── test_task.py                  # Tests for Task behavior
│   ├── test_signals.py               # Tests for signal extraction
│   ├── test_pattern_detection.py     # Tests for pattern detection
│   └── test_state_transitions.py     # Tests for behavioral state transitions
├── requirements.txt
├── .gitignore
├── DESIGN.md                         # High-level system design
├── docs/
│   ├── behavior_model.md             # Procrastination behavior & state model
│   ├── pattern_model.md              # Patterns model
│   └── state_transition_tests.md     # State tests model
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone <repo-url>
cd argeia
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app/main.py
```

### 5. Tests
```bash
python -m pytest
```

All tests should pass.

---

## 📚 Tech Stack
- Python
- Pytest (testing)
- Flask (app setup in progress)
- SQLite (planned)
- HTML / CSS (planned)

---

## 🎯 Project Status

The behavioral core of Argeia is complete and fully tested.

Implemented:
- Task domain model
- Procrastination signal extraction
- Pattern detection and behavioral evaluation logic
- Proposal-driven behavioral state transitions

---

## 📝 License
This project is for educational purposes.

# Argeia

Argeia is a schedule and procrastination tracker focused on understanding **behavior over time**, not just managing tasks.

Instead of only tracking *what* needs to be done, Argeia models:
- when tasks were planned
- when they were actually started
- how long they were worked on
- where procrastination occurs — late start, early stop, or no start at all

This project is being developed incrementally with a strong emphasis on **clean architecture, testability, and real-world design practices**.

---

## 🚀 Current Features

- Define tasks with planned start and end times
- Track actual task execution — start and completion
- Detect procrastination signals:
  - start delay
  - underwork
  - timeout
- Analytical signal layer exposing absolute deviations from planned behavior
- Pattern detection layer that interprets repeated signals over time:
  - window-level confirmation
  - pattern polarity — positive or negative
  - pattern strength — low or high
- Weekly time windows that bound signal accumulation and pattern detection
- Intra-window pattern batching evaluated every 5 tasks
- Window lifecycle management with automatic closing and reopening
- Behavior evaluation layer that:
  - detects sustained improvement across windows
  - determines degradation severity
  - resolves conflicts between positive and negative evidence
  - produces structured proposals for the state engine
- Asymmetric behavior model:
  - degradation can occur quickly
  - recovery requires sustained improvement across multiple windows
- Behavioral state engine modeling long-term engagement:
  - Stable → Drifting → Strained → Disengaged
- Structured Transition events emitted on accepted state changes
- Persistent history for transitions, windows, and signals via SQLite
- Full state and window reconstruction on startup

---

## 🧪 Procrastination Model

Argeia identifies procrastination through three independent signals:

- **Start Delay** — starting later than scheduled
- **Timeout** — never starting after the planned window ends
- **Underwork** — stopping a task earlier than planned

Signals are treated as factual measurements and do not encode severity or judgment. Each signal is isolated, testable, and feeds into higher-level pattern detection.

Patterns are detected at two levels:
- **Window-level patterns** identify consistent behavior within a bounded set of tasks
- **Sustained patterns** evaluate consistency across multiple windows

Confirmed negative patterns may trigger degradation proposals. Positive patterns require sustained confirmation across windows before a recovery proposal is issued — ensuring recovery is intentionally slower than degradation.

Pattern evidence is interpreted by the behavior evaluation layer, which resolves any conflicts before producing structured proposals for the state engine. State transitions are proposal-driven and intentionally conservative, designed to be fair to one-off mistakes.

---

## 🧠 Behavior Model Overview

Argeia models procrastination as a progression of behavioral layers:

```
Events → Signals → Windows → Pattern Batching → Patterns → Behavior Evaluation → State Engine → Transition Events → Persistence → State Reconstruction
```

- **Signals** measure raw deviations from planned behavior
- **Windows** bound signal accumulation over weekly periods
- **Pattern Batching** detects patterns incrementally every 5 tasks within a window
- **Patterns** interpret accumulated signals to identify consistent behavioral trends
- **Behavior Evaluation** resolves evidence conflicts and produces structured proposals
- **State Engine** updates long-term engagement state conservatively based on proposals
- **Transition Events** capture each state change with full evidence for explainability
- **Persistence** stores transitions, windows, and signals to SQLite
- **State Reconstruction** restores the full behavioral context on restart

The state engine does not inspect patterns directly — it only acts on proposals. This keeps each layer independently testable and decoupled.

State transitions emit structured Transition events capturing:
- previous and new state
- proposal kind and severity
- structured evidence summary
- timestamp

These events form a complete behavioral history and enable explainability without coupling persistence to the state engine.

---

## 🧱 Project Structure

```
argeia/
├── app/
│   ├── infrastructure/
│   │   ├── database.py                 # SQLite connection and schema initialization
│   │   ├── transition_repository.py    # Transition history persistence
│   │   └── window_repository.py        # Window and signal persistence
│   ├── __init__.py                     # Flask app factory
│   ├── behavior_evaluator.py           # Evidence interpretation and proposal generation
│   ├── behavior_runner.py              # Application layer coordinating state engine and persistence
│   ├── main.py                         # Application entry point
│   ├── pattern_detection.py            # Signal interpretation and pattern detection
│   ├── routes.py                       # Web routes
│   ├── signals.py                      # Procrastination signal extraction
│   ├── state_engine.py                 # Behavioral state transition engine
│   ├── tracker.py                      # Core task and procrastination logic
│   ├── window.py                       # Window model and status definitions
│   └── window_manager.py               # Window lifecycle and pattern batching
├── data/
│   └── argeia.db                       # SQLite database
├── docs/
│   ├── behavior_model.md               # Procrastination behavior and state model
│   ├── pattern_model.md                # Pattern detection model
│   └── state_transition_tests.md       # State transition test reference
├── tests/
│   ├── test_behavior_evaluator.py      # Tests for behavior evaluation
│   ├── test_behavior_integration.py    # Integration tests for behavior and state engine
│   ├── test_behavior_runner.py         # Tests for the application runner
│   ├── test_pattern_detection.py       # Tests for pattern detection
│   ├── test_runner_restart.py          # Tests for state reconstruction on restart
│   ├── test_signals.py                 # Tests for signal extraction
│   ├── test_state_transitions.py       # Tests for behavioral state transitions
│   ├── test_task.py                    # Tests for task behavior
│   └── test_windows_implementation.py  # Tests for Window and WindowManager
├── .gitignore
├── DESIGN.md                           # High-level system design
├── README.md
└── requirements.txt
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

### 5. Run tests
```bash
python -m pytest
```

All tests should pass.

---

## 📚 Tech Stack

- Python
- Pytest
- Flask (in progress)
- SQLite
- HTML / CSS (planned)

---

## 🎯 Project Status

The behavioral core is complete. Argeia detects procrastination signals, evaluates behavioral patterns across time windows, drives state transitions through structured proposals, and persists full behavioral history to SQLite with complete reconstruction on restart.

**Implemented:**
- Task domain model with procrastination signal extraction
- Weekly window lifecycle with automatic open/close and restart recovery
- Intra-window pattern batching and signal accumulation
- Pattern detection with polarity and strength classification
- Proposal-driven behavioral state transitions
- Structured transition events for full behavioral explainability
- Persistent storage for transitions, windows, and signals
- Comprehensive unit and integration tests

---

## 📝 License

This project is for educational purposes.
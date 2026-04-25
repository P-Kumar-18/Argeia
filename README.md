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
- Edit and delete upcoming tasks
- Task persistence via SQLite
- Full pipeline entry point through TaskRunner — create, start, and complete tasks
- Detect procrastination signals:
  - start delay
  - underwork
  - timeout (only evaluated after scheduled end time)
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
- Transition evidence stored in a separate normalized table
- Persistent history for transitions, windows, signals, and tasks via SQLite
- Full state and window reconstruction on startup
- Web interface via Flask with server-rendered Jinja2 templates
- CSRF protection via Flask-WTF across all form submissions

---

## 🧪 Procrastination Model

Argeia identifies procrastination through three independent signals:

- **Start Delay** — starting later than scheduled
- **Timeout** — never starting after the planned window ends (only evaluated after scheduled end time)
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
Tasks → Signals → Windows → Pattern Batching → Patterns → Behavior Evaluation → State Engine → Transition Events → Persistence → State Reconstruction
```

- **Signals** measure raw deviations from planned behavior
- **Windows** bound signal accumulation over weekly periods
- **Pattern Batching** detects patterns incrementally every 5 tasks within a window
- **Patterns** interpret accumulated signals to identify consistent behavioral trends
- **Behavior Evaluation** resolves evidence conflicts and produces structured proposals
- **State Engine** updates long-term engagement state conservatively based on proposals
- **Transition Events** capture each state change with full evidence for explainability
- **Persistence** stores transitions, windows, signals, and tasks to SQLite
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
│   ├── core/
│   │   ├── __init__.py
│   │   ├── behavior_evaluator.py       # Evidence interpretation and proposal generation
│   │   ├── pattern_detection.py        # Signal interpretation and pattern detection
│   │   └── state_engine.py             # Behavioral state transition engine
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── signals.py                  # Procrastination signal extraction
│   │   ├── task.py                     # Core task and procrastination logic
│   │   └── window.py                   # Window model and status definitions
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database.py                 # SQLite connection and schema initialization
│   │   ├── task_repository.py          # Task persistence
│   │   ├── transition_repository.py    # Transition history persistence
│   │   └── window_repository.py        # Window and signal persistence
│   ├── runner/
│   │   ├── __init__.py
│   │   ├── behavior_runner.py          # Application layer coordinating state engine and persistence
│   │   ├── task_runner.py              # Task lifecycle and pipeline entry point
│   │   └── window_manager.py           # Window lifecycle and pattern batching
│   ├── web/
│   │   ├── routes/
│   │   │   ├── __init__.py             # Blueprint registration
│   │   │   ├── dashboard.py            # Dashboard route
│   │   │   ├── edit_task.py            # Edit and delete task route
│   │   │   ├── landing.py              # Landing page route
│   │   │   ├── schedule_task.py        # Schedule task route
│   │   │   ├── tasks.py                # All tasks listing route
│   │   │   └── transition_analysis.py  # Transition analysis route
│   │   ├── static/
│   │   │   └── styles.css              # Full application stylesheet
│   │   ├── templates/
│   │   │   ├── dashboard.html          # Dashboard page
│   │   │   ├── edit_task.html          # Edit task form
│   │   │   ├── landing_page.html       # Landing page
│   │   │   ├── layout.html             # Shared base layout
│   │   │   ├── schedule_task.html      # Schedule task form
│   │   │   ├── tasks.html              # All tasks page
│   │   │   └── transition_analysis.html # Analysis page
│   │   └── __init__.py
│   ├── __init__.py                     # Flask app factory
│   └── main.py                         # Application entry point
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
│   ├── test_task_implementation.py     # Tests for TaskRunner and TaskRepository
│   ├── test_task.py                    # Tests for task behavior
│   └── test_windows_implementation.py  # Tests for Window and WindowManager
├── .gitignore
├── DESIGN.md                           # High-level system design
├── LICENSE
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
flask --app main run
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
- Flask
- Flask-WTF
- SQLite
- Jinja2
- HTML / CSS

---

## 🎯 Project Status

**This is the completed v1 of Argeia.** The behavioral core and web interface are fully integrated. Tasks flow from input through signal extraction, window management, pattern detection, behavior evaluation, and state transitions in a single pipeline coordinated by BehaviorRunner, with a complete web UI on top.

Further updates and improvements to Argeia may be made in the future.

**Implemented:**
- Task domain model, persistence, and lifecycle management via TaskRunner
- Task editing and deletion
- Full pipeline integration from task input to state transition via BehaviorRunner
- Comprehensive unit and integration tests
- Weekly window lifecycle with automatic open/close and restart recovery
- Intra-window pattern batching and signal accumulation
- Pattern detection with polarity and strength classification
- Proposal-driven behavioral state transitions
- Structured transition events with normalized evidence persistence
- Persistent storage for transitions, windows, signals, and tasks
- Full state reconstruction on restart
- Flask app factory with blueprint registration and CSRF protection
- Server-rendered web interface with Jinja2
- Landing page, dashboard, task management, and transition analysis pages
- Warm terracotta design system with card layouts and row animations

---

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
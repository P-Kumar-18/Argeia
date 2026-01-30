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
- Detect different forms of procrastination:
  - starting late
  - never starting (timeout)
  - stopping early (underworking)
- Core logic implemented as pure Python domain models
- Comprehensive unit tests for time-based edge cases
- Behavioral state engine modeling long-term engagement:
  - Stable → Drifting → Strained → Disengaged
- State transitions driven by confirmed behavior patterns, not single events
- Symmetry-protected recovery and degradation rules
- Comprehensive unit tests enforcing state transition invariants
- Analytical signal extraction (e.g. start delay, timeout) with unit tests

---

## 🧪 Procrastination Model

Argeia currently identifies procrastination through three independent signals:

- **Start Delay** — starting later than scheduled
- **Timeout** — never starting after the planned window ends
- **Underwork** — completing a task earlier than planned

Each signal is isolated, testable, and designed to be combined later into higher-level insights.

These signals are evaluated over time and combined into higher-level **behavioral patterns**, which drive Argeia’s state-based interpretation of user engagement.

State transitions are intentionally slow-moving, pattern-driven, and designed to be fair to one-off mistakes.

---

## 🧱 Project Structure

```
argeia/
├── app/
│   ├── __init__.py                   # Flask app factory
│   ├── main.py                       # Application entry point
│   ├── routes.py                     # Web routes
│   ├── state_engine.py               # Behavioral state transition engine
│   ├── signals.py                    # Task domain & execution facts
│   └── tracker.py                    # Core task & procrastination logic
├── tests/
│   ├── test_task.py                  # Tests for Task behavior
│   ├── test_state_transitions.py     # Tests for behavioral state transitions
│   └── test_signals.py               # Tests for signal extraction (start delay) 
├── requirements.txt
├── .gitignore
├── DESIGN.md                         # High-level system design
├── docs/
│   └── behavior_model.md             # Procrastination behavior & state model
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
Currently in early development.  
Core task logic, procrastination signal detection, and a fully tested behavioral state engine have been implemented.

---

## 📝 License
This project is for educational purposes.

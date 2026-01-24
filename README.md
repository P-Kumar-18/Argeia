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

---

## 🧪 Procrastination Model

Argeia currently identifies procrastination through three independent signals:

- **Start Delay** — starting later than scheduled
- **Timeout** — never starting after the planned window ends
- **Underwork** — completing a task earlier than planned

Each signal is isolated, testable, and designed to be combined later into higher-level insights.

---

## 🧱 Project Structure

```
argeia/
├── app/
│   ├── __init__.py      # Flask app factory
│   ├── main.py          # Application entry point
│   ├── routes.py        # Web routes
│   └── tracker.py       # Core task & procrastination logic
├── tests/
│   └── test_task.py     # Tests for Task behavior
├── requirements.txt
├── .gitignore
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
Core task domain logic and procrastination detection implemented and fully tested.

---

## 📝 License
This project is for educational purposes.

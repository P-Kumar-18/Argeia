# Argeia

Argeia is a web-based schedule and procrastination tracker built with Flask.  
The goal of this project is not just to manage tasks, but to analyze *behavior* — identifying delays, missed schedules, and procrastination patterns over time.

This project is being developed as a learning-focused application with clean architecture, incremental development, and real-world design practices.

---

## 🚀 Features (Planned)
- Create and manage scheduled tasks
- Track when tasks are started and completed
- Detect delays and procrastination patterns
- Store data persistently using a database (SQLite)
- Simple web interface using Flask and templates
- Future insights and analytics

---

## 🧱 Project Structure

```
argeia/
├── app/
│   ├── __init__.py      # Flask app factory
│   ├── main.py          # Application entry point
│   └── routes.py        # Web routes
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

You should see a confirmation message indicating the app is running.

---

## 📚 Tech Stack
- Python
- Flask
- SQLite (planned)
- HTML / CSS (planned)

---

## 🎯 Project Status
Currently in early development.  
Core structure and routing are set up; task modeling and tracking logic are next.

---

## 📝 License
This project is for educational purposes.

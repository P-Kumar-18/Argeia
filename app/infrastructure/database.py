import sqlite3, os

os.makedirs("../data", exist_ok=True)

with sqlite3.connect("../data/argeia.db") as connection:
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS transitions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        previous_state TEXT NOT NULL,
        current_state TEXT NOT NULL,
        proposal_kind TEXT NOT NULL,
        proposal_severity TEXT NOT NULL,
        evidence_reason TEXT NOT NULL,
        timestamp TEXT NOT NULL
        )""")
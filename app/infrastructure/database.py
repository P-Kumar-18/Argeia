import sqlite3, os


class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.initialize_schema()
    

    def initialize_schema(self):
        self.create_directory()
        self.create_transition()
        self.connection.commit()


    def create_directory(self):
        if self.db_path != ":memory:":
            directory = os.path.dirname(self.db_path)
            if directory:
                os.makedirs(directory, exist_ok=True)


    def create_transition(self):
        cursor = self.connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS transitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            previous_state TEXT NOT NULL,
            current_state TEXT NOT NULL,
            proposal_kind TEXT NOT NULL,
            proposal_severity TEXT NOT NULL,
            evidence_reason TEXT NOT NULL,
            timestamp TEXT NOT NULL
            )""")
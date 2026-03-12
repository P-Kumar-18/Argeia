import sqlite3, os

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.initialize_schema()
    

    def initialize_schema(self):
        self.create_directory()
        self.create_transition()
        self.create_behavior_windows()
        self.create_window_signals()
        self.create_window_patterns()
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
    

    def create_behavior_windows(self):
        cursor = self.connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS behavior_windows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            window_start TEXT NOT NULL,
            window_end TEXT NOT NULL,
            status TEXT NOT NULL
            )""")


    def create_window_signals(self):
        cursor = self.connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS window_signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            window_id INTEGER NOT NULL,
            signal_type TEXT NOT NULL,
            signal_time INTEGER NOT NULL,
            planned_duration INTEGER NOT NULL,
            CONSTRAINT FK_WindowId FOREIGN KEY (window_id) REFERENCES behavior_windows(id)
            )""")
    

    def create_window_patterns(self):
        cursor = self.connection.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS window_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            window_id INTEGER NOT NULL,
            polarity TEXT NOT NULL,
            strength TEXT NOT NULL,
            confirmed TEXT NOT NULL,
            CONSTRAINT FK_WindowId FOREIGN KEY (window_id) REFERENCES behavior_windows(id)
            )""")        
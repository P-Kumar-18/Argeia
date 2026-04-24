import sqlite3
from .database import Database, get_default_path
from app.domain import Signal, Signal_type, Window
from app.core import Pattern_polarity_type, Pattern_strength_type


# --- Getting default database path ---
db_path = get_default_path()


def to_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "t", "yes", "y"}
    return bool(value)


# --- Converters ---
def convert_row_signal(row):
    return Signal(signal_type=Signal_type(row["signal_type"]), time=row["signal_time"], planned_duration=row["planned_duration"])


def convert_row_pattern(row):
    return {
        "polarity": Pattern_polarity_type(row["polarity"]),
        "strength": Pattern_strength_type(row["strength"]),
        "confirmed": to_bool(row["confirmed"])
    }


# --- Window Repository ---
class WindowRepository:
    def __init__(self, db_path=db_path):
        self.db_path = db_path
        self.database = Database(self.db_path)

    def window_creation(self, window: Window):
        cursor = self.database.connection.cursor()
        cursor.execute("""INSERT INTO behavior_windows(
                window_start,
                window_end,
                status
            ) VALUES (?, ?, ?)""", (
                window.window_start.isoformat(),
                window.window_end.isoformat(),
                window.window_status.value
        ))

        self.database.connection.commit()
        return cursor.lastrowid

    def close_window(self, window_id):
        cursor = self.database.connection.cursor()
        cursor.execute("""UPDATE behavior_windows SET status = 'close' WHERE id = ?""", (window_id,))
        self.database.connection.commit()
    
    def save_signals(self, window_id, signal: Signal):
        cursor = self.database.connection.cursor()
        cursor.execute("""INSERT INTO window_signals(
                window_id,
                signal_type,
                signal_time,
                planned_duration
            ) VALUES (?, ?, ?, ?)""",(
            window_id,
            signal.signal_type.value,
            signal.time,
            signal.planned_duration
        ))

        self.database.connection.commit()

    def save_patterns(self, window_id, pattern: dict):
        cursor = self.database.connection.cursor()
        cursor.execute("""INSERT INTO window_patterns(
                window_id,
                polarity,
                strength,
                confirmed
            ) VALUES (?, ?, ?, ?)""",(
            window_id,
            pattern["polarity"].value,
            pattern["strength"].value,
            int(bool(pattern["confirmed"]))
        ))

        self.database.connection.commit()

    def get_latest_open_window(self):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()
        cursor.execute("""SELECT * FROM behavior_windows WHERE status = 'open' ORDER BY id DESC LIMIT 1""")

        row = cursor.fetchone()

        if row == None:
            return None
        else:
            return row
        
    def get_signals(self, window):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()
        cursor.execute("""SELECT signal_type, signal_time, planned_duration FROM window_signals WHERE window_id = ?""", (window["id"],))

        rows = cursor.fetchall()
        if len(rows) == 0:
            return []
        else:
            signal_list = []
            for row in rows:
                signal_list.append(convert_row_signal(row))
            
            return signal_list

    def get_patterns(self, window):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()
        cursor.execute("""SELECT polarity, strength, confirmed FROM window_patterns WHERE window_id = ?""", (window["id"],))

        rows = cursor.fetchall()
        if len(rows) == 0:
            return []
        else:
            pattern_list = []
            for row in rows:
                pattern_list.append(convert_row_pattern(row))
            
            return pattern_list
    
    def get_previous_window(self, required_window = 3):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()
        cursor.execute("""SELECT * FROM behavior_windows WHERE status = 'close' ORDER BY id DESC LIMIT ?""", (required_window, ))

        rows = cursor.fetchall()
        
        return reversed(rows)
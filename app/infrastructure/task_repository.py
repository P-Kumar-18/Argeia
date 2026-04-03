from datetime import datetime
import sqlite3
from .database import Database, get_default_path


# --- Getting default database path ---
db_path = get_default_path()


# --- Converter ---
def convert_row(row):
    if len(row) == 4:
        return {
            "title": row["title"],
            "start_time": datetime.fromisoformat(row["schedule_for_start"]),
            "comment": row["comment"],
            "completed": True if row["completed"] == '1' else False
        }
    else:
        return {
            "title": row["title"],
            "start_time": datetime.fromisoformat(row["schedule_for_start"]),
            "comment": row["comment"]
        }


# --- Task Repository ---
class TaskRepository:
    def __init__(self, db_path=db_path):
        self.db_path = db_path
        self.database = Database(self.db_path)

    def create_task(self, title, start_time, end_time, completed=False, user_id=None, comment=None, started_at=None, completed_at=None):
        cursor = self.database.connection.cursor()

        cursor.execute("""INSERT INTO tasks(
            title,
            schedule_for_start,
            schedule_for_end,
            created_on,
            comment,
            user_id,
            started_at,
            completed_at,
            completed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                title,
                datetime.isoformat(start_time),
                datetime.isoformat(end_time),
                datetime.now().isoformat(),
                comment,
                user_id,
                datetime.isoformat(started_at) if started_at else None,
                datetime.isoformat(completed_at) if completed_at else None,
                completed
            ))
        
        self.database.connection.commit()
        return cursor.lastrowid
    
    def start_task(self, id, when):
        cursor = self.database.connection.cursor()

        cursor.execute("""UPDATE tasks SET started_at = ? WHERE id = ?""", (datetime.isoformat(when), id))

        self.database.connection.commit()
    
    def complete_task(self, id, when):
        cursor = self.database.connection.cursor()

        cursor.execute("""UPDATE tasks SET completed_at = ?, completed = 1 WHERE id = ?""", (datetime.isoformat(when), id))  

        self.database.connection.commit()  

    def get_n_latest_completed_tasks(self, n):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT title, schedule_for_start, comment FROM tasks WHERE completed = '1' ORDER BY id DESC LIMIT ?", (n,))

        rows = cursor.fetchall()

        if not len(rows) == 0:
            tasks_list = []
            for row in rows:
                tasks_list.append(convert_row(row))
            
            return tasks_list
    
    def get_n_latest_upcoming_tasks(self, n):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT title, schedule_for_start, comment FROM tasks WHERE completed = '0' ORDER BY schedule_for_start LIMIT ?", (n,))

        rows = cursor.fetchall()

        if not len(rows) == 0:
            tasks_list = []
            for row in rows:
                tasks_list.append(convert_row(row))
            
            return tasks_list
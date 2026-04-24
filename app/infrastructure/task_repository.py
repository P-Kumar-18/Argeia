from datetime import datetime
import sqlite3
from .database import Database, get_default_path
from app.domain import Task


# --- Getting default database path ---
db_path = get_default_path()


def to_iso(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


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


# --- Converter ---
def converter(task):
    if task:
        return Task(
            task_id=task["id"],
            title=task["title"],
            created_on=task["created_on"],
            start_time=task["scheduled_for_start"],
            end_time=task["scheduled_for_end"],
            user_id=task["user_id"],
            comment=task["comment"],
            completed=to_bool(task["completed"]),
            started_at=task["started_at"],
            completed_at=task["completed_at"]
        )


# --- Task Repository ---
class TaskRepository:
    def __init__(self, db_path=db_path):
        self.db_path = db_path
        self.database = Database(self.db_path)

    def create_task(self, title, start_time, end_time, completed=False, user_id=None, comment=None, started_at=None, completed_at=None):
        cursor = self.database.connection.cursor()

        cursor.execute("""INSERT INTO tasks(
            title,
            scheduled_for_start,
            scheduled_for_end,
            created_on,
            comment,
            user_id,
            started_at,
            completed_at,
            completed) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
                title,
                to_iso(start_time),
                to_iso(end_time),
                datetime.now().isoformat(),
                comment,
                user_id,
                to_iso(started_at),
                to_iso(completed_at),
                int(bool(completed))
            ))
        
        self.database.connection.commit()
        return cursor.lastrowid
    
    def start_task(self, id, when):
        cursor = self.database.connection.cursor()

        cursor.execute("""UPDATE tasks SET started_at = ? WHERE id = ?""", (to_iso(when), id))

        self.database.connection.commit()
    
    def complete_task(self, id, when):
        cursor = self.database.connection.cursor()

        cursor.execute("""UPDATE tasks SET completed_at = ?, completed = 1 WHERE id = ?""", (to_iso(when), id))  

        self.database.connection.commit()  

    def get_n_latest_completed_tasks(self, n):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM tasks WHERE CAST(completed AS INTEGER) = 1 ORDER BY id DESC LIMIT ?", (n,))

        tasks = cursor.fetchall()

        task_list = []

        for task in tasks:
            task_list.append(converter(task=task))
        
        return task_list
    
    def get_latest_upcoming_tasks(self):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM tasks WHERE CAST(completed AS INTEGER) = 0 ORDER BY scheduled_for_start")

        task = cursor.fetchone()

        return converter(task)
    
    def get_all_tasks(self):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM tasks")

        tasks = cursor.fetchall()

        task_list = []

        for task in tasks:
            task_list.append(converter(task=task))
        
        return task_list

    def get_task_by_id(self, id):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))

        task = cursor.fetchone()

        return converter(task=task)
    
    def update_task(self, id, title, comment, start_time, end_time):
        cursor = self.database.connection.cursor()

        cursor.execute("""UPDATE tasks SET 
            title=?,
            comment=?,
            scheduled_for_start=?,
            scheduled_for_end=?
            WHERE id=?""", (
                title,
                comment,
                to_iso(start_time),
                to_iso(end_time),
                id
            ))
        
        self.database.connection.commit()
    
    def delete_task(self, id):
        cursor = self.database.connection.cursor()

        cursor.execute("DELETE FROM tasks WHERE id=?", (id,))

        self.database.connection.commit()
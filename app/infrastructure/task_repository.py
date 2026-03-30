from datetime import datetime
from app.infrastructure import Database


# --- Task Repository ---
class TaskRepository:
    def __init__(self, db_path = "../data/argeia.db"):
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
    
    def complete_task(self, id, when):
        cursor = self.database.connection.cursor()

        cursor.execute("""UPDATE tasks SET completed_at = ?, completed = 1 WHERE id = ?""", (datetime.isoformat(when), id))
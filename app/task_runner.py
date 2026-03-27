from app.task import Task
from app.infrastructure.task_repository import TaskRepository
from app.behavior_runner import BehaviorRunner
from datetime import datetime


# --- Task Runner ---
class TaskRunner:
    def __init__(self, behavior_runner: BehaviorRunner, task_repo: TaskRepository=None):
        self.behavior_runner = behavior_runner
        self.task_repository = task_repo or TaskRepository()
    
    def create_task(self, title, start_time, end_time, comment, user_id=None):
        task_id = self.task_repository.create_task(title=title, start_time=start_time, end_time=end_time, user_id=user_id, comment=comment)
        return Task(task_id=task_id, title=title, start_time=start_time, end_time=end_time, user_id=user_id, comment=comment)
    
    def start_task(self, task: Task, when=None):
        task.start(when)
        self.task_repository.start_task(task.id, when)
    
    def complete_task(self, task: Task, when=None):
        task.complete(when)
        self.task_repository.complete_task(task.id, task.completed_at)

        self.behavior_runner.add_task(task)
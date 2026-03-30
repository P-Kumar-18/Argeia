from datetime import datetime, timedelta
from app.infrastructure import TaskRepository, WindowRepository
from app.runner import TaskRunner, BehaviorRunner


class FakeRepository:
    def __init__(self):
        self.saved = []
        self.latest = None


    def save(self, transition):
        self.saved.append(transition)
    

    def get_latest(self):
        return self.latest


def test_new_task_have_id():
    repo = FakeRepository()
    window_repo = WindowRepository(db_path=":memory:")
    task_repo = TaskRepository(db_path=":memory:")
    behavior_runner = BehaviorRunner(transition_repository=repo, window_repository=window_repo)

    runner = TaskRunner(behavior_runner=behavior_runner, task_repo=task_repo)
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    task = runner.create_task(title="Test", start_time=start_time, end_time=end_time, comment="For test")

    assert task.id is not None


def test_new_task_have_none_started_at_and_completed_at():
    repo = FakeRepository()
    window_repo = WindowRepository(db_path=":memory:")
    task_repo = TaskRepository(db_path=":memory:")
    behavior_runner = BehaviorRunner(transition_repository=repo, window_repository=window_repo)

    runner = TaskRunner(behavior_runner=behavior_runner, task_repo=task_repo)
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    task = runner.create_task(title="Test", start_time=start_time, end_time=end_time, comment="For test")

    assert task.started_at is None
    assert task.completed_at is None
    assert task.completed is False


def test_start_task_updates_started_at():
    repo = FakeRepository()
    window_repo = WindowRepository(db_path=":memory:")
    task_repo = TaskRepository(db_path=":memory:")
    behavior_runner = BehaviorRunner(transition_repository=repo, window_repository=window_repo)

    runner = TaskRunner(behavior_runner=behavior_runner, task_repo=task_repo)
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    task = runner.create_task(title="Test", start_time=start_time, end_time=end_time, comment="For test")

    started_at = start_time + timedelta(minutes=15)
    runner.start_task(task, started_at)

    assert task.started_at == started_at


def test_complete_task():
    repo = FakeRepository()
    window_repo = WindowRepository(db_path=":memory:")
    task_repo = TaskRepository(db_path=":memory:")
    behavior_runner = BehaviorRunner(transition_repository=repo, window_repository=window_repo)

    runner = TaskRunner(behavior_runner=behavior_runner, task_repo=task_repo)
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    task = runner.create_task(title="Test", start_time=start_time, end_time=end_time, comment="For test")

    runner.complete_task(task=task)

    assert task.completed_at != None
    assert task.completed is True


def test_multiple_tasks_different_id():
    repo = FakeRepository()
    window_repo = WindowRepository(db_path=":memory:")
    task_repo = TaskRepository(db_path=":memory:")
    behavior_runner = BehaviorRunner(transition_repository=repo, window_repository=window_repo)

    runner = TaskRunner(behavior_runner=behavior_runner, task_repo=task_repo)
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=1)

    task_1 = runner.create_task(title="Test-1", start_time=start_time, end_time=end_time, comment="For test")
    task_2= runner.create_task(title="Test-2", start_time=start_time, end_time=end_time, comment="For test")

    assert task_1.id != task_2.id
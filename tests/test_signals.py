from app.signals import compute_start_delay_signal, compute_timeout_time, compute_underwork_signal
from app.tracker import Task
from datetime import datetime, timedelta

def test_start_on_time():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time)

    expected_dict = {
        "delay_time": 0,
        "planned_duration": 120
    }

    assert compute_start_delay_signal(task) == expected_dict


def test_start_late():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time + timedelta(hours=1))
    
    expected_dict = {
        "delay_time": 60,
        "planned_duration": 120
    }

    assert compute_start_delay_signal(task) == expected_dict


def test_task_started_early():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time - timedelta(minutes=5))
    
    expected_dict = {
        "delay_time": 0,
        "planned_duration": 120
    }

    assert compute_start_delay_signal(task) == expected_dict


def test_task_stoped_early():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    complete_time = start_time + timedelta(hours=1)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time)
    task.complete(when=complete_time)

    expected_dict = {
        "underwork_time": 60,
        "planned_duration": 120
    }

    assert compute_underwork_signal(task) == expected_dict


def test_task_stopped_at_time():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    complete_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time)
    task.complete(when=complete_time)

    expected_dict = {
        "underwork_time": 0,
        "planned_duration": 120
    }

    assert compute_underwork_signal(task) == expected_dict


def test_task_never_started():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    
    expected_dict = {
        "timeout_time": 120,
        "planned_duration": 120
    }

    assert compute_timeout_time(task) == expected_dict
from datetime import datetime, timedelta
from app.domain import Signal, Signal_type, Task


def test_start_on_time():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time)

    signal = Signal(task)

    assert signal.signal_type == Signal_type.NONE


def test_start_late():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time + timedelta(hours=1))

    signal = Signal(task)

    assert signal.signal_type == Signal_type.DELAY
    assert signal.time == 60
    assert signal.planned_duration == 120


def test_start_early():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time - timedelta(minutes=5))

    signal = Signal(task)

    assert signal.signal_type == Signal_type.NONE


def test_stopped_early():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time)
    task.complete(when=start_time + timedelta(hours=1))

    signal = Signal(task)

    assert signal.signal_type == Signal_type.UNDERWORK
    assert signal.time == 60
    assert signal.planned_duration == 120


def test_stopped_on_time():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")
    task.start(when=start_time)
    task.complete(when=start_time + timedelta(hours=2))

    signal = Signal(task)

    assert signal.signal_type == Signal_type.NONE


def test_never_started():
    start_time = datetime.now() - timedelta(hours=3)
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")

    signal = Signal(task)

    assert signal.signal_type == Signal_type.TIMEOUT
    assert signal.time == 120
    assert signal.planned_duration == 120


def test_never_started_before_end_is_not_timeout():
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)

    task = Task(start_time=start_time, end_time=end_time, task_id=1, title="Test")

    signal = Signal(task)

    assert signal.signal_type == Signal_type.NONE
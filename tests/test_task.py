from app.tracker import Task
from datetime import datetime, timedelta

def test_task_creation():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(
        task_id = 1,
        title = "Study",
        start_time = start,
        end_time = end
    )

    assert task.title == "Study"
    assert task.started_at is None
    assert task.completed is False

def test_delay_when_started_late():
    scheduled_start = datetime.now()
    scheduled_end = scheduled_start + timedelta(hours=1)

    task = Task(1, "Math", scheduled_start, scheduled_end)

    late_start = scheduled_start + timedelta(minutes=15)
    task.start(when=late_start)

    assert task.delay_time() == 15


def test_timeout_when_never_started():
    scheduled_start = datetime.now() - timedelta(hours=2)
    scheduled_end = scheduled_start + timedelta(hours=1)

    task = Task(1, "Missed Task", scheduled_start, scheduled_end)

    current_time = scheduled_end + timedelta(minutes=10)

    assert task.timeout_time(current_time) == 60


def test_no_timeout_before_end():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Future Task", start, end)

    assert task.timeout_time() is None


def test_start_exactly_on_time():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Exact Start", start, end)
    task.start(when=start)

    assert task.delay_time() == 0


def test_start_early():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Early Start", start, end)
    task.start(when=start - timedelta(minutes=10))

    assert task.delay_time() == 0


def test_never_started_not_expired():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Future Task", start, end)

    assert task.timeout_time() is None


def test_never_started_exact_end():
    start = datetime.now() - timedelta(hours=1)
    end = start + timedelta(hours=1)

    task = Task(1, "Exact End", start, end)

    assert task.timeout_time(current_time=end) is None


def test_never_started_just_expired():
    start = datetime.now() - timedelta(hours=1)
    end = start + timedelta(hours=1)

    task = Task(1, "Expired Task", start, end)

    assert task.timeout_time(end + timedelta(minutes=1)) == 60


def test_complete_without_start():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Instant Complete", start, end)
    task.complete()

    assert task.completed is True
    assert task.started_at is None


def test_start_after_end():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Late Start", start, end)
    task.start(when=end + timedelta(minutes=10))

    assert task.delay_time() == 70


def test_no_underwork_when_full_duration():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Full Work", start, end)

    task.start(when=start)
    task.complete(when=end)

    assert task.underwork_time() == 0


def test_underwork_when_stopped_early():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Early Stop", start, end)

    task.start(when=start)
    task.complete(when=start + timedelta(minutes=30))

    assert task.underwork_time() == 30


def test_underwork_when_instant_quit():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Instant Quit", start, end)

    task.start(when=start)
    task.complete(when=start)

    assert task.underwork_time() == 60


def test_no_underwork_when_overworked():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Overwork", start, end)

    task.start(when=start)
    task.complete(when=start + timedelta(minutes=90))

    assert task.underwork_time() == 0


def test_underwork_not_completed():
    start = datetime.now()
    end = start + timedelta(hours=1)

    task = Task(1, "Not Finished", start, end)

    task.start(when=start)

    assert task.underwork_time() is None


def test_underwork_zero_length_task():
    time = datetime.now()

    task = Task(1, "Zero Length", time, time)

    task.start(when=time)
    task.complete(when=time)

    assert task.underwork_time() == 0
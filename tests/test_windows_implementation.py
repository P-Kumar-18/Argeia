from app.window import Window, Window_status
from app.window_manager import WindowManager
from app.infrastructure.window_repository import WindowRepository
from app.signals import Signal, Signal_type
from app.pattern_detection import Pattern_polarity_type, Pattern_strength_type
from datetime import datetime, timedelta


"""
    Window
"""
def test_window_end_is_one_week_after_start():
    start = datetime(2024, 1, 1)
    window = Window(start)
    assert window.window_end == start + timedelta(weeks=1)


def test_window_defaults_to_open():
    window = Window(datetime(2024, 1, 1))
    assert window.window_status == Window_status.OPEN


def test_add_signals_appends_valid_signals():
    window = Window(datetime(2024, 1, 1))
    s1 = Signal(signal_type=Signal_type.DELAY, time=30, planned_duration=60)
    s2 = Signal(signal_type=Signal_type.TIMEOUT, time=15, planned_duration=60)
    window.add_signals([s1, s2])
    assert len(window.signals) == 2


def test_add_signals_skips_none_signal_type():
    window = Window(datetime(2024, 1, 1))
    s_valid = Signal(signal_type=Signal_type.DELAY, time=30, planned_duration=60)
    s_none = Signal(signal_type=Signal_type.DELAY, time=30, planned_duration=60)
    s_none.signal_type = Signal_type.NONE
    window.add_signals([s_valid, s_none])
    assert len(window.signals) == 1


def test_add_patterns_appends_all():
    window = Window(datetime(2024, 1, 1))
    p1 = {"polarity": Pattern_polarity_type.NEGATIVE, "strength": Pattern_strength_type.HIGH, "confirmed": True}
    p2 = {"polarity": Pattern_polarity_type.POSITIVE, "strength": Pattern_strength_type.NONE, "confirmed": True}
    window.add_patterns([p1, p2])
    assert len(window.patterns) == 2


"""
    WindowManager Init
"""
def test_new_window_created_when_none_exists():
    repo = WindowRepository(db_path=":memory:")
    wm = WindowManager(repository=repo)
    assert wm.current_window is not None
    assert wm.current_window_id is not None


def test_no_previous_windows_on_first_run():
    repo = WindowRepository(db_path=":memory:")
    wm = WindowManager(repository=repo)
    assert list(wm.previous_windows) == []


def test_existing_window_is_loaded_on_restart():
    repo = WindowRepository(db_path=":memory:")
    wm1 = WindowManager(repository=repo)
    first_id = wm1.current_window_id

    wm2 = WindowManager(repository=repo)
    assert wm2.current_window_id == first_id


"""
    pattern_batching
"""
def test_task_number_increments_on_each_task():
    repo = WindowRepository(db_path=":memory:")
    wm = WindowManager(repository=repo)
    wm.current_window.signals.append(Signal(signal_type=Signal_type.DELAY, time=30, planned_duration=60))
    wm.pattern_batching()
    assert wm.current_window.task_number == 1


def test_unconfirmed_pattern_resets_task_number():
    repo = WindowRepository(db_path=":memory:")
    wm = WindowManager(repository=repo)
    wm.current_window.task_number = 4
    wm.current_window.signals = []
    wm.pattern_batching()
    assert wm.current_window.task_number == 0


def test_confirmed_pattern_clears_signals_and_saves():
    repo = WindowRepository(db_path=":memory:")
    wm = WindowManager(repository=repo)
    wm.current_window.task_number = 4
    for _ in range(5):
        wm.current_window.signals.append(Signal(signal_type=Signal_type.TIMEOUT, time=60, planned_duration=60))

    wm.pattern_batching()

    assert wm.current_window.task_number == 0
    assert wm.current_window.signals == []
    assert len(wm.current_window.patterns) > 0
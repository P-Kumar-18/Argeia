from enum import Enum
from datetime import datetime, timedelta


# --- Window  Status ---
class Window_status(Enum):
    OPEN = "open"
    CLOSE = "close"


# --- Utils ---
def compute_week_start():
    now = datetime.now()
    monday = now - timedelta(days=now.weekday())
    return monday.replace(hour=0, minute=0, second=0, microsecond=0)


# --- Window ---
class Window:
    def __init__(self, window_start):
        self.window_status = Window_status.OPEN
        self.window_start = window_start
        self.task_number = 0
        self.window_end = self.window_start + timedelta(weeks=1)
        self.signals = []
        self.patterns = []

    def add_signals(self, signals):
        for signal in signals:
            if signal.signal_type == None:
                continue
            else:
                self.signals.append(signal)

    def add_patterns(self, patterns):
        for pattern in patterns:
            self.patterns.append(pattern)
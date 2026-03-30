from collections import deque
from datetime import datetime
from app.core import detect_pattern, evaluate_behavior
from app.domain import Task, Signal, Signal_type, Window, compute_week_start
from app.infrastructure import WindowRepository


# --- Window Manger ---
class WindowManager:
    def __init__(self, repository = None, required_window = 3):
        self.repository = repository if repository is not None else WindowRepository()
        # Making new window
        row = self.repository.get_latest_open_window()
        if row is None:
            week_start = compute_week_start()
            self.current_window = Window(week_start)
            self.current_window_id = self.repository.window_creation(self.current_window)
        # Getting previous open window
        else: 
            self.current_window = Window(datetime.fromisoformat(row["window_start"]))
            self.current_window.add_signals(self.repository.get_signals(row))
            self.current_window_id = row["id"]
        
        # Previous Window for sustainment and adjacency check
        self.previous_windows = deque(maxlen=required_window)
        previous_windows = self.repository.get_previous_window(required_window)
        for window in previous_windows:
            window_n = Window(datetime.fromisoformat(window["window_start"]))
            window_n.add_patterns(self.repository.get_patterns(window))
            self.previous_windows.append(window_n)

    def add_task(self, task: Task):
        if not task.completed:
            return None
        if not datetime.now() >= self.current_window.window_end:
            self.save_signal(task)
            return None
        # Detect pattern at the end of the current window
        else:
            self.repository.close_window(self.current_window_id)
            if self.current_window.signals:
                pattern = detect_pattern(self.current_window.signals)
                self.current_window.patterns.append(pattern)
                self.repository.save_patterns(self.current_window_id, pattern)

            proposal = self.proposal_generation()

            # Creating a new window and saving the current task
            self.previous_windows.append(self.current_window)
            week_start = compute_week_start()
            self.current_window = Window(week_start)
            self.current_window_id = self.repository.window_creation(self.current_window)

            self.save_signal(task)
            return proposal
    
    def save_signal(self, task):
        signal = Signal(task)

        if signal.signal_type == Signal_type.NONE:
            return
        else:
            self.current_window.signals.append(signal)
            self.repository.save_signals(self.current_window_id, signal)
            self.pattern_batching()

    def pattern_batching(self):
        self.current_window.task_number += 1
        if self.current_window.task_number == 5:
            pattern = detect_pattern(self.current_window.signals)

            if not pattern["confirmed"]:
                self.current_window.task_number = 0
            
            else:
                self.current_window.task_number = 0
                self.current_window.signals.clear()
                self.current_window.patterns.append(pattern)
                self.repository.save_patterns(self.current_window_id, pattern)

    def proposal_generation(self):
        previous_windows = []
        for previous_window in self.previous_windows:
            previous_windows.append(previous_window.patterns)
        
        return evaluate_behavior(self.current_window.patterns, previous_windows)
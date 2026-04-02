from enum import Enum
from .task import Task


# --- Signal Types ---
class Signal_type(Enum):
    DELAY = "delay"
    UNDERWORK = "underwork"
    TIMEOUT = "timeout"
    NONE = "none"


# --- Signal ---
class Signal:
    def __init__(self, task = None, signal_type = None, time = None, planned_duration = None):
        if task is None and not (signal_type is not None and time is not None and planned_duration is not None):
            raise ValueError("Invalid Arguments!")
        
        if task:
            start_delay = self.compute_start_delay(task)
            underwork = self.compute_underwork(task)
            timeout = self.compute_timeout(task)

            if timeout["timeout_time"] and timeout["timeout_time"] > 0:
                self.signal_type = Signal_type.TIMEOUT
                self.time = timeout["timeout_time"]
                self.planned_duration = timeout["planned_duration"]
            
            elif underwork["underwork_time"] and underwork["underwork_time"] > 0:
                self.signal_type = Signal_type.UNDERWORK
                self.time = underwork["underwork_time"]
                self.planned_duration = underwork["planned_duration"]

            elif start_delay["delay_time"] and start_delay["delay_time"] > 0:
                self.signal_type = Signal_type.DELAY
                self.time = start_delay["delay_time"]
                self.planned_duration = start_delay["planned_duration"]

            else:
                self.signal_type = Signal_type.NONE
        
        else:
            self.signal_type = signal_type
            self.time = time
            self.planned_duration = planned_duration

    def compute_timeout(
            self,
            task: Task
    )-> dict:
        timeout_time = task.timeout_time()
        total_time = int(
            (task.scheduled_for_end - task.scheduled_for_start).total_seconds() / 60
        )

        return {
            "timeout_time": timeout_time,
            "planned_duration": total_time
        }
    
    def compute_underwork(
            self,
            task: Task
    )-> dict:
        underwork_time = task.underwork_time()
        total_time = int(
            (task.scheduled_for_end - task.scheduled_for_start).total_seconds() / 60
        )

        return {
            "underwork_time": underwork_time,
            "planned_duration": total_time
        }
    
    def compute_start_delay(
            self,
            task: Task
    )-> dict:
        delay_time = task.delay_time()
        total_time = int(
            (task.scheduled_for_end - task.scheduled_for_start).total_seconds() / 60
        )

        return {
            "delay_time": delay_time, 
            "planned_duration": total_time
        }
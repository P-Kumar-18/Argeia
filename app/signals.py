from app.tracker import Task

def compute_start_delay_signal(
        task: Task
)-> dict:
    delay_time = task.delay_time()
    total_time = int(
        (task.scheduled_for_end - task.scheduled_for_start).total_seconds() / 60
    )

    if delay_time is None:
        timeout_time = task.timeout_time()
        return {
            "timeout_time": timeout_time, 
            "planned_duration": total_time
        }
    
    return {
        "delay_time": delay_time, 
        "planned_duration": total_time
    }
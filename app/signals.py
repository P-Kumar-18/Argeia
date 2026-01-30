from app.tracker import Task

def compute_start_delay_signal(
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


def compute_underwork_signal(
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


def compute_timeout_time(
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
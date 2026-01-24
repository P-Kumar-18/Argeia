from datetime import datetime

class Task:
    '''
        Task and Tracing field
        may be seperated in the future.
    '''

    # Planning/Behavior
    def __init__(self, task_id, title, start_time, end_time,  user_id=None, comment=None):
        self.id = task_id
        self.title = title
        self.scheduled_for_start = start_time
        self.scheduled_for_end = end_time
        self.created_on = datetime.now()
        self.comment = comment
        self.user_id = user_id

        # Tracking
        self.started_at = None
        self.completed_at = None
        self.completed = False
    

    # Behavior Tracking
    def start(self, when=None):
        self.started_at = when or datetime.now()
    
    def complete(self, when=None):
        self.completed_at = when or datetime.now()
        self.completed = True
    
    def delay_time(self):
        if not self.started_at:
            return None
        
        delta = self.started_at - self.scheduled_for_start
        return max(int(delta.total_seconds() // 60), 0)
    
    # Task never started
    def timeout_time(self, current_time=None):
        if self.started_at is not None:
            return None

        current_time = current_time or datetime.now()

        if current_time <= self.scheduled_for_end:
            return None

        delta = self.scheduled_for_end - self.scheduled_for_start
        return int(delta.total_seconds() // 60)
    
    # For not working the planed time
    def underwork_time(self):
        if not self.started_at or not self.completed_at:
            return None
        
        planned = self.scheduled_for_end - self.scheduled_for_start
        actual = self.completed_at - self.started_at

        delta = planned - actual
        return max(int(delta.total_seconds() // 60), 0)
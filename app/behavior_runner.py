from app.state_engine import apply_proposal, State
from app.infrastructure.transition_repository import TransitionRepository
from app.window_manager import WindowManager


# --- BehaviorRunner ---
class BehaviorRunner:
    def __init__(self, initial_state: State = None, transition_repository = None, window_repository = None):
        self.repository = transition_repository or TransitionRepository()
        self.current_state = initial_state or self.get_current_state()
        self.window_manager = WindowManager(repository=window_repository)

    def get_current_state(self):
        latest = self.repository.get_latest()

        if latest is None:
            return State.STABLE
        return latest.current_state
    
    def add_task(self, task):
        proposal = self.window_manager.add_task(task)

        if proposal:
            self.process_proposal(proposal)
    
    def process_proposal(self, proposal):
        new_state, transition = apply_proposal(self.current_state, proposal)

        if transition:
            self.repository.save(transition)
        
        self.current_state = new_state
        return self.current_state
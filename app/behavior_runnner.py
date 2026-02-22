from app.state_engine import apply_proposal, State
from app.infrastructure.transition_repository import TransitionRepository

class BehaviorRunner:
    def __init__(self, initial_state: State = State.STABLE, repository = TransitionRepository):
        self.current_state = initial_state
        self.repository = repository
    
    def process(self, proposal):
        new_state, transition = apply_proposal(self.current_state, proposal)

        if transition:
            self.repository.save(transition)
        
        self.current_state = new_state

        return self.current_state
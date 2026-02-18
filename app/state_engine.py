from app.behavior_evaluator import Proposal_kind, Proposal_severity, Proposal
from enum import Enum
from datetime import datetime

# Classifying states
class State(Enum):
    STABLE = "stable"
    DRIFTING = "drifting"
    STRAINED = "strained"
    DISENGAGED = "disengaged"


class Transition:
    def __init__(self, previous_state: State, current_state: State, proposal: Proposal):
        self.previous_state = previous_state
        self.current_state = current_state
        self.proposal_kind = proposal.kind
        self.proposal_severity = proposal.severity
        self.evidence_reason = proposal.evidence_reason
        self.timestamp = datetime.now()


# State Engine
def apply_proposal(
        current_state: State, 
        proposal: Proposal = None
)-> State:
    if proposal is None:
        return current_state, None
    
    if proposal.kind == Proposal_kind.DEGRADATION:
        new_state = degrade(current_state, proposal)
    
    else:
        new_state = recovery(current_state, proposal)
    
    if current_state != new_state:
        transition = Transition(current_state, new_state, proposal)
    else:
        transition = None
    return new_state, transition
    

def degrade(
        current_state: State,
        proposal: Proposal
)-> State:
    if proposal.severity == Proposal_severity.SEVERE:
        if current_state == State.STABLE:
            current_state = State.STRAINED
        
        else:
            current_state = State.DISENGAGED
        
        return current_state
    
    if current_state == State.STABLE:
        current_state = State.DRIFTING
    elif current_state == State.DRIFTING:
        current_state = State.STRAINED
    else:
        current_state = State.DISENGAGED
    
    return current_state

    
def recovery(
        current_state: State,
        proposal: Proposal
)-> State:
    if not proposal.kind == Proposal_kind.RECOVERY:
        raise AssertionError
    
    if current_state == State.DISENGAGED:
        current_state = State.STRAINED
    elif current_state == State.STRAINED:
        current_state = State.DRIFTING
    else:
        current_state = State.STABLE
    
    return current_state
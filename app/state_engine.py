from app.behavior_evaluator import Proposal_kind, Proposal_severity
from enum import Enum

# Classifying states
class State(Enum):
    STABLE = "stable"
    DRIFTING = "drifting"
    STRAINED = "strained"
    DISENGAGED = "disengaged"


# State Engine
def apply_proposal(
        current_state: State, 
        proposal: dict
)-> State:
    if proposal["kind"] == None or proposal["severity"] == None or not proposal:
        return current_state
    
    if proposal["kind"] == Proposal_kind.DEGRADATION:
        return degrade(current_state, proposal)
    
    if proposal["kind"] == Proposal_kind.RECOVERY:
        return recovery(current_state, proposal)

    return current_state
    

def degrade(
        current_state: State,
        proposal: dict
)-> State:
    if not proposal["kind"] == Proposal_kind.DEGRADATION:
        raise AssertionError
    

    if proposal["severity"] == Proposal_severity.SEVERE:
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
        proposal: dict
)-> State:
    if not proposal["kind"] == Proposal_kind.RECOVERY:
        raise AssertionError
    
    if current_state == State.DISENGAGED:
        current_state = State.STRAINED
    elif current_state == State.STRAINED:
        current_state = State.DRIFTING
    else:
        current_state = State.STABLE
    
    return current_state
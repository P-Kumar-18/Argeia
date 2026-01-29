from enum import Enum

# Classifying states
class State(Enum):
    STABLE = "stable"
    DRIFTING = "drifting"
    STRAINED = "strained"
    DISENGAGED = "disengaged"


# Patterns
class Pattern():
    def __init__(
            self,
            exists: bool = False,
            negative_confirmed: bool = False,
            positive_confirmed: bool = False,
            weak: bool = False,
            severe: bool = False,
            sustained: bool = False 
    ):
        self.exists = exists
        self.negative_confirmed = negative_confirmed
        self.positive_confirmed = positive_confirmed
        self.weak = weak
        self.severe = severe
        self.sustained = sustained      # Will be used in the future for recovery gating


# State Engine
class State_Engine:
    def transition(
            self, 
            current_state: State, 
            pattern: Pattern
    )-> State:
        if not pattern.exists or pattern.weak:
            return current_state
        
        if pattern.positive_confirmed and pattern.negative_confirmed:
            return current_state

        if pattern.negative_confirmed:
            return self.degrade(current_state, pattern)
        
        if pattern.positive_confirmed:
            return self.recovery(current_state, pattern)

        return current_state
    

    def degrade(
            self,
            current_state: State,
            pattern: Pattern
    )-> State:
        if not pattern.negative_confirmed:
            raise AssertionError
        

        if pattern.severe:
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
            self,
            current_state: State,
            pattern: Pattern
    )-> State:
        if not pattern.positive_confirmed:
            raise AssertionError
        
        if current_state == State.DISENGAGED:
            current_state = State.STRAINED
        elif current_state == State.STRAINED:
            current_state = State.DRIFTING
        else:
            current_state = State.STABLE
        
        return current_state
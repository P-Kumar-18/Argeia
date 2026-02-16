from app.pattern_detection import Pattern_polarity_type, Pattern_strength_type
from enum import Enum

class Proposal_severity(Enum):
    NORMAL = "normal"
    SEVERE = "severe"


class Proposal_kind(Enum):
    DEGRADATION = "degradation"
    RECOVERY = "recovery"


def detect_sustained_pattern(windows: list, required_windows: int = 3):
    if len(windows) < required_windows - 1:
        return False

    relevant_windows = windows[-(required_windows - 1):]

    for window in relevant_windows:
        positive_flag = False
        for pattern in window:       
            if (
            pattern["polarity"] == Pattern_polarity_type.POSITIVE
            and pattern["confirmed"] is True
        ):
                positive_flag = True
                break
        
        if not positive_flag:
            return False
        
    return True


def evaluate_behavior(
        current_window:list,
        previous_windows: list = None
)-> dict:
    possible_severe_flag = False
    possible_degradation_flag = False
    possible_recovery_flag = False

    for pattern in current_window:
        if pattern["confirmed"] == False:
            continue

        if pattern["polarity"] == Pattern_polarity_type.NEGATIVE:
            if pattern["strength"] == Pattern_strength_type.HIGH:
                # Multiple high strength pattern
                if possible_severe_flag:
                    return {
                        "kind": Proposal_kind.DEGRADATION,
                        "severity": Proposal_severity.SEVERE
                    }
                possible_severe_flag = True
                continue
        
            if pattern["strength"] == Pattern_strength_type.LOW:
                if possible_degradation_flag:
                    possible_severe_flag = True
                possible_degradation_flag = True
                continue
        else:
            possible_recovery_flag = True

    # Single high strength pattern
    if possible_severe_flag:
        return {
            "kind": Proposal_kind.DEGRADATION,
            "severity": Proposal_severity.NORMAL
        }
    
    # Low strenth pattern in adjacent windows
    if possible_degradation_flag:
        if previous_windows != None:
            previous_window = previous_windows[-1]

            for pattern in previous_window:
                if (
                    pattern["polarity"] == Pattern_polarity_type.NEGATIVE
                    and pattern["strength"] == Pattern_strength_type.LOW
                    and pattern["confirmed"] is True
                ):
                    return {
                        "kind": Proposal_kind.DEGRADATION,
                        "severity": Proposal_severity.NORMAL
                    }
    
    if possible_severe_flag or possible_degradation_flag:
        possible_recovery_flag = False

    # Recovery
    if possible_recovery_flag:

        if previous_windows and detect_sustained_pattern(previous_windows):
            return {
                "kind": Proposal_kind.RECOVERY,
                "severity": Proposal_severity.NORMAL
            }
    
    return {
        "kind": None,
        "severity": None
    }
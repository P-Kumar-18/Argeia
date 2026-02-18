from app.pattern_detection import Pattern_polarity_type, Pattern_strength_type
from enum import Enum

class Proposal_severity(Enum):
    NORMAL = "normal"
    SEVERE = "severe"


class Proposal_kind(Enum):
    DEGRADATION = "degradation"
    RECOVERY = "recovery"


class Proposal_windows_scope(Enum):
    SINGLE_WINDOW = "single_window"
    MULTI_WINDOW = "multi_window"


class Proposal:
    def __init__(self, kind = None, severity = None, evidence_reason = None):
        self.kind = kind
        self.severity = severity
        self.evidence_reason = evidence_reason


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
    high = 0
    low = 0

    for pattern in current_window:
        if pattern["confirmed"] == False:
            continue

        if pattern["polarity"] == Pattern_polarity_type.NEGATIVE:
            if pattern["strength"] == Pattern_strength_type.HIGH:
                # Multiple high strength pattern
                if possible_severe_flag:
                    propsoal = Proposal(
                        Proposal_kind.DEGRADATION,
                        Proposal_severity.SEVERE,
                        {
                            "high_count": high,
                            "low_count": low,
                            "windows_scope": Proposal_windows_scope.SINGLE_WINDOW,
                            "sustained_trigger": False
                        }
                    )
                    return propsoal
                high += 1
                possible_severe_flag = True
                continue
        
            if pattern["strength"] == Pattern_strength_type.LOW:
                low += 1
                if possible_degradation_flag:
                    possible_severe_flag = True
                possible_degradation_flag = True
                continue
        else:
            possible_recovery_flag = True

    # Single high strength pattern
    if possible_severe_flag:
        propsoal = Proposal(
            Proposal_kind.DEGRADATION,
            Proposal_severity.NORMAL,
            {
                "high_count": high,
                "low_count": low,
                "windows_scope": Proposal_windows_scope.SINGLE_WINDOW,
                "sustained_trigger": False
            }
        )
        return propsoal
    
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
                    propsoal = Proposal(
                        Proposal_kind.DEGRADATION,
                        Proposal_severity.NORMAL,
                        {
                            "high_count": high,
                            "low_count": low,
                            "windows_scope": Proposal_windows_scope.MULTI_WINDOW,
                            "sustained_trigger": False
                        }
                    )
                    return propsoal
    
    if possible_severe_flag or possible_degradation_flag:
        possible_recovery_flag = False

    # Recovery
    if possible_recovery_flag:

        if previous_windows and detect_sustained_pattern(previous_windows):
            propsoal = Proposal(
                Proposal_kind.RECOVERY,
                Proposal_severity.NORMAL,
                {
                    "high_count": high,
                    "low_count": low,
                    "windows_scope": Proposal_windows_scope.MULTI_WINDOW,
                    "sustained_trigger": True
                }
            )
            return propsoal
    
    return None
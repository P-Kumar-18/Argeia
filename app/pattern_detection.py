from enum import Enum

# NOTE: strength thresholds are provisional and subject to tuning

class pattern_polarity_type(Enum):
    NEGATIVE = "negative"
    POSITIVE = "positive" 

class pattern_strength_type(Enum):
    LOW = "low"
    HIGH = "high"


def compute_signals(signals: list)-> list:
    normalized_time = []
    for signal in signals:
        if "delay_time" in signal:
            normalized_time.append(int((signal["delay_time"] / signal["planned_duration"]) * 100))
        elif "timeout_time" in signal:
            normalized_time.append(int((signal["timeout_time"] / signal["planned_duration"]) * 100))
        elif "underwork_time" in signal:
            normalized_time.append(int((signal["underwork_time"] / signal["planned_duration"]) * 100))
        else:
            raise ValueError("Unknown signal type")
    
    return normalized_time


def signals_polarity(normalized_time: list):
    negative_signals = []
    positive_signals = []
    for signal in normalized_time:
        if (signal > 0):
            negative_signals.append(signal)
        else:
            positive_signals.append(signal)
    
    return (negative_signals, positive_signals)


def signals_strength(negative_signals: list):
    weak_signals = []
    moderate_signals = []
    strong_signals = []
    for signal in negative_signals:
        if signal > 0 and signal <= 10:
            weak_signals.append(signal)
        elif signal > 10 and signal <= 30:
            moderate_signals.append(signal)
        else:
            strong_signals.append(signal)
    
    return (weak_signals, moderate_signals, strong_signals)


def pattern_confirmation(count: dict):
    if (count["strong"] > 1) or (count["moderate"] > 2) or (count["weak"] > 5):
        return True
    
    return False


# NOTE: strength thresholds are intentionally stricter than confirmation thresholds
def pattern_strength(count: dict):
    if (count["strong"] >= 2) or (count["moderate"] >= 3) or (count["weak"] >= 12):
        return pattern_strength_type.HIGH
    
    else:
        return pattern_strength_type.LOW



def detect_pattern(signals: list):
    normalized_time = compute_signals(signals)
    negative_signals, positive_signals = signals_polarity(normalized_time)

    # Negative Pattern Detection
    if len(negative_signals) > 0:
        
        weak_signals, moderate_signals, strong_signals = signals_strength(negative_signals)

        count = {
            "weak": len(weak_signals),
            "moderate": len(moderate_signals),
            "strong": len(strong_signals)
        } 
        confirmed_pattern = pattern_confirmation(count)

        if confirmed_pattern:
            strength = pattern_strength(count)
        else:
            strength = None
        
        return {
            "confirmed": confirmed_pattern,
            "polarity": pattern_polarity_type.NEGATIVE,
            "strength": strength
        }
    
    # Positive Window detection
    else:
        # NOTE: window-level positive confirmation requires repeated positive signals
        POSITIVE_CONFIRMATION_THRESHOLD = 5
        confirmed = len(positive_signals) >= POSITIVE_CONFIRMATION_THRESHOLD

        return {
            "confirmed": confirmed,
            "polarity": pattern_polarity_type.POSITIVE,
            "strength": None
        }


def detect_sustained_pattern(windows: list, required_windows: int = 3):
    if len(windows) < required_windows:
        return False

    relevant_windows = windows[-required_windows:]

    for window in relevant_windows:
        if (
        window["polarity"] != pattern_polarity_type.POSITIVE
        or window["confirmed"] is not True
    ):
            return False
    
    return True             
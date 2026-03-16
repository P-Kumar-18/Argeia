from enum import Enum
from app.signals import Signal


# --- Pattern Types ---
class Pattern_polarity_type(Enum):
    NEGATIVE = "negative"
    POSITIVE = "positive" 

class Pattern_strength_type(Enum):
    LOW = "low"
    HIGH = "high"
    NONE = "none"


# --- Detection ---
# NOTE: strength thresholds are provisional and subject to tuning
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
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": strength
        }
    
    # Positive Window detection
    else:
        # NOTE: window-level positive confirmation requires repeated positive signals
        POSITIVE_CONFIRMATION_THRESHOLD = 5
        confirmed = len(positive_signals) >= POSITIVE_CONFIRMATION_THRESHOLD

        return {
            "confirmed": confirmed,
            "polarity": Pattern_polarity_type.POSITIVE,
            "strength": Pattern_strength_type.NONE
        }


def compute_signals(signals: list[Signal])-> list:
    normalized_time = []
    for signal in signals:
        normalized_time.append(int((signal.time / signal.planned_duration) * 100))
    
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

# NOTE: strength thresholds are intentionally stricter than confirmation thresholds
def pattern_confirmation(count: dict):
    if (count["strong"] > 1) or (count["moderate"] > 2) or (count["weak"] > 5):
        return True
    
    return False

def pattern_strength(count: dict):
    if (count["strong"] >= 2) or (count["moderate"] >= 3) or (count["weak"] >= 12):
        return Pattern_strength_type.HIGH
    
    else:
        return Pattern_strength_type.LOW
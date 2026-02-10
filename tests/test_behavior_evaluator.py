from app.behavior_evaluator import evaluate_behavior, Proposal_kind, Proposal_severity
from app.pattern_detection import Pattern_polarity_type, Pattern_strength_type

def test_negative_pattern_priority_over_positive_sustained():
    window_1 = [{"polarity": Pattern_polarity_type.POSITIVE, "confirmed": True}]
    window_2 = [{"polarity": Pattern_polarity_type.POSITIVE, "confirmed": True}]
    window_3 = [
        {"polarity": Pattern_polarity_type.POSITIVE, "confirmed": True},
        {"polarity": Pattern_polarity_type.NEGATIVE, "confirmed": True, "strength": Pattern_strength_type.HIGH},
        {"polarity": Pattern_polarity_type.NEGATIVE, "confirmed": True, "strength": Pattern_strength_type.HIGH}
    ]

    proposal = evaluate_behavior(
        previous_windows=[window_1, window_2],
        current_window=window_3
    )

    assert proposal["kind"] == Proposal_kind.DEGRADATION
    assert proposal["severity"] == Proposal_severity.SEVERE

def test_adjacent_low_negatives_trigger_degradation():
    previous_windows = [
        [{"polarity": Pattern_polarity_type.NEGATIVE, "confirmed": True, "strength": Pattern_strength_type.LOW}]
    ]

    current_window = [
        {"polarity": Pattern_polarity_type.NEGATIVE, "confirmed": True, "strength": Pattern_strength_type.LOW}
    ]

    proposal = evaluate_behavior(
        previous_windows=previous_windows,
        current_window=current_window
    )

    assert proposal["kind"] == Proposal_kind.DEGRADATION
    assert proposal["severity"] == Proposal_severity.NORMAL


def test_single_high_negative_triggers_degradation():
    current_window = [
        {"polarity": Pattern_polarity_type.NEGATIVE, "confirmed": True, "strength": Pattern_strength_type.HIGH}
    ]

    proposal = evaluate_behavior(
        current_window=current_window
    )

    assert proposal["kind"] == Proposal_kind.DEGRADATION
    assert proposal["severity"] == Proposal_severity.NORMAL


def test_multiple_high_negatives_in_same_window_trigger_severe():
    current_window = [
        {"polarity": Pattern_polarity_type.NEGATIVE, "confirmed": True, "strength": Pattern_strength_type.HIGH},
        {"polarity": Pattern_polarity_type.NEGATIVE, "confirmed": True, "strength": Pattern_strength_type.HIGH}
    ]

    proposal = evaluate_behavior(
        current_window=current_window,
    )

    assert proposal["kind"] == Proposal_kind.DEGRADATION
    assert proposal["severity"] == Proposal_severity.SEVERE


def test_three_consecutive_positive_windows_trigger_recovery():
    window_1 = [{"polarity": Pattern_polarity_type.POSITIVE, "confirmed": True}]
    window_2 = [{"polarity": Pattern_polarity_type.POSITIVE, "confirmed": True}]
    window_3 = [{"polarity": Pattern_polarity_type.POSITIVE, "confirmed": True}]

    proposal = evaluate_behavior(
        previous_windows=[window_1, window_2],
        current_window=window_3
    )

    assert proposal["kind"] == Proposal_kind.RECOVERY
    assert proposal["severity"] == Proposal_severity.NORMAL
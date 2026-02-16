from app.behavior_evaluator import evaluate_behavior
from app.pattern_detection import Pattern_polarity_type, Pattern_strength_type
from app.state_engine import State, apply_proposal

"""
    Baseline Stability
"""
def test_high_negative_degrade_once():
    state = State.STABLE

    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        }
    ]

    proposal = evaluate_behavior(window_1)

    state = apply_proposal(state, proposal)

    assert state == State.DRIFTING


"""
    Adjacent Logic
"""
def test_two_consecutive_low_negatives_degrade_once():
    state = State.STABLE

    # Window 1
    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        }
    ]

    proposal = evaluate_behavior(window_1)

    state = apply_proposal(state, proposal)

    assert state == State.STABLE

    # Window 2
    window_2 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        }
    ]

    proposal = evaluate_behavior(window_2, [window_1])

    state = apply_proposal(state, proposal)

    assert state == State.DRIFTING


def test_low_clean_low_does_not_degrade():
    state = State.STABLE

    # Window 1
    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        }
    ]

    proposal = evaluate_behavior(window_1)

    state = apply_proposal(state, proposal)

    assert state == State.STABLE

    # Window 2
    window_2 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    proposal = evaluate_behavior(window_2, [window_1])

    state = apply_proposal(state, proposal)

    assert state == State.STABLE

    # Window 3
    window_3 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        }
    ]

    proposal = evaluate_behavior(window_3, [window_1, window_2])

    state = apply_proposal(state, proposal)

    assert state == State.STABLE


def test_two_low_in_same_window_degrade_once():
    state = State.STABLE

    window = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        }
    ]

    proposal = evaluate_behavior(window)
    state = apply_proposal(state, proposal)

    assert state == State.DRIFTING


def test_high_and_low_same_window_degrade_normally():
    state = State.STABLE

    window = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        }
    ]

    proposal = evaluate_behavior(window)
    state = apply_proposal(state, proposal)

    assert state == State.DRIFTING


"""
    Severe Escalation
"""
def test_repeated_high_negative_cause_severe_degredation():
    state = State.STABLE

    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        }
    ]

    proposal = evaluate_behavior(window_1)

    state = apply_proposal(state, proposal)

    assert state == State.STRAINED


def test_severe_degredation_from_strained():
    state = State.STRAINED

    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        }
    ]

    proposal = evaluate_behavior(window_1)

    state = apply_proposal(state, proposal)

    assert state == State.DISENGAGED


def test_severe_from_stable_does_not_skip_two_levels():
    state = State.STABLE

    window = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        }
    ]

    proposal = evaluate_behavior(window)
    state = apply_proposal(state, proposal)

    assert state != State.DISENGAGED


"""
    Multistep Degredation
"""
def test_consecutive_high_degrade_stepwise():
    state = State.STABLE

    # Window 1
    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        }
    ]

    proposal = evaluate_behavior(window_1)

    state = apply_proposal(state, proposal)

    assert state == State.DRIFTING


    # Window 2
    window_2 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        }
    ]

    proposal = evaluate_behavior(window_2, [window_1])

    state = apply_proposal(state, proposal)

    assert state == State.STRAINED

    # Window 3
    window_3 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        }
    ]

    proposal = evaluate_behavior(window_3, [window_1, window_2])

    state = apply_proposal(state, proposal)

    assert state == State.DISENGAGED


"""
    Recovery Logic
"""
def test_three_consecutive_possitive_windows_recover():
    state = State.DRIFTING

    # Window 1
    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    # Window 2
    window_2 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    # Window 3
    window_3 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    proposal = evaluate_behavior(window_3, [window_1, window_2])

    state = apply_proposal(state, proposal)

    assert state == State.STABLE


def test_recovery_does_nothing_if_the_state_is_stable():
    state = State.STABLE

    # Window 1
    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    # Window 2
    window_2 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    # Window 3
    window_3 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    proposal = evaluate_behavior(window_3, [window_1, window_2])

    state = apply_proposal(state, proposal)

    assert state == State.STABLE


"""
    Conflict Resolution
"""
def test_negative_breaks_possitive_streak():
    state = State.DRIFTING

    # Window 1
    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    # Window 2
    window_2 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    # Window 3
    window_3 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.LOW
        }
    ]

    proposal = evaluate_behavior(window_3, [window_1, window_2])

    state = apply_proposal(state, proposal)

    assert state == State.DRIFTING


def test_severe_over_recovery():
    state = State.DRIFTING

    # Window 1
    window_1 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    # Window 2
    window_2 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        }
    ]

    # Window 3
    window_3 = [
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.POSITIVE
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        },
        {
            "confirmed": True,
            "polarity": Pattern_polarity_type.NEGATIVE,
            "strength": Pattern_strength_type.HIGH
        }
    ]

    proposal = evaluate_behavior(window_3, [window_1, window_2])

    state = apply_proposal(state, proposal)

    assert state == State.DISENGAGED


"""
    No-Op Behavior
"""
def test_no_proposal_does_nothing():
    state = State.DRIFTING

    window_1 = []

    proposal = evaluate_behavior(window_1)

    state = apply_proposal(state, proposal)

    assert state == State.DRIFTING
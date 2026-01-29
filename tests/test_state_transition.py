from app.state_engine import State_Engine, State, Pattern


"""
    Section 1 - No Confirmed Pattern zdoes nothing
"""

def test_stable_with_no_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=False)
    result = engine.transition(
        current_state=State.STABLE,
        pattern=pattern
    )

    assert result == State.STABLE


def test_drifting_with_no_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=False)
    result = engine.transition(
        current_state=State.DRIFTING,
        pattern=pattern
    )

    assert result == State.DRIFTING


def test_strained_with_no_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=False)
    result = engine.transition(
        current_state=State.STRAINED,
        pattern=pattern
    )

    assert result == State.STRAINED


def test_disengaged_with_no_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=False)
    result = engine.transition(
        current_state=State.DISENGAGED,
        pattern=pattern
    )

    assert result == State.DISENGAGED


"""
    Section 2 - Unconfirmed Pattern or Weak Pattern do nothing
"""

def test_stable_with_weak_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, weak=True)

    result = engine.transition(
        current_state=State.STABLE,
        pattern=pattern
    )

    assert result == State.STABLE


def test_drifting_with_weak_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, weak=True)

    result = engine.transition(
        current_state=State.DRIFTING,
        pattern=pattern
    )

    assert result == State.DRIFTING


def test_strained_with_weak_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, weak=True)

    result = engine.transition(
        current_state=State.STRAINED,
        pattern=pattern
    )

    assert result == State.STRAINED


def test_disengaged_with_weak_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, weak=True)

    result = engine.transition(
        current_state=State.DISENGAGED,
        pattern=pattern
    )

    assert result == State.DISENGAGED


"""
    Section 3 - Standard Degradation (one step at a time)
"""

def test_stable_with_negative_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, negative_confirmed=True)

    result = engine.transition(
        current_state=State.STABLE,
        pattern=pattern
    )

    assert result == State.DRIFTING
    
    
def test_drifting_with_negative_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, negative_confirmed=True)

    result = engine.transition(
        current_state=State.DRIFTING,
        pattern=pattern
    )

    assert result == State.STRAINED

    
def test_strained_with_negative_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, negative_confirmed=True)

    result = engine.transition(
        current_state=State.STRAINED,
        pattern=pattern
    )

    assert result == State.DISENGAGED

    
def test_disengaged_with_negative_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, negative_confirmed=True)

    result = engine.transition(
        current_state=State.DISENGAGED,
        pattern=pattern
    )

    assert result == State.DISENGAGED


"""
    Section 4 - Escalated Degradation
"""

def test_stable_with_severe_degradation():
    engine = State_Engine()
    pattern = Pattern(exists=True, negative_confirmed=True, severe=True)

    result = engine.transition(
        current_state=State.STABLE,
        pattern=pattern
    )

    assert result == State.STRAINED
    assert result != State.DISENGAGED


def test_drifting_with_severe_degradation():
    engine = State_Engine()
    pattern = Pattern(exists=True, negative_confirmed=True, severe=True)

    result = engine.transition(
        current_state=State.DRIFTING,
        pattern=pattern
    )

    assert result == State.DISENGAGED


def test_strained_with_severe_degradation():
    engine = State_Engine()
    pattern = Pattern(exists=True, negative_confirmed=True, severe=True)

    result = engine.transition(
        current_state=State.STRAINED,
        pattern=pattern
    )

    assert result == State.DISENGAGED


def test_disengaged_with_severe_degradation():
    engine = State_Engine()
    pattern = Pattern(exists=True, negative_confirmed=True, severe=True)

    result = engine.transition(
        current_state=State.DISENGAGED,
        pattern=pattern
    )

    assert result == State.DISENGAGED


"""
    Section 5 - Recovery is Slow and Earned
"""

def test_stable_with_positive_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, positive_confirmed=True, sustained=True)

    result = engine.transition(
        current_state=State.STABLE,
        pattern=pattern
    )

    assert result == State.STABLE


def test_drifting_with_positive_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, positive_confirmed=True)

    result = engine.transition(
        current_state=State.DRIFTING,
        pattern=pattern
    )

    assert result == State.STABLE


def test_strained_with_positive_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, positive_confirmed=True)

    result = engine.transition(
        current_state=State.STRAINED,
        pattern=pattern
    )

    assert result == State.DRIFTING


def test_disengaged_with_positive_pattern():
    engine = State_Engine()
    pattern = Pattern(exists=True, positive_confirmed=True)

    result = engine.transition(
        current_state=State.DISENGAGED,
        pattern=pattern
    )

    assert result == State.STRAINED


"""
    Section 6 - Symmetry checks
"""

def test_negative_pattern_blocks_recovery():
    engine = State_Engine()

    pattern = Pattern(exists=True, negative_confirmed=True, positive_confirmed=True)

    result = engine.transition(
        State.DRIFTING, 
        pattern=pattern)

    assert result == State.DRIFTING


def test_recovery_from_disengaged_is_one_step_only():
    engine = State_Engine()

    pattern = Pattern(exists=True, positive_confirmed=True, sustained=True)

    result = engine.transition(
        State.DISENGAGED, 
        pattern=pattern)

    assert result == State.STRAINED
    assert result != State.DRIFTING
    assert result != State.STABLE

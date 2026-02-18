from app.state_engine import State, apply_proposal
from app.behavior_evaluator import Proposal_kind, Proposal_severity, Proposal


"""
    Section 1 - No proposal["kind"] does nothing
"""

def test_stable_with_no_proposal_kind():
    proposal = None
    result_state, tansition = apply_proposal(
        current_state=State.STABLE,
        proposal=proposal
    )

    assert result_state == State.STABLE


def test_drifting_with_no_proposal_kind():
    proposal = None
    result_state, tansition = apply_proposal(
        current_state=State.DRIFTING,
        proposal=proposal
    )

    assert result_state == State.DRIFTING


def test_strained_with_no_proposal_kind():
    proposal = None
    result_state, tansition = apply_proposal(
        current_state=State.STRAINED,
        proposal=proposal
    )

    assert result_state == State.STRAINED


def test_disengaged_with_no_pattern():
    proposal = None
    result_state, tansition = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result_state == State.DISENGAGED


"""
    Section 3 - Standard Degradation (one step at a time)
"""

def test_stable_with_negative_proposal():
    proposal = Proposal(Proposal_kind.DEGRADATION, Proposal_severity.NORMAL)
    result_state, tansition = apply_proposal(
        current_state=State.STABLE,
        proposal=proposal
    )

    assert result_state == State.DRIFTING
    
    
def test_drifting_with_negative_proposal():
    proposal = Proposal(Proposal_kind.DEGRADATION, Proposal_severity.NORMAL)
    result_state, tansition = apply_proposal(
        current_state=State.DRIFTING,
        proposal=proposal
    )

    assert result_state == State.STRAINED

    
def test_strained_with_negative_proposal():
    proposal = Proposal(Proposal_kind.DEGRADATION, Proposal_severity.NORMAL)
    result_state, tansition = apply_proposal(
        current_state=State.STRAINED,
        proposal=proposal
    )

    assert result_state == State.DISENGAGED

    
def test_disengaged_with_negative_proposal():
    proposal = Proposal(Proposal_kind.DEGRADATION, Proposal_severity.NORMAL)
    result_state, tansition = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result_state == State.DISENGAGED


"""
    Section 4 - Escalated Degradation
"""

def test_stable_with_severe_degradation():
    proposal = Proposal(Proposal_kind.DEGRADATION, Proposal_severity.SEVERE)
    result_state, tansition = apply_proposal(
        current_state=State.STABLE,
        proposal=proposal
    )

    assert result_state == State.STRAINED
    assert result_state != State.DISENGAGED


def test_drifting_with_severe_degradation():
    proposal = Proposal(Proposal_kind.DEGRADATION, Proposal_severity.SEVERE)
    result_state, tansition = apply_proposal(
        current_state=State.DRIFTING,
        proposal=proposal
    )

    assert result_state == State.DISENGAGED


def test_strained_with_severe_degradation():
    proposal = Proposal(Proposal_kind.DEGRADATION, Proposal_severity.SEVERE)
    result_state, tansition = apply_proposal(
        current_state=State.STRAINED,
        proposal=proposal
    )

    assert result_state == State.DISENGAGED


def test_disengaged_with_severe_degradation():
    proposal = Proposal(Proposal_kind.DEGRADATION, Proposal_severity.SEVERE)
    result_state, tansition = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result_state == State.DISENGAGED


"""
    Section 5 - Recovery is Slow and Earned
"""

def test_stable_with_positive_proposal():
    proposal = Proposal(Proposal_kind.RECOVERY, Proposal_severity.NORMAL)
    result_state, tansition = apply_proposal(
        current_state=State.STABLE,
        proposal=proposal
    )

    assert result_state == State.STABLE


def test_drifting_with_positive_pattern():
    proposal = Proposal(Proposal_kind.RECOVERY, Proposal_severity.NORMAL)
    result_state, tansition = apply_proposal(
        current_state=State.DRIFTING,
        proposal=proposal
    )

    assert result_state == State.STABLE


def test_strained_with_positive_pattern():
    proposal = Proposal(Proposal_kind.RECOVERY, Proposal_severity.NORMAL)
    result_state, tansition = apply_proposal(
        current_state=State.STRAINED,
        proposal=proposal
    )

    assert result_state == State.DRIFTING


def test_disengaged_with_positive_pattern():
    proposal = Proposal(Proposal_kind.RECOVERY, Proposal_severity.NORMAL)
    result_state, tansition = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result_state == State.STRAINED


"""
    Section 6 - Symmetry checks
"""

def test_recovery_from_disengaged_is_one_step_only():
    proposal = Proposal(Proposal_kind.RECOVERY, Proposal_severity.NORMAL)
    result_state, transition = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result_state == State.STRAINED
    assert result_state != State.DRIFTING
    assert result_state != State.STABLE

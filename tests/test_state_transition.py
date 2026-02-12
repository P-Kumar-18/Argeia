from app.state_engine import State, apply_proposal
from app.behavior_evaluator import Proposal_kind, Proposal_severity


"""
    Section 1 - No proposal["kind"] does nothing
"""

def test_stable_with_no_proposal_kind():
    proposal = {
        "kind": None,
        "severity": None
    }
    result = apply_proposal(
        current_state=State.STABLE,
        proposal=proposal
    )

    assert result == State.STABLE


def test_drifting_with_no_proposal_kind():
    proposal = {
        "kind": None,
        "severity": None
    }
    result = apply_proposal(
        current_state=State.DRIFTING,
        proposal=proposal
    )

    assert result == State.DRIFTING


def test_strained_with_no_proposal_kind():
    proposal = {
        "kind": None,
        "severity": None
    }
    result = apply_proposal(
        current_state=State.STRAINED,
        proposal=proposal
    )

    assert result == State.STRAINED


def test_disengaged_with_no_pattern():
    proposal = {
        "kind": None,
        "severity": None
    }
    result = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result == State.DISENGAGED


"""
    Section 3 - Standard Degradation (one step at a time)
"""

def test_stable_with_negative_proposal():
    proposal = {
        "kind": Proposal_kind.DEGRADATION,
        "severity": Proposal_severity.NORMAL
    }
    result = apply_proposal(
        current_state=State.STABLE,
        proposal=proposal
    )

    assert result == State.DRIFTING
    
    
def test_drifting_with_negative_proposal():
    proposal = {
        "kind": Proposal_kind.DEGRADATION,
        "severity": Proposal_severity.NORMAL
    }
    result = apply_proposal(
        current_state=State.DRIFTING,
        proposal=proposal
    )

    assert result == State.STRAINED

    
def test_strained_with_negative_proposal():
    proposal = {
        "kind": Proposal_kind.DEGRADATION,
        "severity": Proposal_severity.NORMAL
    }
    result = apply_proposal(
        current_state=State.STRAINED,
        proposal=proposal
    )

    assert result == State.DISENGAGED

    
def test_disengaged_with_negative_proposal():
    proposal = {
        "kind": Proposal_kind.DEGRADATION,
        "severity": Proposal_severity.NORMAL
    }
    result = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result == State.DISENGAGED


"""
    Section 4 - Escalated Degradation
"""

def test_stable_with_severe_degradation():
    proposal = {
        "kind": Proposal_kind.DEGRADATION,
        "severity": Proposal_severity.SEVERE
    }
    result = apply_proposal(
        current_state=State.STABLE,
        proposal=proposal
    )

    assert result == State.STRAINED
    assert result != State.DISENGAGED


def test_drifting_with_severe_degradation():
    proposal = {
        "kind": Proposal_kind.DEGRADATION,
        "severity": Proposal_severity.SEVERE
    }
    result = apply_proposal(
        current_state=State.DRIFTING,
        proposal=proposal
    )

    assert result == State.DISENGAGED


def test_strained_with_severe_degradation():
    proposal = {
        "kind": Proposal_kind.DEGRADATION,
        "severity": Proposal_severity.SEVERE
    }
    result = apply_proposal(
        current_state=State.STRAINED,
        proposal=proposal
    )

    assert result == State.DISENGAGED


def test_disengaged_with_severe_degradation():
    proposal = {
        "kind": Proposal_kind.DEGRADATION,
        "severity": Proposal_severity.SEVERE
    }
    result = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result == State.DISENGAGED


"""
    Section 5 - Recovery is Slow and Earned
"""

def test_stable_with_positive_proposal():
    proposal = {
        "kind": Proposal_kind.RECOVERY,
        "severity": Proposal_severity.NORMAL
    }
    result = apply_proposal(
        current_state=State.STABLE,
        proposal=proposal
    )

    assert result == State.STABLE


def test_drifting_with_positive_pattern():
    proposal = {
        "kind": Proposal_kind.RECOVERY,
        "severity": Proposal_severity.NORMAL
    }
    result = apply_proposal(
        current_state=State.DRIFTING,
        proposal=proposal
    )

    assert result == State.STABLE


def test_strained_with_positive_pattern():
    proposal = {
        "kind": Proposal_kind.RECOVERY,
        "severity": Proposal_severity.NORMAL
    }
    result = apply_proposal(
        current_state=State.STRAINED,
        proposal=proposal
    )

    assert result == State.DRIFTING


def test_disengaged_with_positive_pattern():
    proposal = {
        "kind": Proposal_kind.RECOVERY,
        "severity": Proposal_severity.NORMAL
    }
    result = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result == State.STRAINED


"""
    Section 6 - Symmetry checks
"""

def test_recovery_from_disengaged_is_one_step_only():
    proposal = {
        "kind": Proposal_kind.RECOVERY,
        "severity": Proposal_severity.NORMAL
    }
    result = apply_proposal(
        current_state=State.DISENGAGED,
        proposal=proposal
    )

    assert result == State.STRAINED
    assert result != State.DRIFTING
    assert result != State.STABLE

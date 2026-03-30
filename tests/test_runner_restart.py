from app.core import State, Proposal, Proposal_kind, Proposal_severity
from app.infrastructure import TransitionRepository, WindowRepository
from app.runner import BehaviorRunner


def test_restart_with_empty_db_initializes_stable():
    repo = TransitionRepository(db_path=":memory:")
    runner = BehaviorRunner(transition_repository=repo, window_repository=WindowRepository(db_path=":memory:"))

    assert runner.current_state == State.STABLE


def test_restart_restores_last_state():

    repo = TransitionRepository(db_path=":memory:")
    runner = BehaviorRunner(transition_repository=repo, window_repository=WindowRepository(db_path=":memory:"))

    proposal = Proposal(
        kind=Proposal_kind.DEGRADATION,
        severity=Proposal_severity.NORMAL,
        evidence_reason="test"
    )

    runner.process_proposal(proposal)
    new_runner = BehaviorRunner(transition_repository=repo, window_repository=WindowRepository(db_path=":memory:"))

    assert new_runner.current_state == State.DRIFTING


def test_restart_uses_latest_transition():

    repo = TransitionRepository(db_path=":memory:")
    runner = BehaviorRunner(transition_repository=repo, window_repository=WindowRepository(db_path=":memory:"))

    # 1st degradation
    runner.process_proposal(Proposal(
        Proposal_kind.DEGRADATION,
        Proposal_severity.NORMAL,
        "test"
    ))

    # 2nd degradation
    runner.process_proposal(Proposal(
        Proposal_kind.DEGRADATION,
        Proposal_severity.NORMAL,
        "test"
    ))

    new_runner = BehaviorRunner(transition_repository=repo, window_repository=WindowRepository(db_path=":memory:"))

    assert new_runner.current_state == State.STRAINED
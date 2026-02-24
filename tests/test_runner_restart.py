from app.behavior_runner import BehaviorRunner
from app.infrastructure.transition_repository import TransitionRepository
from app.state_engine import State
from app.behavior_evaluator import Proposal, Proposal_kind, Proposal_severity


def test_restart_with_empty_db_initializes_stable():
    repo = TransitionRepository(db_path=":memory:")

    runner = BehaviorRunner(repository=repo)

    assert runner.current_state == State.STABLE


def test_restart_restores_last_state():

    repo = TransitionRepository(db_path=":memory:")

    runner = BehaviorRunner(repository=repo)

    proposal = Proposal(
        kind=Proposal_kind.DEGRADATION,
        severity=Proposal_severity.NORMAL,
        evidence_reason="test"
    )

    runner.process_proposal(proposal)

    new_runner = BehaviorRunner(repository=repo)

    assert new_runner.current_state == State.DRIFTING


def test_restart_uses_latest_transition():

    repo = TransitionRepository(db_path=":memory:")

    runner = BehaviorRunner(repository=repo)

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

    new_runner = BehaviorRunner(repository=repo)

    assert new_runner.current_state == State.STRAINED
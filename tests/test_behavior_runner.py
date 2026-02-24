from app.behavior_runner import BehaviorRunner
from app.behavior_evaluator import Proposal, Proposal_kind, Proposal_severity
from app.state_engine import State

class FakeRepository:
    def __init__(self):
        self.saved = []
        self.latest = None


    def save(self, transition):
        self.saved.append(transition)
    

    def get_latest(self):
        return self.latest


def test_no_proposal_does_not_change_state_or_save():
    repo = FakeRepository()
    runner = BehaviorRunner(repository=repo)

    new_state = runner.process_proposal(None)

    assert new_state == State.STABLE
    assert len(repo.saved) == 0


def test_degradation_proposal_triggers_transition_and_save():
    repo = FakeRepository()
    runner = BehaviorRunner(repository=repo)

    proposal = Proposal(
        kind=Proposal_kind.DEGRADATION,
        severity=Proposal_severity.NORMAL,
        evidence_reason="consecutive_negative_confirmed"
    )

    new_state = runner.process_proposal(proposal)

    assert new_state == State.DRIFTING
    assert len(repo.saved) == 1

    transition = repo.saved[0]
    assert transition.previous_state == State.STABLE
    assert transition.current_state == State.DRIFTING


def test_no_transition_no_save():
    repo = FakeRepository()
    runner = BehaviorRunner(initial_state=State.DISENGAGED, repository=repo)

    proposal = Proposal(
        kind=Proposal_kind.DEGRADATION,
        severity=Proposal_severity.NORMAL,
        evidence_reason="continued_negative"
    )

    new_state = runner.process_proposal(proposal)

    assert new_state == State.DISENGAGED
    assert len(repo.saved) == 0
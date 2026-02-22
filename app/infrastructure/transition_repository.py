import sqlite3
from app.state_engine import Transition

class TransitionRepository:
    def save(
        self,
        transition: Transition
        ):
        with sqlite3.connect("../data/argeia.db") as connection:
            cursor = connection.cursor()

            cursor.execute("""INSERT INTO transitions (
                    previous_state,
                    current_state,
                    proposal_kind,
                    proposal_severity,
                    evidence_reason,
                    timestamp
                ) VALUES (?,?,?,?,?,?)""", (
                transition.previous_state.value, 
                transition.current_state.value, 
                transition.proposal_kind.value, 
                transition.proposal_severity.value, 
                transition.evidence_reason, 
                transition.timestamp.isoformat()
            ))
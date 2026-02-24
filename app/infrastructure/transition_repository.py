import sqlite3, datetime
from app.infrastructure.database import Database
from app.state_engine import Transition, State
from app.behavior_evaluator import Proposal, Proposal_kind, Proposal_severity


def convert_row(
        previous_state,
        current_state,
        proposal_kind,
        proposal_severity,
        evidence_reason,
        timestamp
):
    proposal = Proposal(Proposal_kind(proposal_kind), Proposal_severity(proposal_severity), evidence_reason)
    return Transition(State(previous_state), State(current_state), proposal, datetime.datetime.fromisoformat(timestamp))


class TransitionRepository:
    def __init__(self, db_path = "../data/argeia.db"):
        self.db_path = db_path
        self.database = Database(self.db_path)


    def save(
        self,
        transition: Transition
    ):
        cursor = self.database.connection.cursor()

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

        self.database.connection.commit()
    

    def get_latest(
            self
    ):
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM transitions ORDER BY id DESC LIMIT 1")

        row = cursor.fetchone()
        if row == None:
            return None
        else:
            return convert_row(row[1], row[2], row[3], row[4], row[5], row[6])

    def get_all(
            self
    ):
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM transitions")
        
        rows = cursor.fetchall()
        if len(rows) == 0:
            return []
        else:
            transition_list = []
            for row in rows:
                transition_list.append(convert_row(row[1], row[2], row[3], row[4], row[5], row[6]))
            
            return transition_list
    

    def get_latest_n(
            self,
            n
    ):
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM transitions ORDER BY id DESC LIMIT ?", (n,))

        rows = cursor.fetchall()
        if len(rows) == 0:
            return []
        else:
            transition_list = []
            for row in rows:
                transition_list.append(convert_row(row[1], row[2], row[3], row[4], row[5], row[6]))
            
            return transition_list
    

    def close(
            self
    ):
        self.database.connection.close()
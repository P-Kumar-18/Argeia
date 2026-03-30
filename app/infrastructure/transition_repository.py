import datetime
import sqlite3
from app.core import Transition, State, Proposal, Proposal_kind, Proposal_severity
from app.infrastructure import Database


# --- Converters ---
def convert_row(row):
    proposal = Proposal(
        Proposal_kind(row["proposal_kind"]),
        Proposal_severity(row["proposal_severity"]),
        row["evidence_reason"]
    )
    return Transition(
        State(row["previous_state"]),
        State(row["current_state"]),
        proposal,
        datetime.datetime.fromisoformat(row["timestamp"])
    )


# --- Transition Repository ---
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
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM transitions ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        if row == None:
            return None
        else:
            return convert_row(row)

    def get_latest_n(
            self,
            n
    ):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM transitions ORDER BY id DESC LIMIT ?", (n,))

        rows = cursor.fetchall()
        if len(rows) == 0:
            return []
        else:
            transition_list = []
            for row in rows:
                transition_list.append(convert_row(row))
            
            return transition_list

    def get_all(
            self
    ):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM transitions")
        rows = cursor.fetchall()
        if len(rows) == 0:
            return []
        else:
            transition_list = []
            for row in rows:
                transition_list.append(convert_row(row))
            
            return transition_list

    def close(
            self
    ):
        self.database.connection.close()
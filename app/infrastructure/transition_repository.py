import datetime
import sqlite3
from app.core import Transition, State, Proposal, Proposal_kind, Proposal_severity, Proposal_windows_scope
from .database import Database, get_default_path


# --- Getting default database path ---
db_path = get_default_path()


# --- Converters ---
def convert_row(row, ev_reason):

    proposal = Proposal(
        Proposal_kind(row["proposal_kind"]),
        Proposal_severity(row["proposal_severity"]),
        ev_reason
    )
    return Transition(
        State(row["previous_state"]),
        State(row["current_state"]),
        proposal,
        datetime.datetime.fromisoformat(row["timestamp"])
    )


# --- Transition Repository ---
class TransitionRepository:
    def __init__(self, db_path=db_path):
        self.db_path = db_path
        self.database = Database(self.db_path)

    def save(
        self,
        transition: Transition
    ):
        cursor = self.database.connection.cursor()

        cursor.execute("""INSERT INTO transition_reasons (
                high_count,
                low_count,
                window_scope,
                sustained_trigger
            ) VALUES (?, ?, ?, ?)""", (
            transition.evidence_reason["high_count"],
            transition.evidence_reason["low_count"],
            transition.evidence_reason["window_scope"].value,
            transition.evidence_reason["sustained_trigger"]
        ))

        reason_id = cursor.lastrowid

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
            reason_id, 
            transition.timestamp.isoformat()
        ))

        self.database.connection.commit()
    
    def get_transtion_reasons(
            self,
            id
        ):
        self.database.connection.row_factory = sqlite3.Row
        cursor = self.database.connection.cursor()

        cursor.execute("SELECT * FROM transition_reasons WHERE id = ?", (id,))

        row = cursor.fetchone()

        return {
            "high_count": row["high_count"],
            "low_count": row["low_count"],
            "window_scope": Proposal_windows_scope(row["window_scope"]),
            "sustained_trigger": True if row["sustained_trigger"] == '1' else False
        }


    
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
            ev_reason = self.get_transtion_reasons(row["evidence_reason"])
            return convert_row(row, ev_reason)

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
                ev_reason = self.get_transtion_reasons(row["evidence_reason"])
                transition_list.append(convert_row(row, ev_reason))
            
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
                ev_reason = self.get_transtion_reasons(row["evidence_reason"])
                transition_list.append(convert_row(row, ev_reason))
            
            return transition_list
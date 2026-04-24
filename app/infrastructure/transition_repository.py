import datetime
import sqlite3
from app.core import Transition, State, Proposal, Proposal_kind, Proposal_severity, Proposal_windows_scope
from .database import Database, get_default_path


# --- Getting default database path ---
db_path = get_default_path()


def to_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "t", "yes", "y"}
    return bool(value)


def normalize_evidence_reason(evidence_reason):
    if isinstance(evidence_reason, dict):
        return {
            "high_count": evidence_reason.get("high_count", 0),
            "low_count": evidence_reason.get("low_count", 0),
            "windows_scope": evidence_reason.get("windows_scope", Proposal_windows_scope.SINGLE_WINDOW),
            "sustained_trigger": bool(evidence_reason.get("sustained_trigger", False))
        }

    return {
        "high_count": 0,
        "low_count": 0,
        "windows_scope": Proposal_windows_scope.SINGLE_WINDOW,
        "sustained_trigger": False
    }


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
        evidence_reason = normalize_evidence_reason(transition.evidence_reason)

        cursor.execute("""INSERT INTO transition_reasons (
                high_count,
                low_count,
                windows_scope,
                sustained_trigger
            ) VALUES (?, ?, ?, ?)""", (
            evidence_reason["high_count"],
            evidence_reason["low_count"],
            evidence_reason["windows_scope"].value,
            int(bool(evidence_reason["sustained_trigger"]))
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
    
    def get_transition_reasons(
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
            "windows_scope": Proposal_windows_scope(row["windows_scope"]),
            "sustained_trigger": to_bool(row["sustained_trigger"])
        }

    # Backward-compatible alias for old typo.
    def get_transtion_reasons(self, id):
        return self.get_transition_reasons(id)

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
            ev_reason = self.get_transition_reasons(row["evidence_reason"])
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
                ev_reason = self.get_transition_reasons(row["evidence_reason"])
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
                ev_reason = self.get_transition_reasons(row["evidence_reason"])
                transition_list.append(convert_row(row, ev_reason))
            
            return transition_list
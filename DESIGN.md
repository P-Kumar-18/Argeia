# Argeia – Procrastination System Design

This document captures the **finalized design decisions** for Argeia’s procrastination modeling system.
It intentionally separates **design intent** from **implementation details**, so logic can evolve without losing meaning.

---

## 1. Core Philosophy

Argeia does **not** treat procrastination as a single mistake or a moral failure.

Instead, procrastination is defined as:

> **A pattern of breaking self-imposed commitments over time.**

The system is designed to be:
- Fair to one-off accidents
- Honest about emerging bad habits
- Forgiving when improvement is sustained
- Clear and explainable to the user

---

## 2. Design Scope & Sources of Truth

This document defines Argeia’s **high-level philosophy, guarantees, and system structure**.

The **authoritative specification** for behavioral states and state transition rules is defined separately in:

> **`docs/behavior_model.md`**

This separation is intentional:
- `DESIGN.md` explains **why** the system behaves the way it does
- `behavior_model.md` defines **how behavior is interpreted over time**

Any implementation must follow the rules defined in `docs/behavior_model.md`.

---

## 3. Design Layers (High-Level Architecture)

Argeia models behavior using five layers:

```
Events → Signals → Patterns → Behavior Evaluation → State → Score
```

Each layer has a **single responsibility**.

Behavior Evaluation interprets pattern evidence across windows and produces a proposal (degradation or recovery) 
The state engine consumes proposals but does not inspect patterns directly

---

## 4. Events (Raw User Actions)

Events are **atomic facts**. They are recorded but not judged.

Examples:
- Task started late
- Task stopped early
- Task never started
- Task completed fully
- Task completed "good enough"

A single event:
- NEVER changes state
- MAY slightly affect score
- ALWAYS contributes to signal history

---

## 5. Signals (Quantified Deviations)

Signals convert events into measurable deviations.

### Primary Signals

- **Delay**: Minutes late relative to scheduled start
- **Underwork**: Planned duration minus actual duration
- **Timeout**: Full planned duration when task was never started

Signals are:
- Objective
- Time-based
- Non-judgmental

Signals may exist even when behavior is considered "good enough".

---

## 6. Patterns (Behavioral Evidence)

Patterns determine whether signals represent noise or habit formation.

Patterns are detected across:

### A. Intra-task consistency
- Repeated avoidance of the same task
- Repeated early stopping for the same task

### B. Inter-task consistency
- Lateness across many tasks
- Early stopping across many tasks
- Repeated missed tasks

Patterns do not change state directly. They provide evidence that is interpreted by the behavior evaluation layer

---

## 7. Behavior Evaluation (Interpretation Layer)

Patterns provide behavioral evidence but do not change state directly.

The Behavior Evaluation layer interprets pattern evidence across windows and produces a structured proposal:
- *DEGREDATION (NORMAL)*
- *DEGREDATION (SEVERE)*
- *RECOVERY*
- no proposal

This layer is responsible for:
- Escalation logic (e.g., multiple high-severity negatives)
- Adjacent window evaluation
- Sustained positive detection
- Conflict resolution (degradation overrides recovery)

The state engine does not inspect patterns. It only consumes proposals.

## 8. Behavioral States (Primary Feedback)

States represent the system’s interpretation of behavior.

States are **slow-changing** and pattern-driven.

### 🟢 Stable
- Schedule mostly followed
- Minor deviations recover quickly
- Strong consistency

### 🟡 Drifting
- Repeated "good enough" behavior
- Small deviations accumulating
- Early warning state

### 🟠 Strained
- Clear deviations
- Streak broken
- Pattern confirmed

### 🔴 Disengaged
- Repeated missed tasks
- Abandonment
- Schedule largely ignored

### State Transition Rules
- Single events NEVER change state
- Degradation proposals move state one step at a time unless marked severe
- State skipping allowed ONLY via confirmed escalation patterns
- Recovery occurs gradually through sustained improvement
- Recovery proposals move state one step at a time

---

## 9. Memory Model (Hybrid)

Argeia uses a **hybrid memory system**:

### Rolling Window (Primary)
- Recent behavior matters most
- Old mistakes decay naturally

### Streak Momentum (Secondary)
- Sustained consistency softens penalties
- Streaks NEVER override recent bad behavior
- Streaks act as shock absorbers, not erasers

---

## 10. Score Philosophy

The procrastination score is **feedback**, not judgment.

The score:
- Reflects trend and intensity
- Lives inside state-defined ranges
- Moves gently on minor events
- Moves strongly on serious violations
- Recovers faster with good history

The score is secondary to state.

> Users should notice state changes before score changes.

---

## 11. Score Semantics

- **Zero is attainable**
- **Zero is fragile**
- **Zero is recoverable**

A single slip removes zero, but:
- does not escalate state
- does not heavily punish score

Sustained consistency allows zero to be regained.

---

## 12. "Good Enough" Behavior

Argeia distinguishes between:

- **Noise**: Small human variance
- **Signal**: Repeated deviation

"Good enough" behavior:
- Does not break streaks
- Does not immediately affect score
- Leaves trace signals for pattern detection

Consistent "good enough" behavior can escalate into drifting.

---

## 13. Severity Hierarchy

From least severe to most severe:

1. Starting late
2. Stopping early
3. Never starting

Severity influences:
- Score movement magnitude
- Pattern escalation speed

---

## 14. Recovery Rules

Recovery:
- Is always possible
- Is faster with strong history
- Requires sustained improvement
- Never happens instantly

Recovery moves states **one step at a time**.

---

## 15. Design Guarantees

This system guarantees:

- No punishment for single accidents
- No hiding bad habits with one good task
- No permanent penalties
- Clear, explainable feedback

---

## 16. Intentional Omissions

This document intentionally avoids:
- Mathematical formulas
- Threshold values
- Implementation details

These are left flexible to allow iteration without breaking meaning.

---

## 17. Guiding Principle (Single Source of Truth)

> **Events do not change state. Pattern evidence is interpreted into proposals. Proposals change state.**

This rule governs the entire system.

---

## 18. Future Extensions (Non-Binding)

Potential future additions:
- Per-task state overlays
- Weekly behavioral summaries
- Visualization of recovery momentum
- Personalized thresholds

None of these alter the core design.

---

This document defines the current design intent and may evolve as Argeia grows.
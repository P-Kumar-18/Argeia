# Behavioral State Transition Specification
*(Argeia – Procrastination Model)*

## 1. Purpose of States

Behavioral states represent **long-term engagement quality**, not task success.

They answer the question:

> “How consistently is the user honoring self-imposed commitments over time?”

States are:
- Slow-changing
- Proposal-driven
- Explainable to the user
- More important than the numeric score
- Descriptive indicators, not moral judgments or performance scores.

A single task can never define a state.

---

## 2. Inputs to the State System

The state system **does not consume raw events**.

It only reacts to **proposals**, which are conclusions from confirmed patterns.

Patterns summarize:
- Repetition within a window
- Confirmed polarity (positive / negative)
- Strength (low / high)

Escalation, adjacency, and sustained evaluation are handled by the behavior evaluation layer before proposals are generated. This preserves layering.

If no proposal , the state must not change.

Signals may exist without forming a pattern; such signals are recorded but must not affect state.

---

## 3. Defined States

### 🟢 Stable
The user mostly follows their schedule.
- Deviations are rare or isolated
- Recovery from mistakes is quick
- No recent confirmed negative patterns

This is the baseline healthy state.

---

### 🟡 Drifting
Early warning state.
- Repeated “good enough” behavior
- Small deviations accumulating
- Commitments are mostly met, but consistency is weakening

Drifting is not failure — it is **signal without collapse**.

Drifting is primarily informational and intended as early awareness, not correction.

---

### 🟠 Strained
Clear commitment stress.
- Repeated lateness, early stopping, or missed tasks
- One or more confirmed negative patterns
- Momentum is broken

Strained indicates the system should intervene or reflect more strongly.

---

### 🔴 Disengaged
Loss of engagement.
- Tasks frequently missed or abandoned
- Schedule is largely ignored
- Strong, repeated patterns of avoidance

Disengaged is the worst state, but **never permanent**.

---

## 4. Degradation Rules (State Worsening)

### Core Rule
> **States only degrade due to a Proposal.**

A proposal means:
- Repetition beyond noise
- Observed within a rolling window
- Stronger than a single anomaly

### Standard Degradation
States degrade **one step at a time**:

```
Stable → Drifting → Strained → Disengaged
```

A Proposal can cause **one-step degradation** or **escalated degradation**.

Escalation rules are determined during behavior evaluation. The state engine only applies the severity level indicated in the proposal.

This keeps the state layer pure.

---

### Escalation Exception (Limited)

A state may degrade by two steps only if the proposal severity is marked as SEVERE.

The criteria for severity are defined in the behavior evaluation layer.

Rules:
- Stable → Strained is allowed
- Stable → Disengaged is never allowed

Escalation must always be explainable.

---

## 5. Recovery Rules (State Improvement)

### Core Rule
> **Recovery requires sustained improvement, not a single good task.**
> **Recovery proposals are generated only after sustained improvement is detected by the behavior evaluation layer.**
> **The state engine applies recovery one step at a time.**

Recovery occurs when a RECOVERY proposal is received.

The criteria for generating recovery proposals (including sustained improvement detection) are defined in the behavior evaluation layer.

### Recovery Path
Recovery always happens **one step at a time**:

```
Disengaged → Strained → Drifting → Stable
```

Instant recovery is not allowed.

Consistent positive history may **speed recovery**, but never skip steps.

---

## 6. Relationship Between State and Score

- State reflects **behavioral interpretation**
- Score reflects **trend intensity**

Rules:
- State changes should be noticeable before score extremes
- Score never overrides state
- Score cannot force a state change on its own

The score may react to individual events, even when state remains unchanged.

The score supports the state — it does not define it.

---

## 7. Design Guarantees

This model guarantees:
- No punishment for single mistakes
- No hiding bad habits behind isolated success
- No permanent negative states
- Clear reasoning for every transition
- Recovery is always achievable through consistent behavior

---

## 8. Governing Principle (Invariant)

> **Events create signals.**
> **Signals create patterns.**
> **Patterns are interpreted as proposals.**  
> **Proposals change state.**

Any implementation that violates this is incorrect.

---

## 9. Non-Goals

This system does not:
- Predict user intent or motivation
- Diagnose psychological conditions
- Enforce schedules or issue punishments
- Optimize for maximum productivity

Its sole purpose is reflective feedback on commitment consistency.
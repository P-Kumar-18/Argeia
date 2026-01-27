# Behavioral State Transition Specification
*(Argeia – Procrastination Model)*

## 1. Purpose of States

Behavioral states represent **long-term engagement quality**, not task success.

They answer the question:

> “How consistently is the user honoring self-imposed commitments over time?”

States are:
- Slow-changing
- Pattern-driven
- Explainable to the user
- More important than the numeric score
- Descriptive indicators, not moral judgments or performance scores.

A single task can never define a state.

---

## 2. Inputs to the State System

The state system **does not consume raw events**.

It only reacts to **detected patterns**, which are conclusions drawn from signals over time.

Patterns summarize:
- Repetition
- Severity
- Consistency
- Time window

If no pattern exists, the state must not change.

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
> **States only degrade due to confirmed negative patterns.**

A confirmed pattern means:
- Repetition beyond noise
- Observed within a rolling window
- Stronger than a single anomaly

### Standard Degradation
States degrade **one step at a time**:

```
Stable → Drifting → Strained → Disengaged
```

A single pattern can only cause **one-step degradation**.

Multiple patterns confirmed within the same evaluation window are treated as a single degradation decision unless escalation rules apply.

---

### Escalation Exception (Limited)

A state may degrade by **two steps** only if:
- Pattern severity is high (e.g. repeated missed tasks)
- Pattern spans multiple tasks or contexts
- Pattern emerges rapidly in a short window

Rules:
- Stable → Strained is allowed
- Stable → Disengaged is never allowed

Escalation must always be explainable.

---

## 5. Recovery Rules (State Improvement)

### Core Rule
> **Recovery requires sustained improvement, not a single good task.**
> **Recovery uses the same evidence standards as degradation: repetition, consistency, and time.**

Recovery happens when:
- No recent confirmed negative patterns exist
- Positive or neutral behavior persists
- Improvement is sustained over time

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

> **Events create signals.  
Signals create patterns.  
Patterns change state.**

Any implementation that violates this is incorrect.

---

## 9. Non-Goals

This system does not:
- Predict user intent or motivation
- Diagnose psychological conditions
- Enforce schedules or issue punishments
- Optimize for maximum productivity

Its sole purpose is reflective feedback on commitment consistency.

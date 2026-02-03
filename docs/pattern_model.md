# Behavioral State Transition Specification
*(Argeia – Patterns Model)*

## Purpose of Patterns

Patterns determine whether signals represent noise or habit formation.

A window represents a bounded sequence of recent tasks used to evaluate behavioral consistency.

---

## Signal Strength

Signal strength describes how large a deviation is **relative to the task**.

There are three types of signal strength:

- **Weak Signal** — Small relative deviation
- **Moderate Signal** — Moderate relative deviation
- **Strong Signal** — Large relative deviation

---

## Patterns

### Pattern Polarity

Pattern polarity describes the directional tendency of a detected pattern.

There are two types of pattern polarity:

- **Negative Pattern** — Indicates behavioral degradation pressure
- **Positive Pattern** — Indicates behavioral improvement pressure

Sustained patterns are defined separately and govern recovery behavior.

---

### Pattern Confirmation

Pattern confirmation determines whether observed signals represent a real behavioral tendency or temporary noise.

A pattern is considered **unconfirmed** when:
- signals are isolated
- signals are sparse within a window

A pattern becomes **confirmed** when:
- similar signals recur consistently within a window
- or when unconfirmed patterns appear in adjacent windows

---

### Pattern Strength

Pattern strength represents the intensity of a confirmed behavioral pattern.

Strength does not determine whether a pattern exists.
It determines how impactful the pattern is once confirmed.

Pattern strength is influenced by:
- the magnitude of individual signals (strong vs weak deviations)
- the density of signals within a window
- the presence of extreme signals (e.g. full timeout)

Pattern strength is evaluated only after pattern confirmation.

---

### Pattern Severity

Pattern severity describes how strongly the system should *respond* to a detected pattern.

Severity is a **policy-level interpretation** derived from the pattern, not an inherent property of the pattern itself.

While pattern strength describes *how intense the behavior is*, severity describes *how impactful that behavior should be considered* by the system.

Severity is influenced by:
- the **strength** of the detected pattern
- the **type** of pattern (negative vs positive)
- the **presence of extreme signals** (e.g. full task timeouts)
- the **current behavioral state** of the user

Severity does **not** determine whether a pattern exists.
It determines **how strongly the system reacts once a pattern is confirmed**.

For negative patterns:
- low severity may result in standard degradation
- high severity may result in accelerated or severe degradation

For positive patterns:
- severity influences recovery eligibility
- recovery remains intentionally slower and requires sustained patterns

Severity decisions are enforced exclusively by the state transition logic, not by the pattern detection layer.

---

## Sustained Patterns

A sustained positive pattern represents consistent improvement maintained across multiple windows.

Sustainment requires:
- confirmed positive patterns
- continuity across adjacent windows
- absence of confirmed negative patterns during the sustainment period

A single negative window breaks sustainment.

---

## Positive Patterns

Positive patterns represent behavioral improvement.

Unlike negative patterns:
- positive patterns do not immediately cause state changes
- recovery requires sustained positive patterns across multiple windows

This asymmetry prevents over-rewarding short-term improvement.

---
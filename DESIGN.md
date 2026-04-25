# Argeia – System Design Document

This document captures the **finalized design decisions** for Argeia — a behavior-aware task scheduling and procrastination tracking system. It covers architectural choices, infrastructure design, behavioral modeling philosophy, and web layer decisions. It intentionally separates **design intent** from **implementation details**, so the logic can evolve without losing meaning.

---

## 1. Core Philosophy

Argeia does not treat procrastination as a single mistake or a moral failure. Instead, procrastination is defined as a pattern of breaking self-imposed commitments over time. This distinction shapes every design decision in the system. A single late start is noise. A week of late starts is a signal. A month of late starts is a behavioral pattern that warrants intervention.

The system is designed to be fair to one-off accidents, honest about emerging bad habits, forgiving when improvement is sustained, and clear and explainable to the user at every stage. These four properties are not aspirational — they are enforced at the design level through the proposal-driven state engine, the asymmetric recovery model, and the layered signal-to-pattern pipeline.

---

## 2. Design Scope and Sources of Truth

This document defines Argeia's high-level philosophy, architectural guarantees, and system structure. The authoritative specification for behavioral states and state transition rules is defined separately in `docs/behavior_model.md`. This separation is intentional: `DESIGN.md` explains why the system behaves the way it does, while `behavior_model.md` defines how behavior is interpreted over time. Any implementation must follow the rules defined in `docs/behavior_model.md`.

---

## 3. Package Architecture

Argeia's codebase is organized into four clearly separated packages inside `app/`: `core/`, `domain/`, `runner/`, and `web/`. This separation was a deliberate architectural decision made early in development and maintained throughout.

The `domain/` package contains the pure business logic — the `Task`, `Signal`, and `Window` models. These classes have no knowledge of databases, Flask, or any infrastructure concern. They can be instantiated and tested in complete isolation, which is why the test suite can run without a database or a running Flask server.

The `core/` package contains the analytical layers — `pattern_detection.py`, `behavior_evaluator.py`, and `state_engine.py`. These modules operate on domain objects and produce structured outputs. They are also infrastructure-free and fully testable in isolation.

The `runner/` package contains the application layer — `TaskRunner`, `BehaviorRunner`, and `WindowManager`. These classes coordinate between the domain, core, and infrastructure layers. They own the pipeline: a task flows from `TaskRunner` into `BehaviorRunner`, which delegates to `WindowManager`, which produces patterns and proposals that eventually reach the state engine. The runners are the only layer allowed to touch both domain objects and repositories simultaneously.

The `infrastructure/` package contains all persistence logic — the database connection, schema initialization, and three repositories (`TaskRepository`, `WindowRepository`, `TransitionRepository`). Repositories speak SQLite; the rest of the system speaks domain objects. This boundary is strict and enforced throughout the codebase.

The `web/` package contains everything Flask-related — routes, templates, and static assets. It is the outermost layer and only interacts with the system through the runners and repositories attached to the Flask app context.

---

## 4. Behavioral Pipeline

Argeia models behavior using a layered pipeline:

```
Tasks → Signals → Windows → Pattern Batching → Patterns → Behavior Evaluation → State Engine → Transition Events → Persistence → State Reconstruction
```

Each layer has a single responsibility. This was a foundational design decision: no layer skips another, and no layer inspects the internals of another. The state engine does not inspect patterns directly — it only consumes proposals produced by the behavior evaluation layer. This keeps each layer independently testable and decoupled from the others.

When a user completes a task, `TaskRunner` records it and passes it to `BehaviorRunner`, which passes it to `WindowManager`. `WindowManager` converts the task into signals, accumulates them within the current weekly window, and periodically evaluates them into patterns. When the window closes, patterns are passed to `BehaviorRunner`, which invokes the behavior evaluation layer to produce a proposal. That proposal is passed to the state engine, which decides whether to transition state. If a transition occurs, a structured `Transition` event is emitted and persisted.

---

## 5. Signals

Signals convert task execution events into measurable deviations from planned behavior. There are three signal types: start delay, underwork, and timeout.

Start delay measures how many minutes late a task was started relative to its scheduled start time. Underwork measures how many minutes short of the planned duration the user worked. Timeout fires when a task was never started at all — but only after the scheduled end time has passed. This guard was an important design fix: a task that hasn't been started yet at 2pm but is scheduled for 3pm should not be flagged as a timeout. Timeout values are clamped to a minimum of zero to prevent negative signal values from corrupting the analytical layer.

Signals are objective, time-based, and non-judgmental. They do not encode severity or moral weight. A signal is simply a measurement. All interpretation happens at the pattern and behavior evaluation layers.

---

## 6. Windows

Signals are accumulated within weekly time windows. A window opens at the start of a week and closes when the weekly time boundary is reached. Windows serve two purposes: they bound signal accumulation so that old behavior naturally decays, and they provide a unit of analysis for the pattern detection layer.

Windows are persisted to the database. On startup, `WindowManager` queries the database for the latest open window and restores it, including all its signals and patterns. If no open window exists, a new one is created. This restart recovery behavior is essential for a personal productivity tool — the system must be able to pick up where it left off without losing behavioral context.

Within each window, pattern detection runs in batches every five tasks. This intra-window batching was a deliberate design choice: running pattern detection on every task would be noisy, but waiting until the window closes would delay feedback too long. Batching every five tasks strikes a balance between responsiveness and stability.

---

## 7. Pattern Detection

Patterns interpret accumulated signals to identify consistent behavioral trends. A pattern has two properties: polarity (positive or negative) and strength (low or high). Polarity reflects whether the behavior is improving or degrading. Strength reflects how pronounced the trend is.

Patterns do not change state directly. They provide evidence that is passed to the behavior evaluation layer. This indirection is intentional — it prevents a single bad batch from immediately triggering a state change, and it allows the evaluation layer to apply additional logic such as conflict resolution and escalation before producing a proposal.

---

## 8. Behavior Evaluation

The behavior evaluation layer interprets pattern evidence across windows and produces a structured proposal. Proposals are one of four kinds: degradation (normal), degradation (severe), recovery, or no proposal. The behavior evaluation layer is responsible for escalation logic, adjacent window evaluation, sustained positive detection, and conflict resolution.

Conflict resolution is a key design concern: it is possible for a window to contain both positive and negative patterns. The evaluation layer resolves this by giving degradation evidence priority over recovery evidence. This is asymmetric by design — the system is more willing to flag a problem than to declare recovery.

---

## 9. State Engine

The state engine maintains four behavioral states: Stable, Drifting, Strained, and Disengaged. States are slow-changing and proposal-driven. A single task never changes state. Only confirmed proposals from the behavior evaluation layer can trigger a transition.

Degradation proposals move state one step at a time unless marked severe. Severe degradation can skip a state. Recovery proposals always move state one step at a time — there is no fast recovery path. This asymmetry is intentional: the system is designed to be conservative about declaring recovery because premature positive feedback can mask real problems.

When a transition occurs, a structured `Transition` event is emitted capturing the previous state, the new state, the proposal kind and severity, a structured evidence summary, and a timestamp. These events are persisted to the database and are visible to the user on the analysis page. They form a complete behavioral history and enable full explainability of every state change.

---

## 10. Database Design

Argeia uses SQLite for persistence. The schema consists of six tables: `tasks`, `behavior_windows`, `window_signals`, `window_patterns`, `transitions`, and `transition_reasons`.

The decision to separate `transitions` and `transition_reasons` into two tables was made to avoid storing structured data as a serialized blob. The evidence reason for a state transition is a structured object with four fields: high pattern count, low pattern count, window scope, and sustained trigger. Storing this as a JSON string in the transitions table would have worked but would have made querying and analyzing evidence difficult in future versions. A foreign key relationship between `transitions` and `transition_reasons` keeps the data properly normalized.

The schema is initialized automatically on startup via the `Database` class. When a `Database` object is instantiated with a path, it creates the database file and directory if they don't exist, then runs all `CREATE TABLE IF NOT EXISTS` statements. This means the app can be run on a fresh machine without any manual setup step.

SQLite cross-thread mode (`check_same_thread=False`) is enabled because Flask serves requests in separate threads but the database connection is created once at app startup. For a single-user personal tool, this is the appropriate solution — per-request connections would add unnecessary complexity without meaningful benefit.

---

## 11. Repository Pattern

Each persistence concern has its own repository class: `TaskRepository`, `WindowRepository`, and `TransitionRepository`. Repositories are the only classes in the system that speak SQLite. They accept and return domain objects, never raw rows.

This boundary was maintained strictly throughout development. Routes do not write SQL. Runners do not know about SQLite. The repository pattern makes it possible to swap the persistence layer in future versions — for example, replacing SQLite with PostgreSQL for a multi-user v2 — without touching the domain or runner layers.

Each repository creates its own `Database` instance using a shared default path derived from the project root. This path is computed using `os.path` relative to the `database.py` file itself, which ensures the correct path is found regardless of which directory the app is launched from.

---

## 12. Flask Web Layer

The web layer was added after the behavioral core was complete and fully tested. This sequencing was intentional: the core system needed to be correct before it was exposed to users. Flask was chosen for the web framework because Argeia is a personal tool with no need for a complex SPA frontend. Server-rendered Jinja2 templates are simpler to build, simpler to maintain, and eliminate the need for a separate API layer and frontend build system.

The Flask app is constructed in `app/__init__.py` via a `create_app()` factory function. This pattern makes it possible to create multiple app instances with different configurations, which is essential for testing. At startup, `create_app()` initializes the database, wires all repositories and runners, attaches the top-level objects to the app context, and registers the blueprint.

Routes are organized inside `web/routes/` as a single blueprint with one file per page. The blueprint pattern allows routes to be grouped logically without requiring multiple blueprint registrations. Each route file imports the blueprint from `web/routes/__init__.py` and adds its routes to it.

The dashboard is the most behaviorally critical page because it is where users start and complete tasks. Start and end actions are handled via JavaScript `fetch` calls to a POST endpoint on the dashboard route, returning JSON responses. This avoids full page reloads for time-sensitive interactions. CSRF protection is applied to all forms and fetch calls via Flask-WTF, with the CSRF token passed in the `X-CSRFToken` header for JSON requests.

Only one task is presented as active at a time in the dashboard UI by selecting the next upcoming incomplete task. The start button is disabled client-side if the task has already been started or if the current time is before the scheduled start. The end button is disabled if the task has not been started. Server-side checks enforce task existence and lifecycle validity (for example, cannot start a completed task and cannot end a task that was never started).

---

## 13. Design Guarantees

This system guarantees the following properties regardless of implementation changes:

No punishment for single accidents — a single late start, early stop, or missed task will never trigger a state change on its own. State changes require confirmed patterns across multiple tasks and, in the case of recovery, across multiple windows.

No hiding bad habits with one good task — a single good task cannot produce a recovery proposal. Recovery requires sustained positive patterns across multiple windows.

No permanent penalties — every state can be recovered from given sufficient sustained improvement.

Clear, explainable feedback — every state transition is backed by a structured evidence record that is stored in the database and visible to the user on the analysis page.

---

## 14. Intentional Omissions in v1

Several features described in early design iterations were intentionally deferred to future versions. A score system was planned but not implemented in v1 — the state model provides sufficient feedback for a first version, and a score would require careful calibration to avoid misleading users. Per-user support was deferred but the schema includes a nullable `user_id` column in the tasks table to make the migration to multi-user support easier in v2. Weekly behavioral summaries and visualization of recovery momentum were also deferred.

---

## 15. Guiding Principle

> **Events do not change state. Pattern evidence is interpreted into proposals. Proposals change state.**

This rule governs the entire system and was the single most important design decision made during development. It ensures that Argeia is fair, explainable, and resistant to gaming — a user cannot manipulate their state by performing a single action at the right moment.

---

This document defines the current design intent for Argeia v1 and will evolve as the system grows in future versions.
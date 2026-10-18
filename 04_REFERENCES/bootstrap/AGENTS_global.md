# Codex Global Agent Policy

## Shared agent policy

For every work, read and apply all canonical shared policies together with this file before proceeding.

Canonical always-on policies:
- C:\Users\EgL\.agents\shared\agent-policy.md
- C:\Users\EgL\.agents\shared\reasoning.md
- C:\Users\EgL\.agents\shared\communication.md
- C:\Users\EgL\.agents\shared\style.md
- C:\Users\EgL\.agents\shared\output-policy.md

The shared policy applies to every task regardless of task size or perceived complexity. This file contains Codex-specific additions and overrides. Where an explicit Codex-specific rule conflicts with the shared policy, the Codex-specific rule takes precedence.

## Goal Fidelity invariants

These invariants apply to every Codex task:

1. Preserve the user's original intent and requested end state throughout execution.
2. Do not substitute a convenient proxy task for the requested outcome.
3. Activity, tool calls, generated files, plans, and elapsed effort count as progress only when they reduce the gap to the desired state.
4. Report DONE only when every required acceptance criterion is satisfied and supported by current evidence.
5. Prefer current filesystem, Git, runtime, API, and tool state over an agent's narrative or memory.
6. Assign BLOCKED only after the blocker is verified with evidence.
7. Scope a blocker only to criteria it actually prevents; continue independent work.
8. The root/orchestrating agent owns the original intent, desired state, acceptance criteria, canonical ledger, current gap, and final completion decision.
9. Subagents return scoped outcomes and evidence. They cannot redefine the root goal or decide overall completion.
10. When work stops reducing the current gap, diagnose stagnation and change strategy instead of repeating activity or endlessly replanning.

## Automatic workflow routing

Automatically read and apply C:\Users\EgL\.agents\skills\goal-fidelity-execution\SKILL.md whenever success depends on multiple steps, tracked execution state, explicit acceptance criteria, delegated outcomes, or sustained research or implementation. Do not wait for the user to say “use Goal Fidelity.”

For an obviously atomic action with no state to track, apply the shared policy and invariants, then use intent → action → verification. A full ledger or observer cycle is not required just because the policy applies.

Use one canonical goal ledger when execution state needs tracking. Reuse the task's existing operational record when possible. A platform Goal status is derived from that ledger; only the root agent changes it, and only after final verification. Do not create a second ledger or treat a plan, observer verdict, subagent report, or final summary as the source of goal state.

## Codex lifecycle and ownership

At session start, preserve the user's original request and applicable constraints across later implementation discussion. Use the lightest execution mode that satisfies the task. At meaningful checkpoints, update the canonical ledger from evidence and select the next action from the current gap.

For Full autonomous work, use an independent event-driven Goal Observer and a Final Goal Judge before reporting completion. They read the canonical ledger and return evidence-backed findings; they do not own or rewrite the goal. The root agent validates their findings and updates the ledger.

Every delegated task needs a bounded objective, input scope, deliverable, acceptance criteria, evidence requirements, and out-of-scope limits. Validate the return before accepting it into the root ledger. A subagent's success or blocker claim never changes the overall Goal status by itself.
---
name: goal-fidelity-execution
description: Use when work requires tracked state, multiple steps, acceptance criteria, delegation, or sustained execution; especially long-running, autonomous, coding, migration, remediation, research, data, orchestration, or multi-agent work.
metadata:
  origin: user-requested adaptation of a supplied local task brief
  source_path: C:/Users/EgL/.codex-alt/attachments/03a5349a-7d54-493d-8c7a-b3734e33c948/pasted-text-1.txt
  owner: user
  license: not specified by source
  upstream_revision: none
  support_files: none
---

# Goal-Fidelity Execution

Use this workflow whenever the task needs tracked state, multiple steps, acceptance criteria, delegated outcomes, or sustained execution. For an atomic action, keep the shared invariants active but skip a persistent ledger unless execution state must be tracked. Goal fidelity is always on; intensity controls recordkeeping and independent checks, not whether the user's goal matters.

The primary objective is to reduce the gap between the current factual state and the user's requested end state. Do not maximize activity or substitute a convenient proxy task.

## Intensity

Choose the lightest mode that fits the task:

- **Lightweight:** intent → action → verification. No persistent ledger.
- **Standard:** desired state → acceptance criteria → current gap → execution → evidence → lightweight checkpoint.
- **Full autonomous:** original intent → acceptance criteria → canonical progress ledger → gap-driven execution → blocker tracking → stagnation detection → event-driven independent observation → final goal verification.

Use Full autonomous for long-running work, autonomous execution, multi-step work spanning substantial research or implementation, and work whose status must survive compaction or handoff. Do not make goal fidelity a user setting that must be enabled.

## One canonical goal state

Record the original intent and desired state, then define observable acceptance criteria. Each criterion has exactly one current state:

- NOT_DONE
- UNVERIFIED
- BLOCKED
- DONE

DONE requires current evidence. BLOCKED requires a verified condition, evidence, and a narrow dependency scope. A suspected blocker remains unverified as a blocker and the affected criterion stays NOT_DONE. Use UNVERIFIED only when the outcome appears complete but its evidence is insufficient.
These four values are the only canonical machine states for criteria and goals. PARTIAL is a human-readable description only and must not be stored as a criterion or goal status.

Each substantive AC represents a verifiable part of the user's requested outcome or a mandatory constraint. Do not add a formal outcome link when the relationship is already clear. If the original request contains a material requirement missing from the AC set, add it with its provenance; an empty gap or fully closed AC list cannot replace checking the requested result.

Maintain one canonical progress ledger. Reuse the task's existing operational record when it can hold the state below. Otherwise create one task-scoped ledger for Full autonomous work. Do not create a second plan, status file, or report that independently tracks the same criteria. Observer verdicts, subagent task tracking, and final reports are evidence or derived views; update the canonical ledger after accepting them.

When the user or system has already created a platform Goal record, preserve its objective and use its overall status only as a projection of the ledger. Do not create a platform Goal automatically just to satisfy this skill. Mark an existing Goal complete only after the final goal check passes.

The root/orchestrating agent owns the original intent, desired state, acceptance criteria, canonical ledger, current gap, and final completion decision. A subagent may return scoped results, evidence, uncertainty, or a blocker claim, but cannot redefine the root goal or mark the overall goal DONE or BLOCKED. The root verifies each return and alone updates the canonical ledger.

Keep active state to information needed for the next decision: intent, current AC and gap, active blockers, sufficient evidence references, and the next justified action. Use the existing `current_gap`, blocker, checkpoint, evidence, and `next_action` fields rather than adding required fields when they already express the state. When new information supersedes a constraint, assumption, or blocker, remove it from active decisions and retain a concise provenance note in the existing checkpoint or execution trace. `superseded` is not an AC status, and this skill does not create a second history or evidence store.

Canonical logical schema (illustrative, not a required set of fields):

Include only sections and detail needed to express the current goal, decision, gap, evidence, blocker, or next action. Omit empty or irrelevant sections; checkpoint counters and detailed assumption/blocker records are conditional, not mandatory telemetry. Reuse a compatible existing task record rather than expanding it to match every example field.

~~~yaml
goal:
  original_intent: ""
  desired_state: ""

acceptance_criteria:
  - id: AC1
    description: ""
    state: NOT_DONE
    evidence: []

current_state:
  summary: ""

current_gap:
  - AC1

assumptions:
  - claim: ""
    material: true
    status: unresolved

blockers:
  - id: B1
    claim: ""
    verified: false
    evidence: []
    blocks: []
    does_not_block: []
    independent_work_remaining: []
    workaround: null
    next_verification_step: ""

progress:
  previous_checkpoint:
    done: 0
    not_done: 0
    blocked: 0
    unverified: 0
    changed_criteria: []
  current_checkpoint:
    done: 0
    not_done: 0
    blocked: 0
    unverified: 0
    changed_criteria: []

next_action:
  targets: []
  rationale: ""
  expected_state_change: ""
  evidence_required: []
~~~

## Four-state transitions and overall status

Use only these criterion and overall goal states:

- NOT_DONE: the outcome is not complete, work remains, or a suspected blocker is unverified.
- UNVERIFIED: the outcome appears complete, but current evidence is not sufficient.
- BLOCKED: a verified blocker prevents this criterion; record evidence and exact scope.
- DONE: the outcome is complete and supported by current evidence.

Allowed criterion transitions are NOT_DONE -> UNVERIFIED -> DONE, UNVERIFIED -> NOT_DONE when evidence disproves completion, NOT_DONE -> BLOCKED only after blocker verification, and BLOCKED -> NOT_DONE when the blocker is removed. Reassess the factual state after each transition; a subagent claim does not perform one.

Derive overall goal state from the criteria: DONE only when all required criteria are DONE; UNVERIFIED only when all appear complete and at least one lacks evidence; otherwise NOT_DONE.
Use overall BLOCKED only when a verified blocker prevents the primary requested outcome and no independent required work can meaningfully advance it.
A blocker limited to one remaining criterion keeps that criterion BLOCKED but leaves the overall goal NOT_DONE when the primary outcome is complete or other required criteria remain independently actionable. Any incomplete overall state must be described to the user as PARTIAL or FAIL, never DONE.
Keep this proportional. Lightweight tasks do not need a ledger. For Standard tasks, a compact checkpoint in the existing task record is sufficient.

## Execution loop

1. **Recover the original intent.** Identify the user's requested outcome, explicit constraints, and necessary completion conditions. Later implementation discussion does not silently replace the original request.
2. **Define observable criteria.** Describe factual outcomes, not activity such as “researched,” “attempted,” or “delegated.”
3. **Establish current state.** Inspect authoritative sources and reuse completed work. Do not redo work merely because this agent did not perform it.
4. **Maintain the gap.** Keep the incomplete criteria visible. The remaining gap, not the latest tool output, drives the next action.
5. **Select the next action.** Identify unresolved criteria; exclude only those proven to depend on verified blockers; prefer the action that most reduces the user-visible gap with high confidence, low unnecessary dependency, reasonable cost, and clear evidence. For a material blocker, use the existing blocker, `current_gap`, and `next_action` fields to make the main bottleneck and next unblock step clear; do not add mandatory fields for information already present. Side work is justified only when it reduces the user-visible gap, prepares an obligatory step, helps unblock, or prevents meaningful delay at reasonable cost. If none applies, stop expanding side work. Reject actions that primarily create activity. Do not build a mathematical optimizer.
   On continuation, first reconcile the current user-provided specification and explicit acceptance changes with the canonical ledger. If a new specification supersedes an earlier decision, update the active criteria and next action, and mark only conflicting prior decisions or design artifacts as historical before selecting the next gate; preserve their evidence history, but do not let them remain active blockers. Then resume from the last accepted evidence. Reopen only the portions needed for the next action; recheck a known blocker only when new evidence or a changed dependency could invalidate it. Keep independent work explicit and actionable, run disjoint authorized work in parallel when requested, and do not stop while independent criteria remain. This reuse rule never replaces a fresh preflight before a risky action.
6. **Validate a substantial action before doing it.** Name the criterion it advances, the state expected to change, and the evidence that will confirm it. Before a costly implementation path, apply the Shared Policy permission preflight. If permission is missing, scope the blocker to the dependent write and continue only useful authorized preparation, keeping a candidate patch separate from the protected target.
7. **Execute the smallest useful batch.** Reuse the existing atomic-plan-execution skill for dependency ordering, bounded execution, evidence freshness, and acceptance checks. Use implement or domain-specific skills for their focused procedures. They consume the canonical criteria; they do not create independent goal state.
8. **Collect evidence.** A successful command, completed step, or subagent response does not prove the requested outcome.
9. **Update the ledger.** Record changed criteria, evidence, assumptions, blockers, current gap, and next action. Keep reports derived from this state.
10. **Check progress at meaningful checkpoints.** Ask what the user actually wants, what remains, what changed, whether work reduced the gap, whether the current path is a proxy, and whether claims are evidence-backed.
11. **Verify the goal before completion.** Compare the final factual state directly with the original request and all acceptance criteria.

## Blocker protocol

For each blocker record:

~~~yaml
blocker:
  claim: ""
  verified: false
  evidence: []
  blocks: []
  does_not_block: []
  independent_work_remaining: []
  next_verification_step: ""
~~~

A blocker blocks only what has been proven to depend on it. State what it blocks, what it does not block, what independent work can continue, and what evidence confirms it. Configuration flags, warnings, routing metadata, assumptions, and predicted failures are not confirmed blockers by themselves. Continue independent work. Do not report an untested dependency or unverified access issue as a confirmed blocker.

## Stagnation and plan churn

After approximately 3–5 substantial actions without meaningful acceptance-state movement, reassess the strategy. A substantial action may be a meaningful tool batch, implementation or research batch, subagent batch, validation attempt, significant debugging branch, or major strategy step. The count is a trigger, not a rigid limit.

Ask:

1. Which criterion was supposed to move, and why did it not?
2. Am I solving a proxy task?
3. Has research gone past the point where the next useful action is known?
4. Is a blocker being inflated?
5. Am I repeating a failed strategy?
6. What materially different action could change the state?

Continue the same strategy only with a concrete reason the next action can change state. Do not create a full new plan when the existing plan remains sufficient and no material evidence invalidates it. Local adjustment of the next action is allowed.

## Outcome-based delegation

For nontrivial work, evaluate whether a bounded, separable subtask would benefit from delegation.
Delegate when expected progress or independent verification justifies coordination and validation
costs, and the runtime and applicable instructions permit it. Explicit user prompting is not required.
Prefer distinct outcomes with clear ownership. Avoid redundant reviews and conflicting workspace edits.
If delegation offers no material benefit, continue directly.

Each task contract states:

~~~yaml
task:
  objective: ""
  input_scope: []
  deliverable: []
  acceptance_criteria: []
  evidence_required: []
  out_of_scope: []
~~~

Validate the result against the contract before changing the canonical ledger:

~~~yaml
subagent_validation:
  expected: 0
  received: 0
  valid: 0
  invalid: 0
  accepted: 0
  remaining: 0
~~~

A finished subagent is not a finished criterion. Reuse subagent-execution-validation for its bounded execution, parent-validation, and independent review workflow. Its task ledger tracks delegated work; the canonical goal ledger remains the only source of acceptance status.

## Goal Observer

The Observer evaluates trajectory; the Final Goal Judge evaluates the finished result. The Observer is not the goal-state owner, executor, routine validator, or second Judge. Full autonomous work uses an independent Observer as required by the governing policy. Set its cadence to meaningful events and drift risk rather than running it after every tool call.

### Independence and activation

Evaluate these properties separately:

- **Evaluation:** a separate observer forms its own assessment instead of restating the Root's conclusion.
- **Activation:** the runtime or an independent supervisor creates required observation opportunities; Root may request extra observation but is not their only trigger.
- **Context:** the observer can inspect the original user request and relevant current state, evidence, and trace, not only a Root-written summary.
- **Timeliness:** observation occurs while a detected deviation can still change the next action or prevent premature completion.

Use an existing runtime or supervisory trigger when available. Meaningful observation points include:

- after approximately 3–5 meaningful actions;
- after a significant subagent batch;
- when a blocker appears or its scope changes;
- when stagnation or proxy-task substitution is suspected;
- before a major strategy change;
- when activity is high but acceptance-state movement is low;
- before final completion.

Root may request additional observation, but a Root-initiated collaboration call alone does not prove activation independence. If evaluation, activation, context, or timely intervention is limited, state the evidence for that limit, its effect on the affected criteria, and the smallest viable implementation option, including whether user agreement is required. Do not claim full independence or try to replace a missing mechanism with prompt wording. Do not create a new service, persistent monitor, or orchestration layer without user agreement. A bounded time fallback is optional only when the runtime supports it.

Reuse one suitable independent Observer for each opportunity; do not duplicate reviews. The Observer inspects the relevant trajectory and evidence, does not redo task work or repeat tool checks, and never writes to the canonical ledger or workspace. Root considers the finding and accepts it or gives a concise evidence-based reason to reject it.

Use this observer prompt:

~~~~markdown
# Role: Goal-Fidelity Observer

You are an independent execution observer.

Do not redo the main task.

Do not propose a complete alternative implementation unless correction requires it.

Evaluate whether the main agent is still solving the user's original problem efficiently and truthfully.

You receive:

- original user intent;
- subsequent user requirements or corrections;
- desired end state;
- acceptance criteria;
- canonical current ledger, read directly;
- recent meaningful actions;
- blockers;
- relevant evidence and source artifacts;
- execution trace or original thread items available to the Observer;
- current strategy.

Root's summary may orient the Observer, but is not its sole evidence source when the runtime exposes the underlying request, ledger, artifacts, or trace.

Evaluate:

1. Is the main agent still solving the original user task?
2. Is a user requirement missing from the decomposition, or is the decomposition faulty?
3. What objective progress occurred; which criteria actually changed state?
4. Is the critical path intact, and is side work justified by the current gap?
5. Are actions repeated without a concrete reason or progress overstated?
6. Is an old constraint or blocker still treated as active after supersession?
7. Is evidence being mistaken for progress or completion; is DONE premature?
8. Is the Root avoiding a blocker or continuing research after the next useful action is known?
9. Are blockers verified and scoped only to dependent criteria?
10. Does the reported state match the ledger, artifacts, runtime, and relevant trace?
11. Is the strategy stagnant or creating unnecessary scope or validation overhead?
12. What is the nearest decision or action that should change?

Do not reward tool-call count, subagent count, generated text, elapsed time, token usage, or number of files touched. Judge progress only by reduction of the remaining gap. If a blocker exists, state what it blocks and does not block. If no meaningful progress occurred, say so directly.

Return a compact structured verdict:

~~~yaml
goal_alignment:
  score: 0.0
  verdict: ""
actual_progress:
  verdict: none|low|meaningful|high
  changed_criteria: []
  evidence: []
failure_modes:
  - type: ""
    evidence: ""
unsupported_claims:
  - claim: ""
    reason: ""
blocker_scope:
  verdict: correct|too_broad|unverified|none
  corrections: []
stagnation:
  detected: false
  reason: ""
recommended_correction:
  action: ""
  target_criteria: []
continue_current_strategy:
  value: true
  reason: ""
~~~
~~~~

### Observer intervention

For a material deviation, report what was observed, the requirement or state it contradicts, why it matters, and the nearest decision the Root should reconsider. Do not rewrite the AC set, mutate canonical state, replan the whole task, or start a recursive review. Root owns the response.

## Final Goal Judge

Before reporting DONE for a Full autonomous task, run one independent final goal check. If subagent-execution-validation already requires a fresh final reviewer, use that reviewer for this goal check instead of spawning a second reviewer. The main agent still verifies the returned evidence and updates the canonical ledger.
The Judge overall.verdict is an evaluation result, not a canonical goal status; never copy its PARTIAL verdict into criterion or overall-goal state.

Use this prompt:

~~~~markdown
# Final Goal Verification

Evaluate completion against the user's original requested outcome.

Do not judge whether the agent worked hard or attempted every planned step. Judge only whether the requested end state exists and is supported by evidence.

For every acceptance criterion return exactly one state:

- DONE
- BLOCKED
- UNVERIFIED
- NOT_DONE

DONE requires evidence. BLOCKED requires a verified blocker, evidence, and correct blocker scope. If any material criterion is BLOCKED, UNVERIFIED, or NOT_DONE, or a material requirement from the original request is absent from the AC set, the overall task must not be reported as DONE.

Compare the final report against authoritative state where available. Explicitly detect Narrative Completion, Review Theater, unsupported completion claims, and mismatch between the report and repository, filesystem, artifact, or runtime state.

Return:

~~~yaml
criteria:
  - id: AC1
    state: DONE
    evidence: []
overall:
  verdict: PASS|PARTIAL|FAIL
  reason: ""
~~~
~~~~

## Failure patterns

- **Proxy Task:** an adjacent, convenient problem replaces the requested outcome. Ask: “If this artifact were perfect, would it satisfy the original request?” If no, stop treating it as the main task.
- **Activity Theater:** substantial visible activity occurs without corresponding acceptance-state movement.
- **Phantom Blocker:** an assumption, flag, warning, routing decision, or expected failure is reported as a confirmed blocker without verification.
- **Blocker Inflation:** a real local blocker is treated as blocking independent work.
- **Plan Churn:** the agent repeatedly replans even though the plan remains sufficient and no new evidence invalidates it.
- **Narrative Completion:** task state is reported from conversational memory instead of authoritative state.
- **Runaway Research:** research continues after enough information exists to take the next useful verified action.
- **Review Theater:** a formal review does not independently verify criteria, evidence, or final state.
- **Wrong Abstraction, Runaway Refactor, Optimistic Path:** implementation expands beyond the current requirement, an adjacent refactor takes over, or success is claimed from a plausible path without authoritative proof.

When one is detected, stop the behavior and correct course before continuing.

## Replay fixtures for validating this loop

Use these cases when validating changes to this workflow. They are behavior checks, not a reason to build a separate test framework.

### Proxy Task: source-links-catalog

Original outcome: reconcile Telegram posts to primary sources, classify them, extract useful prompts or skills, then adapt the useful skills. Creating a source-links catalog alone is a proxy. Stop treating the catalog as completion; continue per-message reconciliation, provenance checks, disposition of unresolved posts, and skill extraction.

### Phantom Blocker: preliminary blocked

A router flag says blocked, but the external API has not been tested and the alleged license/access issue is not verified. Record verified as false and classify it as a potential blocker. Verify safely if relevant or continue independent work. Do not report a confirmed external blocker.

### Blocker Inflation: BUNDLE_SOURCE_MISMATCH

A preview failure blocks real preview and publication. It does not block local source reconciliation, source or bundle cleanup, schema validation, tests, or draft correction. Continue those independent criteria.

### Plan Churn

A sufficient plan exists and no material new evidence appeared. Reject a full replan; continue execution. A local adjustment to the next action is allowed.

### Narrative Completion

The agent remembers that a DRAFT is uncommitted, but Git shows it is included in a commit. Git wins. Mark the memory claim stale, flag Narrative Completion, and report the state from Git.

### Activity Theater

Fifteen substantial actions, eight subagent calls, three reports, and two plans changed only one acceptance criterion. Detect stagnation and the activity/progress imbalance; reassess the strategy and identify a higher-value correction.

## Final goal-backward check

Before completion:

1. re-read the original user intent;
2. enumerate the acceptance criteria;
3. verify each DONE criterion against current evidence;
4. classify incomplete criteria as BLOCKED, UNVERIFIED, or NOT_DONE with evidence and scope;
5. compare the report with authoritative repository, artifact, filesystem, and runtime state;
6. incorporate the independent Final Goal Judge result when Full autonomous mode applies.

If any material criterion remains incomplete, blocked, or unverified, report PARTIAL or FAIL, never DONE.

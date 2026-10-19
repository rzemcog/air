---
name: instruction-conflict-resolution
description: Resolve a material conflict between applicable agent instructions without duplicating the shared policy or creating a parallel workflow.
version: 0.1.0
author: EgL
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [instructions, policy, conflict-resolution]
    related_skills: [goal-fidelity-execution, skill-adaptation]
---

# Instruction Conflict Resolution

Use this skill only when the user asks to resolve an instruction conflict or when two applicable instructions materially prescribe incompatible actions. For ordinary ambiguity, follow the governing instruction and use judgment without starting a conflict review.

The normative authority and scope contract lives in [`../../shared/agent-policy.md`](../../shared/agent-policy.md). This skill applies that contract; it is not a second authority system, status model, or validation lifecycle.

## Resolve a material conflict

1. **Name the decision.** State the concrete action or outcome that cannot satisfy both instructions. Ignore wording differences that do not change behavior.
2. **Check applicability.** Read the relevant instruction sources and determine whether each applies to this task, runtime, file, actor, and action. Use current runtime and filesystem facts where scope depends on them.
3. **Apply the shared contract.** Resolve authority, specificity, scope, ownership, and explicit user intent using Shared Policy. Preserve constraints that can be composed; do not manufacture a conflict when both can be followed.
4. **Keep ownership clear.** Goal state and completion decisions remain with the root agent; execution rules remain with their owning skill; an observer evaluates progress; a final judge evaluates the completion claim. Reuse suitable existing evidence and assign one owner to each new evidence acquisition.
5. **Choose the smallest safe resolution.** In order, try a compatible interpretation, clarify scope or trigger, reuse the existing owner or mechanism, and make a narrow local repair. Change the shared contract only when evidence shows its universal rule is the source and the change has the required authority. Retain all protections and user outcomes that still apply.
6. **If unresolved, stop only the affected action.** Record the competing applicable instructions, the concrete incompatibility, the blocked scope, and the decision needed in the existing task record. Continue independent work only when it advances the user's outcome or removes the blocker.

## Useful diagnostic lenses

When they help explain a real conflict, describe it in plain terms such as authority, scope, ownership, duplication, semantic mismatch, workflow order, or runtime capability. These are optional lenses, not required fields, labels, or a new ledger.

## Handoff

Report the governing instruction, the minimal resolution, any preserved constraints, and any remaining decision or runtime limitation. Do not claim that an instruction was loaded, enforced, or independently activated without evidence from the actual runtime.

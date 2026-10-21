---
name: instruction-conflict-resolution
description: Resolve escalated material instruction conflicts using the governing policy contract supplied by the host, without independently setting instruction authority.
version: 0.2.0
author: EgL
license: MIT
platforms: [linux, macos, windows]
---

# Instruction Conflict Resolution

Use this skill for a **material unresolved conflict** between applicable instructions, when explicitly asked to review such a conflict, or when AIR escalates a conflict that deterministic resolution and the Semantic Resolver could not settle. Routine ambiguity and already resolved cases follow the governing instructions without a new review.

## Normative contract and inputs

The **single governing Shared Policy** defines authority, scope, user intent and conflict modes. The host integration is responsible for providing that contract to this skill, either in the active instruction context or through a host-supported discovery/loading mechanism. This skill does not hardcode a filesystem path, replicate the authority hierarchy or introduce its own normative ranking.

Before deciding, establish:

1. The applicable Shared Policy and its provenance/version as made available by the host.
2. The two or more relevant instructions with source identity, scope, actor, triggering action and actual conflicting outcome.
3. Any supplied AIR Conflict Decision / Resolution Overlay excerpt with decision IDs, validation status and reason for escalation. Its presence does **not** replace the governing contract.
4. The requested decision and the smallest affected action that may be blocked.

If Shared Policy is unavailable or its provenance is not trustworthy, do **not** infer authority from file names, delivery role, relative paths or personal convention. Ask for the missing governing contract or report the local blocker. Continue independent, permissible work.

## Resolve the escalated conflict

1. **Identify the material incompatibility.** Describe the concrete action or outcome that cannot satisfy both applicable requirements. Ignore merely stylistic differences.
2. **Verify applicability.** Use verified runtime facts and source provenance to determine which instructions apply to the task, actor, action, path and lifecycle situation. Unknown facts are recorded as unknown; no invented defaults.
3. **Apply the supplied Shared Policy.** Follow its authority, specificity, scope, ownership, explicit user intent and interactive/silent mode. Preserve compatible requirements. Do not change message-level host authority by prose.
4. **Preserve responsibility.** Root owns the task outcome and final completion claim; owning skills keep their execution requirements; observers/reviewers evaluate within their own mandates. Reuse sufficient existing evidence rather than producing duplicate work.
5. **Find the narrowest compatible resolution.** First reconcile interpretations, then disambiguate scope/trigger, then reuse the correct owner/mechanism. Propose a targeted source correction only if authorized; never silently rewrite Shared Policy, Canonical Sources or a cached generated result.
6. **Escalate or block locally if unresolved.** State competing instructions, concrete conflict, blocked action, information/decision required and preserved independent work. Request a user decision where the governing mode requires it.

## Handback to the caller

Return a concise record containing governing source/provenance, applicability, minimal resolution or `UNRESOLVED`, preserved constraints, affected scope, reason for blocker and outstanding decision. Reuse the caller's existing task log/trace; create no parallel authority store or status taxonomy. AIR or the host decides whether to cache, redeliver or resume the affected action.

Do not claim a successful hook, loaded contract, model visibility or downstream compliance without independent runtime evidence. Do not silently promote this skill into a replacement for AIR Semantic Resolver.

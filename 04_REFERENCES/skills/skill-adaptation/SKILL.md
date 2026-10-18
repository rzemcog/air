---
name: skill-adaptation
description: Adapt upstream skills without losing provenance.
version: 0.1.0
author: EgL, Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [skills, adaptation, provenance, workflows]
    related_skills: []
---

# Skill Adaptation

Use layered adaptation when an upstream skill is useful but its defaults do not fully match the user's runtime, policies, or project conventions. Preserve the upstream source as an updateable reference; put local behavior in a separately owned adapter or overlay.

This is a universal workflow. It is not a router, does not install every discovered skill, and does not make upstream guidance authoritative over explicit user policy.

## When to Use

Use when:

- importing skills from an external repository;
- adapting an upstream skill to Hermes or another agent runtime;
- reconciling upstream defaults with durable user preferences;
- reviewing an upstream update;
- deciding why a candidate skill is deliberately not enabled.

Do not use for a one-off task that needs no reusable skill or provenance record.

## Instruction compatibility check

For a material adaptation or a real instruction conflict, use the conflict contract in the canonical Shared Policy. Do not repeat its authority ladder here.

Treat an adaptation as material when it could change an instruction's trigger, domain, ownership, dependencies, state, workflow order, validation, retry or stop behavior, completion boundary, safety, or runtime requirement. If none of those dimensions change, use a lightweight content check and skip expanded compatibility analysis.

1. Check applicable system, developer, `AGENTS.md`, shared, project, and skill instructions vertically. Compare peer skills only when their triggers and affected behavior plausibly overlap; do not perform a pairwise audit of unrelated skills.
2. Compare only the dimensions that can change this adaptation: trigger, domain, dependencies, owned files or state, authority, workflow stages, validation, retries, and runtime capabilities.
3. Classify the result as `Compatible`, `Adaptable`, or `Architectural conflict`. These describe the compatibility finding; they are not acceptance criteria or task status values.
4. Resolve local terminology, scope, and redundant steps when the change preserves ownership and safety. Do not silently change shared authority, ownership, safety, or user-approved decisions; route a material unresolved conflict to the appropriate owner.
5. Record only a decision that affects selection, adaptation, or future maintenance, in the existing adaptation record. Do not add a per-skill compatibility ledger or recurring telemetry.

## Procedure

1. **Discover the source.** Identify the repository or URL, owner, license, revision, and exact candidate paths. Read the source instructions and the candidate skill files. Done when the source and revision are reproducible.

2. **Inspect the local surface.** For a material adaptation, inspect only the applicable shared/project instructions, relevant skills with overlapping triggers or behavior, and runtime capabilities that can affect the changed dimensions. Identify applicable duplicate names, conflicting defaults, unavailable tools, and side effects. For a non-material documentation or administrative edit, do only the lightweight content check and skip this expanded search. Done when the affected candidate's relevant ownership and compatibility are clear.

3. **Choose a bounded set.** Include only skills with a clear recurring use and an owner. Prefer adapting one coherent class over installing a whole repository. Record every non-selected candidate in an exclusion ledger with a reason and a revisit trigger. Done when included and excluded counts equal the discovered candidate count.

4. **Absorb or compose.** If the candidate has the same trigger, goal, and output as an existing canonical skill, absorb only its useful practices into that skill and record the source. Create a composition adapter only when the sources retain different contracts or stages; the adapter should call or point to the canonical skills rather than duplicate them. Keep a candidate excluded when it is merely a router, a thin wrapper, runtime-specific, or not recurring. Done when each overlap is classified as `absorbed`, `composed`, or `deferred`.

5. **Separate ownership.** Keep upstream in a separate checkout. Store adapted skills in a local managed directory. Never edit upstream to encode local policy, and never blind-copy an update over an adapted file. Done when upstream and local paths are distinct.

6. **Write provenance.** Record source URL, revision, source path, local path, adaptation status, and local deviations in an adaptation manifest. Record exclusions separately; an exclusion is a decision, not a missing file. Done when another agent can reconstruct the selection without this conversation.

7. **Apply the overlay.** Preserve useful upstream concepts, but rewrite conflicting defaults in the local adapter. Keep project invariants in project files, not in a global skill. Done when each material deviation has a stated policy reason.

8. **Validate.** Check frontmatter, stable names, descriptions, non-empty bodies, referenced support files, path portability, and deterministic scripts. Validate only the changed contract and direct dependencies; reuse current evidence for unchanged source and runtime. Run a relevant skill test only when it covers a material behavior that inspection cannot establish. Done when the scoped validation passes and no protected upstream file changed.

9. **Verify discovery.** Use `skills_list`/`skill_view` or the runtime's equivalent, then exercise one representative workflow. If the loader caches its index, verify after a new session or reset. Done when the intended source is enabled, or the cache limitation is recorded.

10. **Review updates.** Fetch the new upstream revision, diff only selected source paths, classify changes as adopt, adapt, reject, or investigate, and update both manifests. Do not silently re-enable an excluded skill because its upstream text changed.

## Required records

Maintain these records for every external collection:

- **adaptation manifest:** included skills, source paths, local paths, pinned revision, and deviations;
- **exclusion ledger:** excluded paths, reason, disposition, and revisit trigger;
- **overlap disposition:** whether a practice was absorbed into a canonical skill, composed into an adapter, or deliberately deferred;
- **policy layer:** durable precedence rules that must survive upstream updates.

Use one canonical record for each role. Do not duplicate the same decision in multiple journals.

## Pitfalls

- Installing every upstream skill increases trigger collisions and context load.
- Copying upstream files destroys the update boundary and loses local rationale.
- A skill that is useful in its source repository may assume its tracker, CLI, files, or agent runtime.
- An exclusion without a reason will be accidentally reconsidered as a forgotten task.
- A successful file write does not prove runtime discovery or behavior.
- Upstream examples are references, not product requirements.

## Verification Checklist

- [ ] Source URL, revision, and exact paths are recorded.
- [ ] The source checkout is separate and clean.
- [ ] Included and excluded candidates are exhaustive and counted.
- [ ] Every exclusion has a reason and revisit trigger.
- [ ] Local policy is outside upstream files.
- [ ] Existing support files and runtime discovery were checked.
- [ ] Validation and a representative workflow were actually run.

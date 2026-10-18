# Agent Context Entrypoint

This is the local, non-repository entrypoint for agents working across the user's devices.

Use it before local setup, networking, remote access, dependency installation, Docker pulls, registry access, database access, or other environment-sensitive work.

## Start Here

1. Run `hostname` and identify the current OS.
2. Open the device registry:
   - `C:\Users\EgL\.agents\devices\INDEX.md`
3. Match the current hostname to a device profile.
4. Read the project-owned device/runtime reference for the active project.
5. Choose a target device by its documented purpose and use the current device's connection alias.
6. Start with a bounded read-only identity or health probe.
7. Obtain explicit approval before deploys, restarts, migrations, DB writes, secret handling, or other non-diagnostic side effects. A diagnostic request authorizes bounded probes and operations whose effects are limited to per-user diagnostic state, such as health-check status or refresh of a local provider cache, when they do not alter persistent configuration, publish or write shared data, change routes/listeners beyond loopback, or require secret handling. Restore temporary settings and verify the result. Ask before actions outside this boundary.
   Discovering and querying an already-running controller bound to `127.0.0.1`, `localhost`, or `[::1]` is diagnostic and requires no separate confirmation, including bounded read-only state requests and health checks. Verify that the listener is the intended controller/API before using it. Enabling or exposing a controller, changing its configuration, or restarting a service/core to create access is a configuration change and requires explicit approval. This does not waive the separate approval for secret handling.

Current Windows device profile:

- `C:\Users\EgL\.agents\devices\windows-desktop.md`

OpenDrugs device references:

- see `C:\Users\EgL\.agents\devices\INDEX.md`;
- the registry points to existing project-owned OpenDrugs runbooks instead of creating a second project source of truth.

If the current hostname is absent from the registry, do not reuse another device's assumptions. Stop environment-sensitive execution and create or request the missing profile.

## Scope

This directory stores local device identities, connection entrypoints, constraints, and links to project-owned references.

Project-specific instructions, architecture, runbooks, plans, and source-of-truth documents should stay inside the relevant project repository.

## Safety

- Do not print secrets from local env files, shell profiles, credential stores, or neighboring config files.
- An SSH alias proves only that connection configuration exists; it does not authorize remote changes.
- Treat this context as local operational guidance, not as project truth.
- If local facts conflict with repository instructions, report the conflict instead of silently choosing one.

## Instruction-file completeness

Жди EOF, а если ты его не видишь, значит файл неполный.

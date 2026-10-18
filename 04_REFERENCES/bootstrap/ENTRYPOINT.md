# Agent Entrypoint

Resolve `~` to the current user's home directory.

Read and apply every file directly in `~/.agents/shared/` before substantive work. Do not reread unchanged content already available in the active context.

If the output of a required instruction file is truncated, continue reading until the entire file has been retrieved.

Use `~/.agents/` as the user-level context root. Consult other materials only when relevant to the task.

For environment-sensitive work, consult `~/.agents/devices/INDEX.md` and relevant device profiles, verify mutable runtime facts, and follow project-owned documentation. Identify unlisted devices independently.

When modifying `~/.agents/`, read and follow `~/.agents/AGENTS.md`.

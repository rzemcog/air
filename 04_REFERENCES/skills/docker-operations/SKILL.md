---
name: docker-operations
description: Use when any agent needs local Docker. Start it safely.
---

# Docker Operations

Use this skill for local Docker work on this device.

## Daemon Not Running

- Starting Docker Desktop, inspecting local Docker state, and running necessary safe local checks are permitted when authorized by the current task and allowed by higher-priority instructions and the execution environment. Do not request redundant approval for already authorized safe operations. Do not start, stop, restart, delete, or recreate unrelated containers or modify persistent volumes as an incidental effect of verification. Require explicit approval before destructive operations, persistent data modification, production mutations, or unauthorized external effects. Check required permissions before expensive implementation. If an operation is blocked, preserve any useful preparation separately and report the precise blocker.
- Check `docker context show` and `docker context inspect <context> --format '{{json .Endpoints}}'` before starting Desktop. Start it automatically only when the active endpoint is the local Windows named pipe (`npipe:`); never switch contexts automatically or start local Desktop for a remote context.
- If `docker info` succeeds, continue with CLI work even if the Dashboard window is absent. Engine readiness and Dashboard visibility are separate checks; use `computer_use(action='list_windows')` when the task actually requires the GUI.
- If the Engine is down and no `Docker Desktop`/`com.docker.backend` process exists, invoke the shared helper from PowerShell with the tested command `powershell.exe -NoProfile -NonInteractive -Command '& (Join-Path $env:USERPROFILE ".agents\skills\docker-operations\scripts\start-docker-desktop.ps1") -TimeoutSeconds 120'`. It starts the installed EXE once in the current interactive user session, uses `%USERPROFILE%` as the working directory, omits `ELECTRON_DISABLE_SANDBOX` from the child environment, restores the parent environment immediately, and waits up to a bounded timeout for `docker info`.
- On this Hermes host, a controlled direct-launch test failed when the inherited `ELECTRON_DISABLE_SANDBOX=1` reached Docker Desktop and succeeded when only that child variable was omitted. Keep this per-child workaround; do not persistently edit user/system environment settings.
- **Codex on Windows:** before treating `AuthorizationManager` rejection, a sandbox startup timeout, or `npipe:` `permission denied` as a Docker Engine blocker, follow the bounded diagnostic and permitted-execution fallback in [`references/codex-windows.md`](references/codex-windows.md). Keep this harness-specific handling out of the shared helper.
- If Docker Desktop/backend processes already exist while `docker info` fails, do not spawn another copy or force-kill the backend. Wait once for the bounded timeout, then inspect logs and report the concrete startup blocker. Backend termination can interrupt running containers and requires separate authorization.
- After the Engine becomes ready, verify `docker info` and inspect `docker ps`. If a task's required named container is stopped or missing, inspect `docker ps -a` and the project's runbook; start only an existing container when the task/runbook clearly calls for it. Do not create, remove, prune, reset, or reconfigure Docker resources, change Docker Desktop settings, or modify persistent data without explicit approval.
- When startup times out, mark only Docker-dependent steps as blocked and continue independent work. State what was attempted, the observed failure, and the next useful diagnostic; do not silently abandon the whole task.

## First Reads

- Read `C:\Users\EgL\.agents\ENTRYPOINT.md` when present.
- If working inside a repository, read its Docker/local-dev runbook before changing Docker state.
- Do not print secrets from `.env`, Docker auth files, shell profiles, credential helpers, or registry tokens.

## Safety Rules

- Treat container creation, volume changes, image removal, and migrations as write-capable local state changes.
- Inspect before changing: `docker ps -a`, `docker images`, relevant ports, and existing container names.
- For long-running services, prefer named containers and stable localhost port bindings.
- When using env secrets, pass them through temporary process environment variables; do not put secret values in command text or output.

## Windows / Docker Desktop Notes

- Docker Desktop may show daemon proxy as `http.docker.internal:3128`; that is Docker Desktop's internal proxy, not the upstream Mihomo port.
- On this device, Mihomo exposes useful local ports:
  - mixed: `127.0.0.1:7890`
  - socks: `127.0.0.1:7891`
  - http: `127.0.0.1:7892`
- For Docker Desktop manual proxy, prefer HTTP proxy URLs: `http://127.0.0.1:7892` for both HTTP and HTTPS.
- SOCKS may be accepted by Docker Desktop settings but can fail during Docker Hub registry TLS handshakes.
- Fresh Docker proxy logs usually live at `C:\Users\EgL\AppData\Local\Docker\log\host\httpproxy.log`.

## Network Failure Ladder

For safe idempotent network operations such as `docker pull`:

1. Retry a small number of times; this network often fails intermittently.
2. Verify Docker Desktop proxy settings and the relevant registry endpoints with a non-secret request.
3. Prefer registry mirrors when the canonical registry is unstable. For Docker Hub images, try `mirror.gcr.io/<repo>:<tag>` if policy allows, then tag the local image back to its canonical name.
4. If Docker Hub or a mirror transfers layers but fails late on metadata/referrers, retry; cached layers can make the next attempt succeed.
5. If repeated retries fail, notify the user and name concrete options: change Mihomo routing/node, download/export the image from another machine, or use a technically safe alternative source.

## Known Local Workaround

During the OpenDrugs pgvector setup, the successful path was:

- Docker Desktop manual proxy: `http://127.0.0.1:7892`.
- Temporarily disable Docker Desktop `UseContainerdSnapshotter` when OCI referrers/attestations requests keep failing and no important local images/containers depend on the containerd image store.
- Pull through `mirror.gcr.io`, then tag to the canonical image name.

Keep this as a troubleshooting pattern, not a universal rule. Record or report any Docker Desktop setting changed and where its backup is stored.

## Readiness Checks

- For a running container: `docker ps`, `docker logs`, and container-specific health/readiness commands.
- For PostgreSQL containers: use `pg_isready` first, then read-only SQL checks such as `SELECT version()` and `SELECT current_database()`.
- Confirm localhost port bindings with `netstat` or `Get-NetTCPConnection`.

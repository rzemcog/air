# Reuse references / live links

**Проверить actual revision и hooks APIs по исходникам перед заимствованием.** Ни одна из ссылок не доказывает, что проект установлен у пользователя. Ссылки — материалы для следующей реализации, не требование установить все одновременно.

| Приоритет | Источник | Назначение | Статус |
|---|---|---|---|
| 1 | https://github.com/code-yeongyu/codex-rules | Основной кандидат: Codex plugin, `SessionStart`, `UserPromptSubmit`, `PostToolUse`, `PostCompact`, dedup/cache, тесты, packaging. MIT; проверить версию и licence file. | **Reuse candidate, архитектура одобрена** |
| 2 | https://learn.chatgpt.com/docs/hooks | Официальные native hooks, `SessionStart(source=compact)`, `SubagentStart`, `PostCompact`, `additionalContextLimit`, stdout/JSON и scope. | **Обязательный contract check** |
| 3 | https://github.com/Diluka/codex-subpath-agentsmd-hooks | Windows/PowerShell path handling, project/child `AGENTS.md` maps. Брать идеи/код с лицензией, не активировать одновременно. | **Read-only reference** |
| 4 | https://github.com/JuliusBrussee/caveman | Native skill reinforcement и компрессия progress. Есть snapshots из старого handoff. | **Pattern only** |
| 5 | https://learn.chatgpt.com/docs/agent-configuration/subagents | Custom subagents через `.codex/agents/*.toml`/`~/.codex/agents/*.toml`, scope. | **Contract for later Observer** |
| 6 | https://github.com/yimengbenxin/codex-goal-supervisor | Возможное использование goal-checking, judge, checkpoints для отдельного Goal Observer. Не вносить собственный North Star. | **Deferred** |
| 7 | https://github.com/pirate/codex-structured-steering | Аналог pro-active assumptions/steering, близок концептуально You Should Know. | **Deferred** |
| 8 | https://github.com/openai/codex | Источник информации о coverage инструментов, hook routing, collaboration JSONL. | **Diagnostics only** |

**Документированные ограничения (обновить при фактическом тесте):**
- `SessionStart(compact)` before next root model request. Plain stdout adds developer context.
- `PostCompact` stdout not injected, handler useful for invalidating cached state.
- `SubagentStart` can add developer context to child.
- Hook context by default ограничен ~2500 tokens per handler; configure `additionalContextLimit` carefully and detect truncation.
- `PreToolUse` includes tool input for supported local function tool paths, but specialized calls may opt out. **Не считать intercept of `spawn_agent` proven in ChatGPT.exe**.
- `codex-rules` from upstream adds broad sources `CLAUDE.md`, `.cursor`, `.github/instructions`, etc. **Отключить broad discovery; доверять лишь явно указанным пользователем sources**.

Исходные документы в новом архиве — `04_REFERENCE_SNAPSHOTS` (не перезаписывать ими пользовательские актуальные `.agents`).

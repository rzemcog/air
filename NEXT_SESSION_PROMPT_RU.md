Продолжи проект **Codex agent workflow / Agents Policies** по приложенному облегчённому handoff ZIP.

Сначала читай `README_START_HERE.md`, `HANDOFF_COMPACT_RU.md`, `02_DECISIONS/ARCHITECTURE_DECISIONS_RU.md`, `01_CURRENT/AGENTS_POLICIES_TZ_RU.md`. Остальные reference/evidence файлы — только при необходимости. `.git` в ZIP реконструирован из известных версий; не считать его оригинальной историей пользователя.

`Zapret Maintainer` остановлен пользователем (`PAUSED_BY_USER`). Не запускай ни один AC, router tests, SSH mutating commands, `/goal` auto-resume, live smoke. Цель текущего этапа — **Agents Policies plugin для Codex Desktop Windows**.

Архитектуру уже обсудили, пересмотрели и приняли. Не возвращайся к проектированию с нуля: reuse `https://github.com/code-yeongyu/codex-rules`; reference `codex-subpath-agentsmd-hooks`, official Codex hooks, Caveman, Ultracave. Реальные API и поддержку Desktop нужно проверить.

Соблюдай границы: native AGENTS.md остаётся Codex, actual installed bootstrap не дублировать; canonical ENTRYPOINT и selected shared policies; full injection при compact, scope-aware SubagentStart, selected hot sections на UserPromptSubmit, hashes/cache per context generation, policy-only structured trace; explicit trusted source selection, безопасная обработка secrets/truncation. `UserPromptSubmit` не решает длинный intra-turn, PostToolUse вариант ещё гипотеза.

§2 утверждён; §3 Ultracave без новых правок; provenance уже принят. Пиши minimal patch с тестами и rollback, не создавай другой agent framework. Root по умолчанию координатор, независимая реализация и тесты делегируются субагентам; сам интегрирует. В первую очередь изучить actual installed state и upstream code; для smoke использовать только безопасный isolated test project.

Goal Observer/Agent Audit/You Should Know/MCP wrapper/UI отложены. Результат: installable plugin, точные изменения, unit/integration/e2e tests, evidence model-context delivery отдельно от соблюдения правил, состояние/rollback/остаточные gaps. Не заявляй успех без end-to-end проверки.

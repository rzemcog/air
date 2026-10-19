# ТЗ: Agents Policies — управляемая доставка агентных правил в Codex Desktop

**Статус:** принятая архитектурная основа из совместного review Sol-5.6/Sol-6 и замечаний пользователя. Это **следующая задача**. Изменения не реализованы и не проверены. Реализовать минимальный working MVP с реальным Codex Desktop smoke, а не ещё одну теоретическую спецификацию. **Не возобновлять Zapret Maintainer.**

## 1. Цель и действующие условия

В текущей конфигурации `~/.agents/AGENTS.md`/`ENTRYPOINT.md`/`~/.agents/shared/` правила читаются агентом через инструменты. При `compaction` содержимое внешних файлов не гарантировано восстанавливается как full text; строгий §2 также часто нарушается в 9+ часов даже когда был ранее прочитан. Нужно увеличить **проверяемую доставку канонических правил**, не вводя новых competing instruction sources.

MVP plugin: `Agents Policies`, Codex Desktop Windows first. `Hermes` рассматривается как будущий adapter (не переносить его в обязательную часть MVP). User controls exactly selected files/dirs, with explicit scopes and provenance. Отсутствие конфигурации/источника должно быть видно.

**Root-agent orchestration для реализации plugin:** прежде чем менять файлы, распределить независимые exploration, source review и test harness задачи по субагентам параллельно, с конкретным ownership/files/acceptance. Root — integrator, owner безопасности и проверяющий, выполняет самостоятельно только тривиальные действия с меньшим overhead. Никаких параллельных изменений общего config/plugin cache одного профиля.

## 2. Reuse прежде нового кода

1. Прочитать актуальный upstream `https://github.com/code-yeongyu/codex-rules`: `hooks`, `src`, cache state, `SessionStart`, `UserPromptSubmit`, `PostCompact`, packaging, tests/license. Реально оценить объем изменений; выбрать fork/minimal-adaptation или small wrapper, не копировать файлы без соблюдения лицензии.
2. `https://github.com/Diluka/codex-subpath-agentsmd-hooks`: read-only источник для Windows/Subpath/AGENTS scope semantics. Не активировать его рядом как независимый плагин.
3. `https://github.com/JuliusBrussee/caveman`: reference `SessionStart` reinforcement и различие Claude `UserPromptSubmit` / Codex; локальные исходники включены в старом архиве handoff. Не зависеть от установленного Caveman.
4. `https://learn.chatgpt.com/docs/hooks`: официальный schema/hook contract; docs могут быть новее installed Desktop — подтвердить e2e. `SessionStart(compact)` возвращает context до следующего запроса модели, `SubagentStart` передает developer context ребенку; `PostCompact` не умеет injection plain stdout.
5. `https://learn.chatgpt.com/docs/agent-configuration/subagents`: native subagents TOML; не подменять их Markdown из `~/.agents/agents/`.
6. Зафиксировать version/commit hash каждого заимствованного upstream и ссылку на license в provenance.

## 3. Обязательный функциональный контракт

**Sources:** explicit manifest, например `~/.agents/policies.toml`; имя/схема могут отличаться при обоснованной совместимости с upstream. Absolute/global file and dirs, project-scoped file and dirs; deterministic file enumeration, precise recursive opt-in, max size, excludes, path normalization (Windows drive, `~`, symlinks), canonical path, SHA256 и scope. Native Codex `AGENTS.md` разрешается только native scanner. Не превращать untrusted project Markdown в global developer instruction.

**Initial state:** проверить текущие `~/.agents/AGENTS.md`, `ENTRYPOINT.md`, shared, `.codex/config.toml` и installed hooks. На первом этапе startup остаётся через existing bootstrap; plugin не повторяет тот же полный текст. Проверить фактический порядок на тестовом проекте. При необходимости согласовать атомарное изменение bootstrap вместе с настройками plugin; ни скрытого двойного чтения, ни silently missing essential instructions.

**Resume/compact:** `SessionStart(source=compact)` безусловно inject current mandatory full bundle независимо от hashes/cache. Если postcompact marker не приходил или generation не совпал, компактный fingerprint не должен блокировать восстановление. `PostCompact` invalidates injection state, не рассчитывать, что его stdout попадет модели. `resume` обязан проверить гарантии/дубли по действующему lifecycle.

**Child:** `SubagentStart` inject minimal applicable policy set с учетом роли, path/scope, negation, authored API; не инжектить human-progress §2 ребенку как обязанность писать Root progress, если он сам сообщений пользователю не публикует. Проверить, что модель ребенка реально увидела важные инструкции (не только что hook вызван).

**Hot:** `UserPromptSubmit` inject short *canonical excerpts* из `output-policy.md §2`, релевантного `style.md` и `communication.md`, optional §4 final. Extraction via headings, без дублирования содержимого в конфиге и без дополнительного `HOT.md` source-of-truth. Не вводить большие файлы каждый user turn. Отличать full injection cache от hot reminder cache. При смене файла hot excerpt свежий на следующем событии.

**Single long turn:** проверить по реальному Codex hook stream, как обеспечить in-turn reinforcement после серии содержательных операций. `UserPromptSubmit` НЕ решает задачу внутри одного turn. Предпочесть minimal adaptive/phase-based signal вместо каждого `PostToolUse`, с bounded budget и измеренным overhead. Это **дизайн-гипотеза для теста**, не уже принятое поведение. Не включать без демонстрации эффекта/адекватного ограничения.

**Limits/errors:** для полного обязательного policy bundle проверить actual `additionalContextLimit`, stdout sizes, предел model-visible context. Default ~2500 tokens на handler. Не выдавать shortened preview за full load; по превышению лимита или отсутствию mandatory файла дать детерминированный status + корректное bounded решение, прежде чем считать AC выполненным. Не молчать при конфликтах scope/order.

**Fingerprint/trace:** append-only bounded local trace с session_id, agent_id/turn_id (если доступны), hook_event, generation, selected source+sha256+bytes, full/hot, attempted/success/error, duration. Успех hook ≠ подтверждение поведения модели; дополнительно transcript-level test. Не писать raw policy bodies, secrets, arbitrary tool inputs, transcript или assistant messages в trace. Срок хранения/ротация, конфигурация opt-out.

**Reliability:** fail-safe hooks, no service/daemon/external DB, no telemetry/network, no destructive global overwrites, concurrency-safe cache writes, rollback of plugin enablement, recoverable on Windows encoding/powershell/Node failures, unsupported hook events treated as explicit compatibility gap.

## 4. Проверки и критерии приёмки

- Unit tests: glob/path scope, symlink/boundary rejection, deterministic ordering, duplicate sources, missing/edited mandatory policy, heading selector, cache generation and changes, truncation/error paths.
- Hook contract simulation: startup/resume/compact/subagent/user prompt/PostCompact; validate legal stdout JSON and context visibility, default limit vs configured override.
- Windows exact environment: specific installed Codex Desktop build, existing plugin/hooks config and startup behavior. Не устанавливать второй одноимённый plugin; не ломать текущий bootstrap.
- **Real Codex Desktop E2E** в безопасном тестовом workspace: initial normal bootstrap без двойной инъекции; forced compaction then proof next request sees exact new hash/content; child proof subagent sees applicable policy; changed on-disk policy becomes available; hot reminder extraction matches canonical section; plugin disabled restores former behavior; source/file error reported.
- Controlled output §2 regression: multiple nontrivial user progress messages, verify actual limits before/after reload/compaction; separating `delivered` vs `complied`. Не обещать 100%-ное соблюдение.
- No extraneous plugin framework, service, background agent, ongoing monitoring or new memory provider. Не выполнять live Zapret, reboot или AC tasks в ходе проверки policy loader.
- Deliver diff, tests with exact output, allowed configs, installation/rollback instructions, capability gaps, upstream license/version, no unapproved modifications to global machines.

## 5. Отдельные будущие workstreams, не включать в MVP

1. Goal Observer — independent hook-triggered judge/read-only, separate trusted goal source; check `codex-goal-supervisor` before implementing.
2. Root orchestration contract — за 10h Root фактически основной implementer. Не решать только reminder-ами.
3. Agent Audit — opt-in native agent-message telemetry if hooks provide plaintext, otherwise cannot reconstruct encrypted JSONL. Не копировать в Agents Policies trace.
4. UI file/folder picker, multiple providers/Hermes adapter, full bootstrap migration.
5. In-turn semantic compliance trigger only after measuring basic plugin; decide whether it belongs in future lightweight extension rather than inflating first release.

## 6. Условия завершения задачи

Не считать plugin готовым по `npm test` и написанному JSON alone. Нужны plugin load подтверждение в реальном Codex Desktop, проверяемый resumed/compacted policy контекст, child delivery, hot policy, no duplicate startup, fail-visible config errors, и безопасный rollback. Если feature недоступна именно в installed build: сохранить рабочий минимум, точный compatibility blocker и воспроизводимый test case, а не замаскировать failure заявлением `DONE`.

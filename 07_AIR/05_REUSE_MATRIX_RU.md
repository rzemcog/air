# AIR — матрица reuse по компонентам

**Обновлено:** 2026-10-19. **Взято за основу, а не изобретено повторно:** исходный handoff `REFERENCE_SNAPSHOTS/REUSE_LINKS.md` + `AGENTS_POLICIES_TZ_RU.md`; новая часть касается формата Vocabulary/Policy, resolver/cache и User Directives.

### Статусы

- `PREVIOUS_RESEARCH`: зафиксированное прежнее решение/направление, не гарантия актуального source audit.
- `README_VERIFIED`: на текущую дату сверено описание upstream/официальной документации; **не** построчный аудит и **не** тест на пользовательской машине.
- `NEW_CANDIDATE`: подходящий компонент обнаружен сейчас; нужно source-level vetting.
- `REFERENCE_ONLY`: важная идея, не тащить как runtime dependency.
- `NOT_AVAILABLE_AS_GIVEN`: не найдено готового компонента с нашим точным контрактом.

| Компонент AIR | Источник | Что переиспользовать / подсмотреть | Статус | Ограничения / решение для агента |
|---|---|---|---|---|
| Hook lifecycle engine, stdout/json, startup/compact | [code-yeongyu/codex-rules](https://github.com/code-yeongyu/codex-rules) | `SessionStart`, `UserPromptSubmit`, `PostCompact`, `PostToolUse`, handler entrypoints, fixtures/tests, runtime без prod npm dependencies | PREVIOUS_RESEARCH + README_VERIFIED | **Основной кандидат adapt/fork**, проверить лицензии/commit. Глобальный auto-discovery источников **отключить**. |
| Cache generation/session-level dedup | [codex-rules](https://github.com/code-yeongyu/codex-rules) | Session injection state, fingerprint/load/persist, time instrumentation | PREVIOUS_RESEARCH + README_VERIFIED | Не равно GPA semantic cache / Session Directives; обязательно просмотреть data model. |
| Hot reminder по событиям/tool outputs | [codex-rules](https://github.com/code-yeongyu/codex-rules) | Matching `apply_patch`, bounded PostToolUse, event timing | PREVIOUS_RESEARCH + README_VERIFIED | Покрытие tool calls не полно; не считать одно правило на каждый PostToolUse оправданным. |
| Windows paths, symlink/subpath, Git worktree | [Diluka/codex-subpath-agentsmd-hooks](https://github.com/Diluka/codex-subpath-agentsmd-hooks) | `scripts/project_map.ps1`, `tests/test_nested_git_e2e.ps1`, workspace exclusion, `commandWindows` | PREVIOUS_RESEARCH + README_VERIFIED | **Reference/targeted port**, не ставить параллельный scanner. Проект генерирует AGENTS.md map, а AIR не должен инжектировать карты вместо полного текста. |
| Compaction reminder/conservative plugin migration | [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) | Session hook/reminder patterns; atomic state writes and symlink guards, Windows install ergonomics | PREVIOUS_RESEARCH + README_VERIFIED | **Pattern only**; не зависеть от Caveman runtime и не изменять утверждённый Ultracave. |
| Host hooks specification | [OpenAI Codex Hooks](https://developers.openai.com/codex/hooks) / [Learn Hooks](https://learn.chatgpt.com/docs/hooks) | Event names, `additionalContext`, source compact, output limits, trust | PREVIOUS_RESEARCH + OFFICIAL CONTRACT | **Обязательный исходник**, Desktop version E2E требуется отдельно. Сверять actual URL/version. |
| Custom Agent Profile/subagent | [OpenAI Codex repo](https://github.com/openai/codex), [Subagents docs](https://learn.chatgpt.com/docs/agent-configuration/subagents) | TOML `developer_instructions`, actual role transport, event data | PREVIOUS_RESEARCH + OFFICIAL CONTRACT | Verify exact installed version; никаких предположений, что `SubagentStart` даёт надёжный `agent_type`. |
| Packaging / manifest | [Agent Plugins packaging](https://developers.openai.com/plugins/build/plugins) | Root `plugin.json`, `$schema` agent-plugins.org/1.0.0, `extensions.com.openai.hooks`, `PLUGIN_ROOT`, `PLUGIN_DATA`, optional compat manifest | NEW (в этой сессии) + OFFICIAL VERIFIED | **Переиспользовать стандарт**, не делать второй универсальный host manifest. Local Desktop trusted hooks; directory eligibility другая. |
| Policy/Vocabulary structural validation | [Ajv](https://github.com/ajv-validator/ajv) | JSON Schema validation, strict schema, rich errors | NEW_CANDIDATE + README_VERIFIED | Candidate dependency при TypeScript/Node; проверить build/runtime size, license MIT, schema draft, Windows bundling. |
| YAML loading | [yaml (eemeli)](https://github.com/eemeli/yaml) или уже установленный parser | Safe YAML parse/stringify, preserve source locations where available | NEW_CANDIDATE | Проверить availability; запрет unsafe custom tags; не реализовывать собственный YAML parser. |
| Declarative applicability (all/any/not) | [json-logic-js](https://github.com/jwadhams/json-logic-js) | Declarative evaluator по facts без динамического `eval` | NEW_CANDIDATE + LICENSE VERIFIED | **Adapt subset only**, важно запретить произвольные custom operations и проверить unknown-fact semantics. Возможно tiny custom evaluator проще. |
| Deontic `require/forbid/permit/prefer` | [Cedar](https://www.cedarpolicy.com/), [OPA](https://github.com/open-policy-agent/opa), [Casbin](https://github.com/apache/casbin-node-casbin) | Разделение requests/context/policies, типизированные permissions/effects, precedence patterns | NEW_CANDIDATE / REFERENCE_ONLY | **Не подключать движки целиком.** AIR управляет инструкциями модели, не исполняет hard authorization. Их `permit` semantics отличаются и не переносятся автоматически. |
| Policy version/hash | Node `crypto`, canonical JSON libraries / existing project utility | SHA256, deterministic serialization | STANDARD_LIB / ADAPT | Можно взять стандартную библиотеку; канонизацию надо явно определить, не использовать порядок YAML ключей как смысл. |
| GPA persistent cache | codex-rules state storage + Node filesystem primitives | Hook state, file atomicity/persistence patterns | PARTIAL_REUSE | Нужен **новый** content-addressed GPA model, у `codex-rules` нет подтверждённого семантического GPA resolver. |
| Conflict Decision cache | Versioned JSON + hashes; graph IR concepts | Fine-grained keyed relations/decisions | NOT_AVAILABLE_AS_GIVEN | Реализовать небольшую typed структуру; не притворяться, что upstream dedup == semantic conflict decisions. |
| In-memory Rule Graph/IR | ordinary adjacency lists/maps / Graphlib if already present | Rules, relation edges, invalidation | STANDARD_LIB / REFERENCE_ONLY | Нет причин ставить Neo4j/Kuzu/Graph DB; первое измерение complexity vs simple maps. |
| Semantic conflict resolver | existing configured inexpensive model/provider; native agent skill `instruction-conflict-resolution` | Structured output classification, skill procedure & authority rules | PREVIOUS_LOCAL + NEW ADAPT | У skill нет API, который hook может «вызвать» автоматически; LLM connector/transport in hook проверить. Не вызывать Root; не хранить секреты в публичном внешнем API без согласия. |
| Session Directive extraction | low-reasoning model via existing approved provider | Extract add/revoke/supersede/scope decisions from current user prompt | NOT_AVAILABLE_AS_GIVEN | Уточнить idempotency, contradictions, ambiguous scopes, safe failure mode. Hook side effect ≠ гарантия записи. |
| Session state storage | local filesystem / Codex `PLUGIN_DATA` | atomic JSON and generation tracking | PARTIAL_REUSE | Специальная durable пер-сессионная логика новая; не LRU. |
| Manual resolution inspection | existing filesystem/editor, generated `effective.md` | inspectable effective policy and provenance | STANDARD_REUSE | Не создавать UI ради v1; manual edits к generated file не сохранять молча как canonical. |
| Conflict skill and policy contract | приложенные `instruction-conflict-resolution` SKILL + `agent-policy_attached.md` | Уже работающий нормативный процесс; убрать hardcoded relative path | USER_PROVIDED / ADAPT | Только controlled diff, не переписывать автоматом. Убедиться в актуальном live экземпляре. |
| Goal Observer / judge | [yimengbenxin/codex-goal-supervisor](https://github.com/yimengbenxin/codex-goal-supervisor) | Goal checks / checkpoint refs | PREVIOUS_RESEARCH / DEFERRED | Не часть AIR первой версии. |
| Proactive steering | [pirate/codex-structured-steering](https://github.com/pirate/codex-structured-steering) | Event-based steering concepts | PREVIOUS_RESEARCH / DEFERRED | Не добавлять, пока delivery tests не пройдены. |

## Что точно не найдено как готовый целый компонент

Проверенные источники **не дают** полного продукта с нашими: `User > Agent > Project > Global`, content-addressed semantic conflict cache + editable corrections, per-session user-directive extraction, portable structured policy language, native/AIR non-dup and verified Desktop compaction. Поэтому reuse — **компонентный**, а не «установить готовый AIR».

## Что не было исследовано полноценно

- Реальные исходники каждого upstream на конкретном pinned commit, security/licensing beyond README.
- Однозначный cheapest provider/model и latency вызываемой через hook low-reasoning LLM.
- Реальная Windows Desktop совместимость plugin.json/hooks/install/trust.
- Semantic resolver/graph implementation options beyond известные библиотеки.

## Инструкция агенту reuse-review

Для каждой строки: `pin commit → inspect minimal related files → license/notice → test fixture → adapt decision → scope of changes`. Отличать «похоже по описанию» от «код прошёл наш Windows E2E». Не читать весь репозиторий подряд; изучить нужные функции и их tests. Выдать REUSE_DECISION с измеренной стоимостью переноса и альтернативой. Данные из исходного `REUSE_LINKS.md` не переизобретать; отличать новые кандидаты от старых.

# AIR — Architecture Decision Records (ADR)

**Статус:** консолидация прежних ADR и пользовательских решений текущего диалога; `ACCEPTED` означает согласие на уровне концепции, не доказательство готового кода. `CANDIDATE` и `OPEN` не заменять на `ACCEPTED` автоматически. Старый handoff хранится в `REFERENCE_SNAPSHOTS` и не редактировался.

## ADR-001 — Название и границы системы
**ACCEPTED.** Название системы — **AIR (Agent Instruction Runtime)**. Первая реализация — Codex Desktop на Windows: разрешение, доставка и восстановление инструкций. В будущем планируется интеграция функциональности менеджмента skills.

## ADR-002 — Граница Policy и Skill
**ACCEPTED.** **Policy отвечает:** «При каких условиях что обязательно, запрещено, разрешено или предпочтительно?» **Skill отвечает:** «Каким способом и в какой последовательности достичь результата?» Политика задаёт ограничения поведения через декларативные условия и модальности. Skill описывает выполнение и последовательность действий. Для навыков AIR использует native discovery Codex; переносимость ссылок между skills обеспечивается существующими механизмами маршрутизации.

## ADR-003 — Логические приоритеты
**ACCEPTED as semantic intent; RUNTIME_GATE for enforcement.** Current User > active Session Directives > Agent Profile > Project > Global. В частности, Agent Profile выше Project. `silent` автоматически применяет контракт, `interactive` выясняет существенные конфликты с пользователем. Authority System/Developer Codex остаётся вне пользовательской модели. Запрещено считать модельную текстовую декларацию способной поменять протокольные message roles.

## ADR-004 — Отдельный resolver и cache
**ACCEPTED.** Семантические сравнения выполняет выделенный дешёвый low-reasoning resolver, а не Root. Без самооценки уверенности и отдельной постоянной LLM службы. Два уровня кэша: GPA bundle и отдельно conflict decisions. Машинный Resolution Overlay хранится отдельно от model-visible instruction text; пользователь может посмотреть readable result и исправить его. Формальная валидация результата LLM не доказывает смысловую истинность.

## ADR-005 — Грамматика AIR документов
**ACCEPTED principle, SCHEMA_GATE details.** AIR определяет versioned Format Schemas, authored документы **используют** их через `format: air.vocabulary/v1` / `format: air.policy/v1`. Словарь (`Vocabulary`) объявляет доменные symbols/parameter types/facts и human-readable descriptions, но не обязанности. Policy объявляет Rules и ссылается на Vocabulary, не определяя symbols inline. Vocabulary открытые и расширяемые; формат фиксирован и версионируем. `schema:` как поле authored файла уступило `format:` во избежание двусмысленности.

## ADR-006 — Rule structure
**ACCEPTED direction, details CANDIDATE.** `Rule` вместо Instruction Unit. Отвергнуты BDD GIVEN/WHEN/THEN, лишние `subject`, `target`, `target_types`, универсальный `predicate` и обязательные ручные IDs. Пример рабочей структуры: `key?`, `modality`, `operation`, `parameters?`, `applies_if?`, `description?`. `modality` рабочие значения: `require|forbid|permit|prefer`. `description` — natural language opaque для deterministic core. Type constraints берутся из Vocabulary; не зарегистрированный symbol — ошибка, а не повод LLM придумать новый. `applies_if` — булева декларативная логика применимости; формат условий и семантика missing facts требуют фиксации.

## ADR-007 — Граница детерминированности
**ACCEPTED.** Deterministic core может parse/validate/canonicalize/typecheck/hash/evaluate known predicates/assemble. LLM читает free-form descriptions и возвращает ограниченные semantic relations; результат валидирует deterministic layer. Модель не модифицирует Canonical Source, authority, scope или symbols. Структурная проверяемость не гарантирует model compliance.

## ADR-008 — Policy Graph
**CANDIDATE, согласовано как полезная модель, не обязательная внешняя инфраструктура.** Производное in-memory IR/graph: Source→Rule и relationship edges. Не использовать GraphDB; не требовать DAG для полного графа. Fine-grained decisions можно кэшировать на уровне rules/edges; безопасность reuse зависит от контекста третьих правил. Если оправданность графа не подтверждается, может хватить flat IR + typed edges.

## ADR-009 — Native sources и delivery ownership
**ACCEPTED.** Codex сам отвечает за native `AGENTS.md` и native Custom Agent Profile. AIR учитывает их как inputs resolver и не повторяет тела через hook. На текущем историческом handoff `~/.agents/AGENTS.md -> ENTRYPOINT.md -> ~/.agents/shared/` — глобальный bootstrap workflow; расположение и актуальность live Codex installation требуется сверить. Имя `AGENTS.md` само по себе не определяет Global vs Project: классификацию задаёт scope/path. Delivery Plan зависит от host/event и не является постоянным свойством Source.

## ADR-010 — User delegation
**CANDIDATE, experimental.** Предложено узкое self-delegation в существующих `developer_instructions` каждого Custom Agent Profile: явный текущий user может переопределять требования только **данного Agent Profile**. Аналогичный ограниченный контракт внутри AIR Delivery Payload относится только к **этому** payload. Нельзя допускать неопределённое `for managed policies`. Профили старых агентов требуют явной миграции/backup; автоматический безопасный механизм пока не подтверждён.

## ADR-011 — Session Directives
**ACCEPTED model, RUNTIME_GATE mechanics.** Session Directives отдельно от GPA и не входят в reusable GPA cache. Текущий user prompt доставляется Codex напрямую; persistent директивы извлекаются дешёвой моделью и фиксируются как Session State для compaction, resume, subagent. Side-effect-only `UserPromptSubmit` — рабочая гипотеза, а не доказанный Desktop contract. `UserPromptSubmit` hot excerpt из прежнего handoff всё ещё утверждён и требует отдельного согласования с новой схемой (см. ADR-013).

## ADR-012 — Persistence/Trace
**ACCEPTED direction.** Authored sources/config отдельно от cache/session state. Windows root `%LOCALAPPDATA%` предпочтителен, конечное имя и выбор между ним/`PLUGIN_DATA` после проверки. `cache/gpa`, `cache/conflicts`, `sessions`, `trace`. Session State сохраняется на протяжении доступной для resume сессии. Атомарная запись; trace содержит служебные метаданные с ограниченной ретенцией; fingerprints/generation отслеживаются.

## ADR-013 — Hooks and recovery
**ACCEPTED intent, RUNTIME_GATE execution.** На `SessionStart(compact)` обязателен актуальный Recovery Payload при поддерживаемом hook; `PostCompact` не заменяет доставку. `SubagentStart` имеет scoped delivery; `UserPromptSubmit` в ранее утверждённой модели доставляет short canonical hot sections. В последующем обсуждении предложен side-effect-only handler, вызывающий separate user-directive resolver. Совместимость двух задач, порядок, timing, latency и необходимость дополнительной инъекции оставлены открытыми. In-turn `PostToolUse` — гипотеза, без подтверждения не включать.

## ADR-014 — Reuse/packaging
**ACCEPTED strategy.** Не начинать с нуля: `codex-rules` кандидат №1; `codex-subpath-agentsmd-hooks` Windows/scope reference; `caveman` reinforcement pattern; Codex official contracts обязательно. С новым AIR Vocabulary/PIR также проверить Ajv/JSON Schema, JsonLogic и policy engines как references. Agent Plugins root `plugin.json` + `extensions.com.openai` использовать как packaging/integration target при подтверждённой поддержке установленной версии. Без новых MCP/DB/daemon.

## ADR-015 — No guaranteed enforcement
**ACCEPTED.** AIR обеспечивает воспроизводимую обработку, доставку где поддерживается и наблюдаемость; не гарантирует 100% повиновение LLM. `hook exit 0`, trace и `cache hit` не подтверждают model-visible context и compliant behavior; раздельные E2E observables.

## ADR-016 — Legacy policies и миграция
**ACCEPTED direction, implementation OPEN.** Действующие `agent-policy.md` и `instruction-conflict-resolution` skill изменяемы: пользователь разрешил адаптацию. Сама структурированная политика становится canonical после явной миграции, legacy Markdown не нужно вечно поддерживать как равноправный DSL. **До cutover** нельзя потерять действующие правила или скрыто переписать исходные инструкции; migration diff/review/rollback обязательны. Native bootstrap очищается только после подтверждённого transport.

## ADR-017 — Статус AIR и происхождение решений
**FACT.** AIR находится в состоянии проектирования; результаты Windows Desktop экспериментов ещё ожидаются. Предыдущий handoff сохраняет согласованные исходные решения, последующие ADR уточняют архитектуру и условия проверки.

## Обязательные открытые решения перед `DONE`

1. Инсталляция plugin и фактический dispatch hooks на конкретной сборке Windows Desktop.
2. Authoritative delivery с profile developer instructions, user delegation и native `AGENTS.md` при compaction.
3. Нормативная семантика `permit`, unknown runtime facts и объявления custom symbols.
4. Нужен ли online semantic resolver синхронно в hook или только precompile/offline cache; как вести себя на cache miss при latency/error.
5. Разведение original `UserPromptSubmit hot reminders` и новой session-directive extraction.
6. Миграция текущих global bootstrap/ENTRYPOINT/agent-policy/Profile и наличие live files.
7. Алгоритм manual correction с cache invalidation и safe approval.

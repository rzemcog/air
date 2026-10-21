<!-- @style: ./.mdstyled/air.css -->
<!-- @script: ./.mdstyled/air.js -->
<!-- @page: air-docs -->

# AIR — где консенсус, а где доказательства

**Дата редакции:** 2026-10-22. Не путать «утверждено как дизайн» и «будет работать в конкретном Codex Desktop». В таблицах `точно` допустимо только для проверенной спецификации/логики, а не для неизвестного локального runtime.

## A. Консенсус текущего архитектурного обсуждения и прежних проектных сессий

| Тезис | Статус | Комментарий |
|---|---|---|
| AIR = Agent Instruction Runtime; первая реализация в Codex Desktop Windows | CONSENSUS | В будущем планируется интеграция функциональности менеджмента skills. |
| Policy формулирует применимость и нормативные требования; Skill задаёт способ и последовательность исполнения | CONSENSUS | Policy: «при каких условиях что требуется/запрещено/разрешено/предпочтительно?» Skill: «как и в какой последовательности достичь результата?» |
| Текущий user > Session Directives > Agent > Project > Global | CONSENSUS on intended authority | Не доказан технически из-за developer-role транспорта. |
| Отдельный cheap resolver для неразрешимых структурно semantic relations при валидном cache miss | CONSENSUS | Root не выполняет массовую semantic resolution; недоступность/невалидность → локальный `BLOCKED_RESOLUTION`. |
| GPA cache и Conflict Decision cache | CONSENSUS | Состояние user directives отдельное per session. |
| Не передавать overlay работающему агенту | CONSENSUS | Доставлять готовый набор применимых правил. |
| Native `AGENTS.md` и Custom Agent Profile не повторять | CONSENSUS as invariant | Верифицировать фактический native loading/recovery. |
| Versioned Format Schemas, открытые свободные vocabularies | CONSENSUS | Символы с human-readable descriptions, registry внутри загруженных vocabularies. |
| `format:` вместо `schema:` в authored файлах | CONSENSUS | Ссылки на формат, не определение формата. |
| `Rule` вместо Instruction Unit, убрать `subject` / target / BDD | CONSENSUS | Остальные точные YAML поля требуют schema proof. |
| `description` = natural-language zone, остальные поля typed | CONSENSUS | Вопрос «все ли NL semantics только там» нуждается формальным тестом. |
| User доступен к cache effective/resolution, manual corrections | CONSENSUS direction | Точный UX/override format не утверждён. |
| Native skill discovery, не вводить capability-ID registry | CONSENSUS | Не ломать native routing. |
| Agent Plugins manifest учитывать сейчас | CONSENSUS | Не означает, что AIR runtime semantics стандартизованы Agent Plugins. |
| `SessionStart(compact)` full recovery, scoped child, hot reminders | LEGACY ACCEPTED | Новый дизайн user-directive side effect вызвал конфликт назначений `UserPromptSubmit`, требует решения. |
| Функциональность менеджмента skills | PLANNED FUTURE | Сейчас используется штатное обнаружение навыков host. |

| Harness-agnostic Core, Host Adapter для конкретной интеграции | CONSENSUS | Codex paths/events описываются отдельно от общей архитектуры. |
| Адаптированный conflict-resolution skill | SOURCE PATCH APPLIED | Shared Policy без изменений, нужен эксперимент R8 для проверки host загрузки. |
| ТЗ экспериментов отдельно от Draft ТЗ реализации | CONSENSUS | В текущей редакции эксперименты CURRENT, реализация DRAFT. |
| Семантика Schema v1 | DEFERRED | `parameters`, `permit`, `applies_if`, missing facts, literals, `require`. |

## B. Точно НЕ работает как утверждалось (контракт или логическое противоречие)

| Утверждение/подход | Почему не работает |
|---|---|
| Считать `SessionStart.additionalContext` технически user-role и потому ниже direct user | По официальному hook contract это developer-context; не следует менять протокольный приоритет текстовым порядком. |
| Использовать `UserPromptSubmit` для повторного напоминания в середине уже идущего десятичасового turn | Event привязан к новому user prompt, не к серии tool calls внутри turn. |
| Считать `PostCompact` plain stdout доставкой инструкций на следующий model call | Не его подтверждённый механизм; full recovery планируется через `SessionStart(compact)`. |
| Удалить конфликтующую native инструкцию из контекста простым исключением её из AIR Payload | AIR контролирует только собственный payload. Уже доставленное нативно правило оттуда не исчезает. |
| `cache hit`/`hook exit 0`/успех сборки = доказательство модельного соблюдения правила | Логический non sequitur; нужны наблюдения model-visible и поведенческие тесты. |
| «Symbol `test.run` сам по себе имеет детерминированную семантику» без определения в vocabulary | Невозможна валидная структурная проверка, если символ не объявлен. |

## C. Скорее всего НЕ сработает надёжно без изменений

| Идея | Причина и нужный тест |
|---|---|
| Весь GPA+User внедрить в developer context, а затем надеяться на устное `User > Global` | Переход authority и противоречивые native sources. R2. |
| Вычислять persistent session directives однажды на SessionStart | User может изменить/отозвать директиву в любой turn. R6. |
| Кэшировать только pair hashes без scope/context/version | Третье правило и applicability могут изменить решение. Resolver cache invalidation test. |
| Deterministic candidate retrieval только при равных operation IDs | Разные словари могут описывать одно действие разными symbols; межсловарные скрытые конфликты останутся. Semantic candidate coverage test. |
| Обязательные session directives сохранять только в eviction-prone cache | LRU/GC может лишить session актуальных прав. State durability test. |
| После создания AIR автоматически полностью очистить global bootstrap | На конкретном Desktop hooks могут отсутствовать, потребуется staged rollout/rollback. R1/R3. |

## D. Скорее всего сработает, но нужно проверить установленный runtime

| Подход | Основание | Proof gap |
|---|---|---|
| `SessionStart(compact)` для последующей delivery | Документированный hook contract | Desktop dispatch, output limit, next model call. |
| `SubagentStart.additionalContext` для child | Документированный hook contract | Фактический child lifecycle/metadata и scoped visibility. |
| `UserPromptSubmit` как side effect | Допустимый output без обязательного injected context | Actual Desktop dispatch, latency, session identity/durability, privacy. |
| Узкая self-delegation внутри Agent Profile | Логически совместима с developer role, если профиль сам делегирует | Поведенческие тесты и конфликт с другими developer messages. |
| `codex-rules` как основа доставки/cache | Репозиторий содержит hook runtime/state/tests | Неизвестна стоимость адаптации к AIR schema и ограниченному allowlist. |
| Agent Plugins root manifest | Текущая документация поддерживает layout | Совместимость именно installed Desktop + hook trust. |

## E. Точно работает как локальный технический механизм (при корректной реализации)

- SHA256 неизменных байтов воспроизводим; content-addressed lookup возможен без LLM.
- JSON Schema проверяет структуру и типы документов, но не естественноязыковую истинность `description`.
- Typed symbol registry с явными namespace и version способен детерминированно отклонять неизвестные symbol names.
- Каноническая сериализация валидированного объекта + hash может обеспечить deterministic cache invalidation.
- Атомарное файловое сохранение с контролем ошибок и версий возможно локально на Windows; реальная конкурентность всё равно требует тестов.
- Утверждённый Delivery Plan может не повторять AIR-native source body **в payload**. Нельзя из этого заключать, что host не продублировал его самостоятельно.
- Structured relations можно хранить как JSON/graph IR без Neo4j. Наличие графа не гарантирует правильность relation.

**Честная формулировка:** это implementability, а не «AIR работает на ПК пользователя».

## F. Недоказанные и нуждающиеся в решении детали

1. Schema полей `parameters`, `permit`, `applies_if` + `unknown facts`.
2. Session State при fork/resume/manual history changes; доступность turn/session IDs в hooks.
3. Надёжная authority delegation User над Agent/Profile и AIR Payload.
4. Согласование hot reminders прежнего handoff с новой side-effect-only логикой.
5. Forced recovery без превышения лимита и без повышения untrusted project Markdown.
6. Инвалидация fine-grained Conflict Decisions с учётом новых третьих правил.
7. Латентность дешёвой модели на cache miss / privacy disclosure / отказ без потери текущего user prompt.

Каждое неизвестное сопоставлено с probe и `IF → THEN` в `05_EXPERIMENTAL_TZ_RU.md`.

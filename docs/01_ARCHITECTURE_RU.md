# AIR — Agent Instruction Runtime: рабочая архитектура

**Версия документа:** 2026-10-19 / consolidation-2  
**Статус:** консолидированная база по handoff и последующему диалогу, **не** утверждение технической работоспособности.  
**Назначение:** единый словарь и описание архитектуры для реализации; спорные места явно отмечены `OPEN` или `RUNTIME_GATE`.

## 0. Назначение AIR и архитектурная граница

**AIR (Agent Instruction Runtime)** управляет жизненным циклом инструкций агента: выбирает источники, проверяет их форму и применимость, разрешает противоречия, сохраняет результаты, подготавливает инструкции для модели и восстанавливает их при изменениях контекста. Первая реализация рассчитана на **Codex Desktop в Windows**.

**Policy отвечает:** «При каких условиях что обязательно, запрещено, разрешено или предпочтительно?»

**Skill отвечает:** «Каким способом и в какой последовательности достичь результата?»

Отсюда следует разделение языка и исполнения:

- **Policy** описывает нормативные ограничения поведения. В неё входят условия применимости и требования к действию или результату.
- **Skill** описывает процедуру работы: шаги, выбор дальнейших действий, проверку результатов и повторные попытки.
- **AIR** доставляет применимые инструкции и поддерживает их согласованное состояние. Существующий native skill discovery Codex используется для загрузки навыков.

В будущем **планируется интегрировать в AIR функциональность менеджмента skills**. Текущая работа посвящена policy language, resolution, delivery, восстановлению инструкций и состоянию сессии. Декларативная логика условий (`all/any/not`) входит в policy language; процедурное управление выполнением относится к skills.

## 1. Канонический словарь

Подробные определения, жизненные циклы и примеры находятся в **[`07_GLOSSARY_RU.md`](07_GLOSSARY_RU.md)**. Этот словарь является единым справочником терминов пакета.

| Термин | Значение в AIR |
|---|---|
| **Canonical Source** | Выбранный исходный файл или другой авторитетный носитель инструкций; изменения отслеживаются по fingerprint. |
| **Global Policy (G)** | Общие правила для нескольких проектов и агентных профилей в пределах своего scope. |
| **Project Policy (P)** | Правила конкретного репозитория, проекта или его поддерева. |
| **Agent Profile (A)** | Ролевые инструкции специализированного агента, в Codex обычно `developer_instructions`. |
| **User Instruction / Current User Prompt** | Прямое указание пользователя / текущее сообщение, доставляемое Codex. |
| **Session Directive** | Пользовательское указание, продолжающее действовать в этой сессии. |
| **Session State** | Сохраняемое состояние директив с версиями, статусами и происхождением. |
| **GPA Resolution** | Результат разрешения применимых Global, Project и Agent правил. |
| **Resolution Overlay / Conflict Decision** | Машинная карта отношений и конкретное решение по одному конфликту. |
| **GPA Cache / Resolution Decision Cache** | Кэши всего GPA Resolution и отдельных разрешённых конфликтов. |
| **Format Schema / Vocabulary / Policy / Rule** | Формат документа / объявление понятий / нормативный документ / отдельное правило. |
| **Policy IR / Graph** | Производное представление структурных правил, источников и отношений. |
| **Codex Integration / Delivery Plan** | Codex-специфичная интеграция и вычисленная схема доставки применимых правил. |
| **Native Source / Managed Source** | Источник, доставляемый Codex / источник, доставляемый AIR. |
| **Delivery Payload / Recovery Payload** | Готовые инструкции для hook / их набор для восстановления состояния. |
| **Policy Trace** | Диагностические записи о попытках и подтверждениях доставки. |

## 2. Источники и authority

Желаемая логическая иерархия **внутри пользовательски управляемого слоя**:

`текущая явная User Instruction > действующие Session Directives > Agent Profile > Project Policy > Global Policy`.

Это **договорённость о разрешении конфликтов**, а не изменение протокольной роли сообщений. Реальные system/developer/user роли Codex имеют собственный приоритет: custom `developer_instructions` и hook `additionalContext` могут иметь роль `developer`, прямой user prompt — `user`. Поэтому текстовый контракт делегации от developer к текущему user является **рабочим предложением, проверяемым экспериментом**; его нельзя объявить гарантией. Конфликты с другими developer/system требованиями нельзя снять произвольным YAML-правилом AIR.

`silent` mode: применить приоритет автоматически, записать решение. `interactive` mode: при материальном конфликте блокировать только зависимое действие и запросить у пользователя решение. Существующий `instruction-conflict-resolution` skill переиспользуется для конкретных нерешённых случаев и должен быть универсализирован без жестко зашитых путей, если это потребуется. Семантические решения заранее по возможности готовит отдельный дешёвый resolver, не Root.

**Native ownership:** если Codex уже загрузил Agent Profile или `AGENTS.md`, AIR может использовать их как вход резолюции, но не должен повторно отправлять то же содержимое в Delivery Payload. Изменение native source инвалидирует связанные решения. Детерминированный compiler не умеет удалить уже видимые модели native инструкции, если они конфликтуют; это `RUNTIME_GATE`/корректировка источника, а не операция фильтрации текста AIR.

## 3. Authoring/compilation boundary

### 3.1 Format Schema, Vocabulary, Policy, Rule

AIR поставляет форматные определения `air.vocabulary/v1` и `air.policy/v1` (например, JSON Schema и фиксированные семантические проверки). В authored файлах поле `format` **ссылается** на эту схему, но не определяет её:

```yaml
format: air.vocabulary/v1
namespace: example
version: 1
operations:
  probe.execute:
    description: Execute a configured probe to collect reachability evidence.
    parameters:
      strategy:
        type: identifier
        description: Selected probe strategy identifier.
```

```yaml
format: air.policy/v1
uses: [example@1]
rules:
  - key: probe.strategy_required # optional
    modality: require
    operation: example.probe.execute
    parameters:
      strategy:
        exists: true
    description: A probe must identify its strategy.
```

Это **иллюстрация рабочей грамматики**, не утверждённый formal schema file. До реализации schema нужно согласовать semantics полей `parameters`, `permit`, `applies_if` и нормализацию literals. Ошибочно принимать пример за готовый AST-контракт.

**Разделение:** Format Schema определяет допустимую структуру. Vocabulary свободно объявляет symbols/parameters/facts и их human-readable descriptions. Policy ссылается на symbols и задаёт нормативные Rules; Vocabulary не хранит обязанностей/запретов. `Rule` не объявляет Vocabulary inline.

### 3.2 Детерминированность

**Детерминированная область:** YAML/JSON parsing, Format Schema validation, namespace lookup, symbol/type checking, canonicalization, handles/hashes, `applies_if` как булево дерево над фактически доступными typed runtime facts, literal comparison, проверка полномочий по заранее утверждённому контракту, cache, assembly, trace.

**Недетерминированная область:** свободные поля `description` Vocabulary и Rule; семантическое сопоставление правил/описаний; выделение persistently effective user directives из разговорного текста. Дешёвая модель возвращает *ограниченный типизированный результат*, который AIR валидирует. Не может редактировать canonical texts, назначать authority, скрыто менять scope или invent new symbols.

Детерминированность структуры не даёт автоматической гарантии, что модель-исполнитель последует инструкциям. AIR измеряет delivery и compliance раздельно.

**Операции и факты:** синтаксис и регистрация символов детерминированы; содержимое vocabulary свободно расширяется и версионируется. Имя `test.run` существует только если оно зарегистрировано. Поля типов параметров проверяются по declaration словаря, а не угадываются AIR. Возможны extension vocabularies. Unresolved symbol → validation error, без автоматического создания словаря через LLM.

`modality`: рабочий словарь `require`, `forbid`, `permit`, `prefer` (смысл `permit` как исключения требует точной формализации). `applies_if` поддерживает декларативные `all/any/not` и типизированные сравнения с известными facts, но не исполняет алгоритмы. `description` — opaque natural language. Универсальные `subject`, `target`, BDD GIVEN/WHEN/THEN и обязательные ручные IDs отвергнуты; `key` опционален. Стабильный технический handle + отдельный content hash.

### 3.3 Policy Graph и fine-grained cache

Policy Graph — **производная структура памяти**, а не Neo4j или отдельный сервис. Узлы: Sources, Rules; рёбра: contains, equivalent, conflicts, refines, overrides с provenance. Не весь граф обязан быть DAG: циклы возможны у эквивалентности/конфликтов; запрет циклов применим только к будущим действительно зависимостным directed edge types, если они понадобятся. Стабильные идентификаторы Rules и hashes дают потенциальное переиспользование Conflict Decisions. Переносимость решения зависит от неизменности scope и релевантного контекста: нельзя считать пару hash полностью достаточной при появлении третьего правила.

## 4. Runtime flow

### 4.1 Initial session

```text
Selected Canonical Sources G/P/A
   → parse/validate + host facts
   → GPA fingerprint → GPA cache HIT/MISS
   → on MISS: deterministic candidate selection; cheap semantic resolver for unresolved relations
   → validated Resolution Overlay; conflict decision cache
   → Delivery Plan (native vs AIR per source/event)
   → Delivery Payload (лишь AIR-delivered, без повторения native bodies)
   → SessionStart hook [если разрешён экспериментом]
   → Codex model context + current user prompt
```

Результат в cache — inspectable resolved view + decisions; агенту-исполнителю доставляются конкретные инструкции, а не hashes/ссылки для дополнительного чтения.

### 4.2 Новый пользовательский turn

- Само текущее сообщение уже попадает Root как native `user` message.
- `UserPromptSubmit` *может* вызвать отдельный дешёвый extractor обновлений Session Directives и записать Session State без model injection. Это `RUNTIME_GATE`: dispatch, задержка, согласованность записи и recovery должны быть проверены.
- При необходимости `UserPromptSubmit` также может доставлять канонические краткие hot reminders из прежнего handoff; новый side-effect design конфликтует с ранее утверждённым обязательным hot path. **Решение по двум назначениям event не принято; тест должен измерить и предъявить конкретный вариант или `BLOCKED`.**
- Root видит новое указание через normal prompt. Прежние Session Directives остаются в истории до compaction; после compaction восстановление берёт актуальный Session State.

### 4.3 Compaction / resume

```text
SessionStart(source=compact)
   → перечитать применимые source fingerprints
   → GPA cache/recompute при изменениях
   → прочитать активный Session State
   → выяснить, что native Codex уже восстановил
   → построить Recovery Payload с нужными AIR-managed instructions и directives
   → inject full text (если лимиты позволяют) перед следующим model request
```

Не полагаться на наличие отметки `PostCompact` или прошлое успешное inject для пропуска force recovery. `PostCompact` может инвалидировать delivery generation, но не сам по себе доставлять payload. Переинъекция native sources запрещена, если Codex их уже реально сохранил. Если это неизвестно, такой путь не может быть объявлен надёжным.

### 4.4 Subagent

```text
Codex launches profile A → native developer_instructions (проверить)
   → SubagentStart (проверить actual event + role/scope metadata)
   → scoped GPA Resolution keyed by profile + project + global
   → relevant Session Directives
   → AIR Delivery Payload excluding native Agent Profile body
   → child receives tested model-visible context
```

Inherited Root context ≠ доказательство работы `SubagentStart`. Применимость ролей/поддерева должна подтверждаться runtime facts; неизвестный scope нельзя угадывать из `cwd` без дополнительного evidence.

### 4.5 Delegation приоритетов

Рабочий, ещё не экспериментально доказанный вариант:
- native Agent Profile self-delegates current user overrides внутри требований **этого профиля**; при необходимости адаптация старых профилей производится отдельной, подтверждённой миграцией;
- AIR Payload self-delegates current user overrides внутри **текста этого payload**;
- GPA конкуренция A/P/G уже разрешена до runtime.

Если это нарушается, fallback не состоит в более длинной декларации приоритетов: нужно выбирать другой transport/перенастраивать конфликтующие native sources, либо фиксировать `BLOCKED`.

## 5. Persistence, cache, trace

Разделение config/canonical sources и runtime state зафиксировано. Windows-кандидат после утверждения имени:

```text
~/.agents/policies.toml                  # selected sources; первоначальный config candidate
%LOCALAPPDATA%/AIR/
  cache/gpa/<fingerprint>/{resolution.json,effective.md}
  cache/conflicts/<fingerprint>.json
  sessions/<session-id>.json             # durable state на протяжении resumable session
  trace/policy-delivery.jsonl            # bounded, no raw bodies
```

Расположение `%LOCALAPPDATA%` архитектурно согласовано; точное имя root-dir и portable handling `PLUGIN_DATA` уточняются host contract. Atomic writes, simultaneous hook concurrency, dedup generation, file locks и recovery после partial write обязательны. Cache entries имеют origin hashes, vocabulary/schema/authority/resolver versions, scope и provenance; при ручных корректировках generated `effective.md` нельзя молча принять за canonical source: correction нужна в отдельном explicit override, привязанном к hash (формат открыт).

## 6. Package и host integration

Исследованный Agent Plugins стандарт использует корневой `plugin.json` (`$schema: https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`) и `extensions.com.openai` для OpenAI-specific hooks; поддерживается compatibility `.codex-plugin/plugin.json`. Однако **это спецификация упаковки, не runtime ABI политики AIR**. Приоритет: portable package layout с host-specific bindings на границе Codex Integration; отдельно проверять, что installed Desktop принимает именно этот вариант. Не добавлять MCP сервер без подтверждённой потребности.

## 7. Инварианты

1. Нет незаявленного read/glob произвольных repo docs и повышения project content в developer authority.
2. Один source может участвовать в resolution, но его body доставляет только один выбранный mechanism.
3. Cache hit ≠ доказательство наличия инструкции в model context; generation и compaction требуют отдельной логики.
4. Успешный hook return ≠ доказательство model-visible full delivery/поведения.
5. Структурная зона не содержит свободной неограниченной natural-language semantics; `description` является явной opaque зоной.
6. LLM никогда не пишет/меняет canonical source автоматически и не формирует новые vocabulary symbols.
7. У agent-исполнителя нет обязанности читать overlay/trace/исходники ради текущего исполнения; ему доставляется итоговый применимый текст.
8. Session State отделён от GPA cache и сохраняется при resumable session.
9. Отсутствие гарантированного host transport → доказательный blocker соответствующего acceptance, не `DONE`.
10. Изменения в действующей пользовательской `.agents` требуют permission preflight, резервной копии, проверяемого diff и rollback.

## 8. Открытые вопросы и владельцы решений

- **RUNTIME_GATE:** поддержка hooks в текущей Windows Desktop, full context/truncation, message precedence, native AGENTS/Agent Profile reloading, subagents, `UserPromptSubmit` side effect. Владелец: агент-исследователь, затем user approval при несовместимости.
- **SCHEMA_GATE:** точная grammar/types/`permit`/условия `unknown fact`, поддержка частично natural-language только в description, stable handles. Владелец: пользователь + архитектурный review по отчёту прототипа, без скрытых расширений.
- **TRANSPORT_GATE:** conflicting native higher authority и очистка global bootstrap. Владелец: пользователь после evidence.
- **UX_GATE:** формат ручных patches/corrections и их migration при изменении source hash. Владелец: пользователь после практического mockup.
- **ПЛАНИРУЕМОЕ РАСШИРЕНИЕ:** функциональность менеджмента skills в AIR. Состав функций и формат интеграции согласуются отдельно.

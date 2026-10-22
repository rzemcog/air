<!-- @style: ./air.css -->
<!-- @script: ./air.js -->

# AIR — ТЗ на реализацию (DRAFT; зависит от экспериментов и ADR)

**Статус:** НЕ исполняемое разрешение на production implementation · 2026-10-22. Подготовлено как карта следующей работы. Уточнение архитектуры идёт по [`05_EXPERIMENTAL_TZ_RU.md`](05_EXPERIMENTAL_TZ_RU.md). Пользователь отдельно согласует спорные пункты до принятия реализационных контрактов.

## 0. Цель будущей реализации

AIR должен обеспечивать source selection, разрешение конфликтов, детерминированную сборку model-visible инструкций, GPA/Conflict Decisions caches, долговечный Session State, recovery и host-specific delivery. Ядро и формат данных должны оставаться **harness-agnostic**. Первый Host Adapter предназначен для Codex Desktop Windows, после того как его возможности подтверждены экспериментами.

Предыдущая версия задания объединяла probe и код в одном потоке. По новому решению пользователя задачи разделены: **экспериментальное ТЗ исполняется для уточнения архитектуры, а этот draft фиксирует будущие acceptance и зависимости**. Разработчик не должен трактовать любой положительный R1–R9 как автоматическое согласие на окончательный Rule schema или изменение Shared Policy.

## 1. Зависимости реализации

<div class="air-visual" role="group" aria-label="Зависимости реализации AIR">
  <div class="air-v-heading"><strong>Карта зависимостей реализации</strong><span class="air-v-subtitle">DRAFT: реализовывать после согласования gates</span></div>
  <div class="air-dependencies">
    <div class="air-dep-pipeline">
      <div class="air-node air-node--host"><span class="air-tag air-tag--host">Host evidence</span><strong>Экспериментальное ТЗ (05)</strong><small>Host ABI, authority, native, compaction</small></div>
      <div class="air-arrow-down" aria-hidden="true">↓</div>
      <div class="air-node air-node--host"><strong>Host Adapter contract</strong><small>Lifecycle, facts, transport и права</small></div>
    </div>
    <div class="air-dep-pipeline">
      <div class="air-node"><span class="air-tag air-tag--pending">User approval</span><strong>Согласование Schema v1</strong><small>Спорная semantics остаётся открытой</small></div>
      <div class="air-arrow-down" aria-hidden="true">↓</div>
      <div class="air-node air-node--core"><strong>Policy / Vocabulary validation + IR</strong><small>Структурный язык и типизированные Rules</small></div>
    </div>
  </div>
  <div class="air-merge">
    <div class="air-node air-node--core"><strong>Детерминированный отбор кандидатов</strong><small>После валидированного Policy IR</small></div>
    <div class="air-arrow-down" aria-hidden="true">↓</div>
    <div class="air-node air-node--core"><strong>Cheap Semantic Resolver → Validated Decisions</strong><small>Семантическая часть по unresolved relations</small></div>
    <div class="air-arrow-down" aria-hidden="true">↓</div>
    <div class="air-node air-node--core"><strong>GPA Cache + Conflict Decision Cache</strong><small>Повторное использование с контролем изменившегося контекста</small></div>
  </div>
  <div class="air-merge"><div class="air-dep-bottom"><div class="air-node air-node--host"><strong>Host Adapter contract</strong><small>Вход в план доставки</small></div><div class="air-node"><strong>Session Directives extraction / State</strong><small>Директивы пользователя, отдельно от GPA</small></div></div><div class="air-arrow-down" aria-hidden="true">↓</div><div class="air-node air-node--core"><strong>Delivery Plan · Scoped Recovery</strong><small>Получает решение из Cache, факты Host Adapter и Session State.</small></div></div>
  <div class="air-arrow-down" aria-hidden="true">↓</div>
  <div class="air-dep-accept air-node air-node--good"><strong>E2E Acceptance</strong><small>Наблюдаемая доставка (model-visible) и compliance измеряются отдельно.</small></div>
  <div class="air-flow-caption">Любая блокирующая экспериментальная ветвь возвращается к экспериментам с новым узким вопросом; она не разрешает автоматически переписывать архитектуру.</div>
</div>

**Stop-gates:** Schema v1 отложена (значит нормализованное AST и `require`/`permit` semantics не утверждены); приоритеты/делегация на уровне модели, достоверность native recovery, синхронная latency resolver и `UserPromptSubmit` modes требуют экспериментов и/или отдельного ADR. Независимые технические spike/fixtures могут выполняться в experimental workspace, не становясь каноническим runtime.

## 2. Reuse-first и разделение работ

Перед собственной реализацией принять проверяемые решения по каждому компоненту в [`06_REUSE_MATRIX_RU.md`](06_REUSE_MATRIX_RU.md). Исследовательский reuse verdict фиксирует pinned commits, licenses, Windows behavior, тесты и стоимость адаптации. Роли будущих исполнителей: Host Integration, Policy Language/IR, Resolver/Caches, Session State, Independent E2E. Независимый reviewer сравнивает результат с реальным host, а не только с unit tests.

## 3. Rule/Vocabulary candidate (НЕ утверждённая Schema v1)

Schema Definitions в коде AIR; authored files используют `format`. Vocabulary freely declares namespaces, version, operation/fact symbols and typed params, human-readable `description` для каждого экспортируемого символа/параметра. Rule c `modality`, `operation`, `parameters?`, `applies_if?`, `description?`, `key?` (необязателен). `subject`, `target`, BDD и обязательные IDs не включать. Type universe минимален и versioned. Unknown symbols/type mismatch/duplicate namespaces/invalid predicates → deterministic validation error.

Semantic resolver только для unresolved natural-language relations. Он не может писать canonical sources, invent symbols, повышать authority и переписывать text вольно. Resolution Overlay internal; assembler выдаёт человеку проверяемый `effective.md`, а модели только реальный scoped Delivery Payload. Manual correction должна быть inspectable/explicit, не скрытое изменение cache.

**Open schema cases** (`permit` vs `forbid`, missing runtime fact, параметры под оператором, условная семантика) требуют до финального acceptance отдельного мини-RFC с 2–3 конфликтными примерами и user consent. На этот счёт нет разрешения придумывать ограничения от себя только ради прохождения тестов.

## 4. Storage, performance, security: проектные требования

Authored source/config в доверенном указанном пути (candidate `~/.agents/policies.toml`), runtime data в `%LOCALAPPDATA%/AIR` либо `PLUGIN_DATA` при доказанном host контракте. `cache/gpa`, `cache/conflicts`, `sessions`, `trace`. `sessions` не удаляется при cache eviction. File locking/atomic writes + checksum + generation + bounded trace + privacy and safe path resolution. No network/telemetry кроме отдельно разрешённого API запроса выбранного cheap resolver; не хранить raw user prompt в trace.

Измерять: hook median/p95 latency на небольшой тестовой выборке, invocation counts, output bytes/tokens, injected scopes, cache hit ratio, resolver calls, model-visible canary completeness и task compliance отдельно. Performance threshold не изобретать без baseline; дать сравнительные числа и предложить bounded budgets.

## 5. Целевые Acceptance Criteria (DRAFT)

| AC | Обязательный результат | Минимальное доказательство | Блокирующая развилка |
|---|---|---|---|
| **AC01** | Парсер двух versioned formats, Rule IR, свободные vocabularies с namespace/description и строгой ссылочной проверкой | Unit fixtures позитив/негатив; unknown operation → отказ, не LLM; сохранившийся исходный текст | H22 |
| **AC02** | Декларативное `applies_if`, source scope, typed facts; policy/skill boundary | Таблица truth tables, nested all/any/not, отсутствие runtime fact и invalid input | H19/H22 |
| **AC03** | Semantic resolver с typed output и подтверждаемым authority decision; нет переписывания canonical sources | Recorded requests/responses на синтетических документах + test rejected invalid handle; blocked branch при undecidable safety semantics | H9/H10/H20 |
| **AC04** | GPA Cache и Conflict Decision Cache, точная инвалидация; user directives хранятся вне GPA | Cache HIT/MISS, mutation third-rule and scope, file corruption, restart | H17–H19/H23 |
| **AC05** | Настоящий Codex Desktop доставляет managed rules и подтверждён canary в следующем model call | Host exact version; hook receipts + независимый transcript canary | H1–H5 |
| **AC06** | Compaction/resume корректно восстанавливают содержимое и состояние | force compact + middle/end canaries, no native-body duplicate, generation trace | H5–H7 |
| **AC07** | Child получает только применимые правила, Current User не теряется | custom subagent transcript, role/path proofs; native Agent Profile не повторён | H11/H12 |
| **AC08** | User Directives add/revoke/supersede, no double processing; hot mode не конфликтует | Synthetic prompts, same event replay, direct user priority matrix, event timing | H8/H9/H13–H16 |
| **AC09** | Secure install/rollback, trace/privacy, Windows runtime | Isolated before/after diff, disabled behavior, path/symlink/UTF-8 tests, no plaintext secrets | H21/H24 |
| **AC10** | Воспроизводимая сборка, reuse/license provenance, полный отчёт по blockers | pinned revisions, tests with exact outputs, reviewer report, clean Git diff | Все |

**Full `DONE`:** выполнены AC01–AC10, критичные host gates доказаны на целевой Windows Codex Desktop. Иначе `PARTIAL` по реально законченным AC + `BLOCKED_*` по зависимым. Не переименовывать блокирующую ветку в успех только потому, что тестовый CLI или unit fixture прошёл.

### Соглашения о точности

- Отчёт разделяет `IMPLEMENTED`, `UNIT_TESTED`, `HOST_HOOK_DISPATCHED`, `MODEL_VISIBLE`, `BEHAVIOR_OBSERVED`, `ACCEPTED`.
- `model-visible` проверяется независимой наблюдаемой реакцией на canary; это эмпирический proxy, а не доступ к скрытому точному model context.
- Resolver не назначает новый authority, не добавляет symbols, не пишет канонические политики; malformed response не попадает в Delivery Payload.
- Для недоступных runtime facts не предполагать `false` без согласования семантики unknown; `permit` пока отдельный schema gate.
- Для риска third-rule/cross-vocabulary coverage агент документирует false negatives на наборе контрпримеров до объявления semantic coverage достаточным.

**Примечание к AC01/AC02/AC03:** это проектируемые критерии, а не разрешение сейчас выбрать спорную semantics или считать один YAML-пример нормативным. Статус `DONE` применим только после отдельного утверждения и измеримых E2E результатов.

## 6. Проектируемые проверки

**Unit:** schema/vocab/type checks; `applies_if` all/any/not; deterministic source selection / native source exclusion; fingerprint+cache+invalidations; Conflict Decision reuse; Session Directive add/supersede/revoke; corruption/concurrency; Windows path/symlink/scope; trace privacy.

**Integration:** real plugin package install/trust, lifecycle hook fixtures/actual Desktop event receipts, canary delivery startup/compact/subagent, direct user override, no duplicate `AGENTS.md`/Agent Profile, updated policy after on-disk change, hot reminder bounded behavior, disabled rollback.

**E2E mandatory:** next model request sees actual current recovery instructions; custom child sees scoped policies and surviving directives; distinction delivered/complied; exactly tested version named; source/agent/user authority deviations reported; session continuity after compaction/resume. A component may be accepted independently despite another BLOCKED branch; full system `DONE` only when all agreed critical invariants are met.

## 7. Ожидаемые артефакты реализации

Provide source tree, pinned dependencies, tests/scripts, minimal synthetic test workspace, machine-readable schema + sample vocab/policies, `REUSE_DECISION.md`, `HOST_PROBES.md` (version, stdout receipts, screenshots/traces if relevant), `DELIVERY_MATRIX.md`, explicit `BLOCKERS.md`, migration diffs к согласованным sources/profiles/bootstrap (без изменения Shared Policy на текущем шаге), `ROLLBACK.md`, cache sample, policy trace sample redacted. No surprises hidden in global user state. Report `DONE/PARTIAL/BLOCKED` criterion by criterion; include commands/evidence and failures. If blocked, continue all independent implementation rather than looping on one hook.

Из списка миграций исключена автоматическая правка `agent-policy.md`: текущий пользователь её отложил. Действующий адаптированный skill находится в [`skills/instruction-conflict-resolution`](../skills/instruction-conflict-resolution/SKILL.md) и подлежит integration tests; остальные migrations требуют одобрения и rollback.

## 8. План реализации ПОСЛЕ архитектурных решений

1. `git status`, создать implementation branch, snapshot доступных native files/agent profiles и список plugin registrations **read-only**. Узнать реальный `CODEX_HOME`, installed Desktop build, runtime/trust без предположения о пользовательских путях из старых материалов.
2. Root назначает Host Probe, Reuse, Policy IR, Resolver/State, Independent E2E, с отдельными файлами/ветками и фиксированными acceptance. Child Host Probe не меняет общий config. На запись в глобальную конфигурацию один владелец.
3. Зафиксировать минимальные воспроизводимые эксперименты `R1`/`R2` в изолированной папке. Одновременно Policy IR child создаёт parser/schema fixtures и test cases для всех договорённых структур, **не выбирая за пользователя OPEN semantics**.
4. Проверить `codex-rules` и Agent Plugins по pinned revision; запустить их релевантные тесты только в песочнице. Если готовый компонент проходит AC без нарушений scope/trust, адаптировать. Иначе обосновать минимальный собственный модуль.
5. На первом подтверждённом hook event внедрить простой canary payload + receipt, E2E model-visible proof; затем подключить managed source allowlist, compaction и scoped child. Продолжать parser/state независимо от host blocker.
6. Resolver соединять после валидированного IR и сформированной таблицы structural conflicts. Вести честный semantic candidate recall тест: идентичные symbols, aliases разных vocabularies, пересекающиеся scopes, третье Rule, совместимые/несовместимые descriptions.
7. При обнаружении нового архитектурного решения вне карты: сформировать короткий decision request из двух вариантов, tradeoffs и блокируемого AC; не переписывать концептуальные ADR без согласования. Сохранить все независимые готовые изменения и тесты.

Эта последовательность становится исполняемым планом только после согласования архитектурных gates. Пока приоритет имеет экспериментальное задание, а не скрытое начало реализации.

## 9. Условия перехода DRAFT → APPROVED

1. Результаты R1–R9 и H1–H24 рассмотрены, утверждён transport/delivery authority contract.
2. Schema v1 (`parameters`, `permit`, `applies_if`, literals, unknown facts, `require`) согласована отдельно.
3. Режим `UserPromptSubmit`, правила resolver timeout и cache miss выбраны по evidence.
4. Для всех критических gates отмечен `ACCEPTED` либо сохранён локальный `BLOCKED_*`.
5. Утверждены перечень мигрируемых native sources и политика доступа к live файлам.

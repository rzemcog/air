# AIR — единое ТЗ агенту: исследования, эксперименты и реализация в одном процессе

**Статус:** исполняемое задание на первую реализацию, основанное на достигнутом консенсусе. Windows Desktop эксперименты AIR пока не запускались.  
**Требование пользователя:** никакого искусственного разделения на «исследовательскую» и «реализационную» фазы с новым handoff. Агент исследует ровно нужное, проверяет на работающем Desktop, выбирает **заранее перечисленную ветку** и реализует подтверждённое. При истинном blocker не выдумывает новую архитектуру.

## 0. Цель и условия выполнения

**Запуск агента:** открыть этот репозиторий как основной working directory, прочитать `README.md`, затем указанные ниже документы. Сразу создать отдельную Git-ветку реализации (`feat/air-runtime`) и чистые независимые worktrees для назначенных child-задач. Не переписывать существующую историю, не работать в пользовательских production-projects. Не тратить время на создание нового handoff вместо выполнения экспериментов и кода.

**Цикл исполнения в одной задаче:** гипотеза → минимальный эксперимент с независимой проверкой → наблюдение с доказательствами → обновление решения по IF/THEN → реализация разрешённого пути → регрессионный тест → следующая гипотеза. Для каждого event/gate завести журнал `docs/EXPERIMENT_RESULTS.md` (таблица с ID, tested build, workspace, commands, expected/observed, trace refs, branch, status). Проверки и реализация ведутся вместе, а не двумя отдельными заданиями.

Создать первую working version **AIR / Agent Instruction Runtime** для Codex Desktop на Windows: структурированные политики и свободные versioned vocabularies; GPA resolution с отдельной дешёвой моделью, inspectable results, два уровня cache; Session Directives state; доставку, compaction recovery и scoped child, точный trace; совместимость с native instructions и возможностью rollback. Выделить надёжно проверяемый функционал и честно зафиксировать неподдерживаемые ветви.

Работать в изолированном workspace. Изменения действующих конфигураций Windows, Codex и профилей агентов выполнять после permission preflight, снимка исходного состояния и согласования области записи. Использовать синтетический workspace: тестировать инструкции на реальном Codex Desktop без запуска или изменения прежних пользовательских проектов. Использовать имеющиеся hooks, доступного провайдера resolver и локальное файловое хранение. Материалы raw evidence открывать только при доказанной необходимости.

Root действует как integrator. При наличии субагентов выделить **независимые outputs и ownership**:
1. `Host & Runtime`: Codex versions, trust/hooks, message contracts, Desktop probes; read-only и isolated workspace.
2. `Reuse & Licenses`: минимальные исходники codex-rules/subpath/caveman/Agent Plugins; матрица fork/adapt/reference с commits/licenses.
3. `Policy Language`: JSON Schema/vocabulary validation, IR, typed predicate logic; автономные fixtures/tests без изменения глобальной конфигурации.
4. `Resolver & State`: cheap model integration, decision caches, session state, fault/atomicity tests в отдельной области файлов.
5. `E2E & Independent Review`: независимое evidence для model-visible source/authority/compaction/subagent; не полагаться на сообщения автора реализации.

Если платформа не позволяет субагентов, Root фиксирует это и последовательно выполняет задачи. Один writer для глобального config/plugin trust; не параллелить мутации одних файлов.

## 1. Входы и порядок чтения

Сначала прочитать `docs/01_ARCHITECTURE_RU.md`, `docs/07_GLOSSARY_RU.md`, `docs/02_ADR_RU.md`, `docs/03_USE_CASES_RU.md`, `docs/04_EVIDENCE_CHAINS_RU.md`, `docs/08_CONSENSUS_CONFIDENCE_RU.md`, `docs/06_REUSE_MATRIX_RU.md` и этот ТЗ. Исторические наблюдения консолидированы в `docs/04_EVIDENCE_CHAINS_RU.md`; старые первичные журналы остаются в исходном пользовательском handoff и в рабочий репозиторий AIR не включены. Открывать исходный архив только по спорному конкретному факту.

Перед значительным кодом: inspect live `~/.agents/AGENTS.md → ENTRYPOINT.md → shared`, actual Codex home/config/trust, real installed version, existing plugin registration; snapshot affected files. Не переносить historical snapshots на ПК как будто они live. Сравнить новую семантику с текущим attached `agent-policy` и конфликтным skill: изменения разрешены пользователем, но только controlled migration diff.

## 2. Reuse gate (до написания собственного аналога)

Для каждого компонента из `docs/06_REUSE_MATRIX_RU.md`: проверить license, pinned commit, API compatibility, tests, Windows behavior, объём адаптации. Ожидаемые кандидаты:
- `code-yeongyu/codex-rules`: hook plumbing, cache/session generation, dedup/trace, packaging, tests. Отключить broad discovery и auto-loading всех `AGENTS.md`/CLAUDE/etc.
- `Diluka/codex-subpath-agentsmd-hooks`: Windows PowerShell/path/cwd/worktree/scope, reference only, НЕ параллельно установленный runtime.
- `JuliusBrussee/caveman`: reminder/recovery pattern, reference only.
- Agent Plugins manifest: portable `plugin.json` + Codex extension hooks, определить installed-version compatibility.
- Ajv/JSON Schema: validation; JsonLogic or tiny subset for declarative applicability; OPA/Cedar/Casbin only conceptual comparison, не добавлять большие policy engines ради AIR v1.

Сделать `REUSE_DECISION.md`: adopted verbatim/adapted/reference/rejected with evidence, license path и commit. Если код реально заимствован, сохранить LICENSE/NOTICE, attribution.

## 3. Runtime preflight и эксперименты (по ходу реализации)

**Минимальный формат свидетельства:** для каждого `R*` иметь `hypothesis`, `setup + isolated scope`, `expected`, `raw receipt reference`, `model-visible/behavior observation where applicable`, `verdict`, `next IF/THEN branch`. Не писать «успешно», если имеется только stdout hook. Для поведенческих тестов использовать минимум два противоположных canary и повторения на свежих isolated sessions; агент фиксирует число прогонов и текстовые результаты без хранения приватных пользовательских prompts.

Временный isolated workspace с синтетическими `AGENTS.md`, Agent Profiles, tiny hook handler; уникальные canary и отдельный тестовый `CODEX_HOME` там, где реально поддерживается. Не подменять desktop проверку CLI. Проверить непосредственно в установленной Desktop:

**R1 Hook dispatch.** `SessionStart(startup,resume,compact)`, `UserPromptSubmit`, `SubagentStart`, `PostCompact`, optional `PostToolUse`: запись receipt → проверка model-visible canary. Контрольный CLI probe при отказе Desktop. Проверить trust/enabled/duplicate hook registrations и Windows invocation (Node direct vs `.cmd`/PowerShell), stdout JSON UTF-8, concurrency.

**R2 Message authority.** Контролируемые конфликтные тесты (native Project vs user, custom Agent Profile vs user, developer `additionalContext` vs user, developer self-delegation within Agent Profile and within hook payload). Проверять фактическое поведение и доступные role/order traces; менять формулировку/полярность и повторять. Факта hook invocation недостаточно.

**R3 Native reload.** В тестовом репозитории `AGENTS.md` A→B→removed и custom `developer_instructions` профиль A→B; проверять до/после compaction, startup/resume и child. Фиксировать, что реально повторно загрузилось и где.

**R4 Compaction recovery.** `SessionStart(source=compact)` получен, injector доставил актуальный полный payload до следующего model call, включая middle/end canary после лимитов. Если compaction нельзя вызвать безопасно, фиксировать непроверенность; не создавать многочасовые шумовые транскрипты.

**R5 Child scoping.** Real custom subagent with role, project path, task context; verify agent_type/task_name/cwd metadata; isolation native vs AIR; relevant Session Directives; отсутствие дублирования Role Profile и чужих scoped policies.

**R6 UserPromptSubmit modes.** A: side-effect-only update Session State при новой persistent directive, без model output; B: short hot canonical excerpt, сохранение фокуса; C: совместный bounded handler, со временем исполнения и доказательством порядка. Внутри одного длинного turn этот hook не срабатывает повторно. Проверить, кто фактически вызывает cheap model/API и доступен ли он в sync hook.

**R7 Limits and failure.** Проверить default `additionalContextLimit`, override (bounded), spill/truncation, latency/timeouts, invalid JSON, permission-denied source, symlink escaping, missing required file, cache corruption, crash during atomic write, restoration after disable.

## 4. Детерминированная карта IF → THEN (обязательная)

Каждая строка задаёт ветку реализации/законный локальный blocker. Если ситуация не покрыта картой и её решение меняет архитектуру/authority/security, спросить пользователя; не вводить новый transport через самодеятельность.

| Условие | Обязательное действие | Локальный статус |
|---|---|---|
| H1. Desktop доверяет hook и фактически dispatch-ит его | Использовать проверенный native hook transport для соответствующего event | PROCEED |
| H2. Desktop не dispatch-ит hook, CLI работает | Проверить trust/registration/интерпретатор один раз, собрать evidence; реализовать host-independent core, Desktop-dependent delivery не объявлять DONE | BLOCKED_DESKTOP_HOOK |
| H3. Hook отсутствует и в CLI/installed runtime | Использовать только подтверждённые native механизмы для независимых задач; не создавать ACP/MCP/daemon как обход | BLOCKED_EVENT_CONTRACT |
| H4. Hook возвращает корректный JSON, но model-visible canary отсутствует | Путь доставки считать неподтверждённым; тестовый transcript + handler receipt; не принимать AC delivery | BLOCKED_VISIBILITY |
| H5. `additionalContext` усечён/спилится | Установить bounded limit, повторить full-text proof; если не удаётся — mandatory recovery BLOCKED, никогда не считать preview полным | BLOCKED_FULL_RECOVERY |
| H6. Native AGENTS/Profile после compaction реально восстановлены | Не повторять native source bodies в Recovery Payload | PROCEED_NATIVE |
| H7. Native source после compaction НЕ восстановлен и безопасный способ повторной доставки подтверждён | Использовать точечный AIR recovery для этого источника только если не повышает untrusted authority; иначе BLOCKED | CONDITIONAL_RECOVERY |
| H8. Developer self-delegation user override работает в повторённых тестах | Встроить scoped delegation preamble в ТОЛЬКО тестовые/мигрируемые профили после backup; не выдавать вероятностный успех за гарантию | PROCEED_DELEGATION_TESTED |
| H9. Developer self-delegation конфликтует с другими developer instructions или непредсказуема | Не заявлять `User > Agent` как выполненный контракт; сохранить native профиль, зафиксировать конфликт и обратиться к пользователю | BLOCKED_AUTHORITY |
| H10. Air payload конфликтует с неизменяемым native source | Не пытаться скрыть его из hook bundle; предложить минимальную миграцию canonical source с diff/approval | BLOCKED_NATIVE_CONFLICT |
| H11. `SubagentStart` + scope metadata подтверждены | Scoped payload с исключением native Agent Profile и неприменимых Root policies | PROCEED_CHILD |
| H12. `SubagentStart` не вызывается или недостаточно role facts | Не угадывать child role, не заявлять scoped inheritance; независимые components продолжают | BLOCKED_CHILD |
| H13. `UserPromptSubmit` side-effect-only надёжен и extra resolver допустим | Persist Session State без user prompt re-injection, атомарно, idempotent per turn | PROCEED_DIRECTIVES |
| H14. Extractor недоступен/дорог в synchronous hook | Не блокировать каждый запрос скрытым сетевым вызовом; сохранить core/delivery, предложить bounded alternative на согласование | BLOCKED_DIRECTIVES |
| H15. Hot excerpt и directives extraction совместимы | Реализовать оба по отдельным budget/dedup controls, не inject full policy на каждый prompt | PROCEED_HOT |
| H16. Они вызывают двойное чтение, нарушения authority/latency | Остановить только contested user-prompt branch, предоставить сравнительные evidence и запросить выбор | BLOCKED_USER_PROMPT_DESIGN |
| H17. Все source hashes и context одинаковые; валидный cache entry | Не вызывать LLM, reuse GPA/cache decision | CACHE_HIT |
| H18. Изменился один Rule, прочие стабильны | Инвалидировать affected edges; старые conflict decisions переиспользовать только при доказанной context equivalence | PARTIAL_RECOMPILE |
| H19. Changed fact/authority/schema/vocabulary/resolver behavior | Инвалидировать весь затронутый cache; не применять старые конфликты без проверки scope | RECOMPILE |
| H20. LLM resolver вернул invalid/schema-invalid/несуществующие handles | Rejection; не публиковать новый resolved bundle, сохранить проверенный LKG только при неизменных входах, сообщить статус | BLOCKED_RESOLUTION |
| H21. Required source отсутствует / untrusted path | Не inject неполный mandatory bundle как полный; лог + bounded recovery from verified LKG при допустимой политике, иначе blocker | BLOCKED_REQUIRED_SOURCE |
| H22. JSON Schema/vocab или Rule grammar нерешённая существенная неоднозначность | Реализовать parser/test fixtures, совместимые с согласованной семантикой; спорную семантическую ветку представить пользователю без автоподмены | BLOCKED_SCHEMA_BRANCH |
| H23. Cache повреждён, sources доступны | Перекомпилировать; recovery/session state не удалять как cache; atomic replace | PROCEED_REBUILD |
| H24. Plugin disabled/rollback | Поведение старого bootstrap и config возвращено, никаких orphan hooks и скрытых файлов | PASS_ROLLBACK |

**Нет глобального `BLOCKED`, если независимые разрешённые задачи ещё возможны**. `DONE` только при фактически проверенных обязательных AC; иначе `PARTIAL` + точные blockers.

## 5. Первый рабочий Rule/Vocabulary contract

Schema Definitions в коде AIR; authored files используют `format`. Vocabulary freely declares namespaces, version, operation/fact symbols and typed params, human-readable `description` для каждого экспортируемого символа/параметра. Rule c `modality`, `operation`, `parameters?`, `applies_if?`, `description?`, `key?` (необязателен). `subject`, `target`, BDD и обязательные IDs не включать. Type universe минимален и versioned. Unknown symbols/type mismatch/duplicate namespaces/invalid predicates → deterministic validation error.

Semantic resolver только для unresolved natural-language relations. Он не может писать canonical sources, invent symbols, повышать authority и переписывать text вольно. Resolution Overlay internal; assembler выдаёт человеку проверяемый `effective.md`, а модели только реальный scoped Delivery Payload. Manual correction должна быть inspectable/explicit, не скрытое изменение cache.

**Open schema cases** (`permit` vs `forbid`, missing runtime fact, параметры под оператором, условная семантика) требуют до финального acceptance отдельного мини-RFC с 2–3 конфликтными примерами и user consent. На этот счёт нет разрешения придумывать ограничения от себя только ради прохождения тестов.

## 6. Storage, performance, security

Authored source/config в доверенном указанном пути (candidate `~/.agents/policies.toml`), runtime data в `%LOCALAPPDATA%/AIR` либо `PLUGIN_DATA` при доказанном host контракте. `cache/gpa`, `cache/conflicts`, `sessions`, `trace`. `sessions` не удаляется при cache eviction. File locking/atomic writes + checksum + generation + bounded trace + privacy and safe path resolution. No network/telemetry кроме отдельно разрешённого API запроса выбранного cheap resolver; не хранить raw user prompt в trace.

Измерять: hook median/p95 latency на небольшой тестовой выборке, invocation counts, output bytes/tokens, injected scopes, cache hit ratio, resolver calls, model-visible canary completeness и task compliance отдельно. Performance threshold не изобретать без baseline; дать сравнительные числа и предложить bounded budgets.

## 7. Acceptance Criteria и проверка инвариантов

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

## 8. Критерии приёмки

**Unit:** schema/vocab/type checks; `applies_if` all/any/not; deterministic source selection / native source exclusion; fingerprint+cache+invalidations; Conflict Decision reuse; Session Directive add/supersede/revoke; corruption/concurrency; Windows path/symlink/scope; trace privacy.

**Integration:** real plugin package install/trust, lifecycle hook fixtures/actual Desktop event receipts, canary delivery startup/compact/subagent, direct user override, no duplicate `AGENTS.md`/Agent Profile, updated policy after on-disk change, hot reminder bounded behavior, disabled rollback.

**E2E mandatory:** next model request sees actual current recovery instructions; custom child sees scoped policies and surviving directives; distinction delivered/complied; exactly tested version named; source/agent/user authority deviations reported; session continuity after compaction/resume. A component may be accepted independently despite another BLOCKED branch; full system `DONE` only when all agreed critical invariants are met.

## 9. Deliverables

Provide source tree, pinned dependencies, tests/scripts, minimal synthetic test workspace, machine-readable schema + sample vocab/policies, `REUSE_DECISION.md`, `HOST_PROBES.md` (version, stdout receipts, screenshots/traces if relevant), `DELIVERY_MATRIX.md`, explicit `BLOCKERS.md`, migration diffs to `agent-policy`/skill/profiles/bootstrap, `ROLLBACK.md`, cache sample, policy trace sample redacted. No surprises hidden in global user state. Report `DONE/PARTIAL/BLOCKED` criterion by criterion; include commands/evidence and failures. If blocked, continue all independent implementation rather than looping on one hook.


## 10. Конкретный стартовый план (первые безопасные изменения)

1. `git status`, создать implementation branch, snapshot доступных native files/agent profiles и список plugin registrations **read-only**. Узнать реальный `CODEX_HOME`, installed Desktop build, runtime/trust без предположения о пользовательских путях из старых материалов.
2. Root назначает Host Probe, Reuse, Policy IR, Resolver/State, Independent E2E, с отдельными файлами/ветками и фиксированными acceptance. Child Host Probe не меняет общий config. На запись в глобальную конфигурацию один владелец.
3. Зафиксировать минимальные воспроизводимые эксперименты `R1`/`R2` в изолированной папке. Одновременно Policy IR child создаёт parser/schema fixtures и test cases для всех договорённых структур, **не выбирая за пользователя OPEN semantics**.
4. Проверить `codex-rules` и Agent Plugins по pinned revision; запустить их релевантные тесты только в песочнице. Если готовый компонент проходит AC без нарушений scope/trust, адаптировать. Иначе обосновать минимальный собственный модуль.
5. На первом подтверждённом hook event внедрить простой canary payload + receipt, E2E model-visible proof; затем подключить managed source allowlist, compaction и scoped child. Продолжать parser/state независимо от host blocker.
6. Resolver соединять после валидированного IR и сформированной таблицы structural conflicts. Вести честный semantic candidate recall тест: идентичные symbols, aliases разных vocabularies, пересекающиеся scopes, третье Rule, совместимые/несовместимые descriptions.
7. При обнаружении нового архитектурного решения вне карты: сформировать короткий decision request из двух вариантов, tradeoffs и блокируемого AC; не переписывать концептуальные ADR без согласования. Сохранить все независимые готовые изменения и тесты.

## 11. Контроль handoff для следующего продолжения

Не создавать ещё один sprawling архив. Обновить только `docs/EXPERIMENT_RESULTS.md`, тестовые fixtures, `README.md` и `docs/02_ADR_RU.md` при принятом решении. Если блокер: оставить воспроизводимые setup, expected/observed, diff, узкий следующий эксперимент. Данные raw logs вне Git и без персональных секретов.

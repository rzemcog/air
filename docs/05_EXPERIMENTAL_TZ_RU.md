<!-- @style: ./.mdstyled/air.css -->
<!-- @script: ./.mdstyled/air.js -->
<!-- @page: air-docs -->

# AIR — экспериментальное ТЗ для уточнения архитектуры

**Статус:** CURRENT EXPERIMENT PLAN · 2026-10-22. Исполнитель проверяет host contracts и возвращает проверяемые результаты и варианты решений. **Не является разрешением на полноценную реализацию AIR.**

## 0. Цель и границы

Выяснить фактические свойства целевого Codex Desktop на Windows, которые блокируют архитектурные решения AIR: hook dispatch, delivery/authority, compaction, native sources, custom agents, scope и latency. Исследования проводятся в отдельном тестовом workspace. **Schema v1 (`parameters`, `permit`, `applies_if`, missing facts, literal normalization) не утверждается и не реализуется как нормативный контракт.** Shared Policy не изменяется.

Результат экспериментов: `docs/EXPERIMENT_RESULTS.md`, `docs/DELIVERY_MATRIX.md`, `docs/BLOCKERS.md`, артефакты минимальных synthetic fixtures и предложения ADR с пометками `PROPOSED`, а не автоматические изменения основного дизайна.

### Как проводить работу

Root отвечает за интеграцию evidence. При наличии субагентов делегировать независимо:

1. **Host Contract**: version, installation, trust, hook ABI, stdout/message roles; только изолированные настройки.
2. **Native/Authority**: native sources, profile vs user, delegated precedence, compaction и scope, без изменения живых профилей.
3. **Runtime/State**: `UserPromptSubmit`, resume/compact, latency, file races, отсутствие данных и test harness.
4. **Reuse Research**: pinned репозитории + licenses + proof of usable components; без копирования непроверенных аналогов.
5. **Independent Evidence Reviewer**: воспроизведение receipts и canary в новых сессиях, фиксация отрицательных исходов.

На запись в один общий config назначить одного владельца. Если в host нет субагентов, выполнить последовательными независимыми проверками и указать ограничение. Перед изменением пользовательского runtime или конфигурации нужно разрешение, backup и rollback. Успешный `hook exit 0` доказывает только выполнение hook, не visibility и не compliance.

### Схема доказательного цикла

<div class="air-visual" data-air-filterable="true" data-air-active-path="all" role="group" aria-label="Цикл архитектурного эксперимента">
  <div class="air-v-heading"><strong>Исследовательский цикл</strong><span class="air-v-subtitle">Evidence first · никаких автоматических архитектурных решений</span></div>
  <div class="air-dependencies">
    <div class="air-node air-node--core"><span class="air-step-number">01</span><strong>Гипотеза и проверяемый контракт</strong><small>Что наблюдение должно подтвердить или опровергнуть?</small></div>
    <div class="air-node"><span class="air-step-number">02</span><strong>Минимальный воспроизводимый probe</strong><small>Изолированная среда, версия host, test fixture.</small></div>
  </div>
  <div class="air-arrow-down" aria-hidden="true">↓</div>
  <div class="air-entry air-node"><span class="air-step-number">03</span><strong>Наблюдение и свидетельства</strong><small>Receipts, traces, версии и отдельно model-visible/behavior evidence.</small></div>
  <div class="air-checkpoint">Вердикт по исходной гипотезе</div>
  <div class="air-flow-tools" hidden role="group" aria-label="Подсветить вердикт"><button type="button" data-air-filter="all">Все исходы</button><button type="button" data-air-filter="confirmed">Подтверждено</button><button type="button" data-air-filter="refuted">Опровергнуто</button><button type="button" data-air-filter="unknown">Данных мало</button></div>
  <div class="air-experiment-paths">
    <section class="air-path" data-air-path="confirmed"><header>Подтверждено</header><div class="air-path-inner"><div class="air-node air-node--good"><strong>Зафиксировать capability</strong><small>Или строго ограниченный подтверждённый вариант.</small></div><small>↓ Предложение для ADR и Draft ТЗ</small></div></section>
    <section class="air-path" data-air-path="refuted"><header>Опровергнуто</header><div class="air-path-inner"><div class="air-node air-node--bad"><strong>Контрпример и локальный blocker</strong><small>Не переименовывать неудачу в успех.</small></div><small>↓ Предложение для ADR и Draft ТЗ</small></div></section>
    <section class="air-path" data-air-path="unknown"><header>Недостаточно данных</header><div class="air-path-inner"><div class="air-node"><strong>Новый узкий probe</strong><small>Уточнить наблюдаемое различие; сформулировать новую гипотезу.</small></div><small>↩ Возврат к пункту 01</small></div></section>
  </div>
  <div class="air-merge"><div class="air-node air-node--core"><span class="air-step-number">04</span><strong>Предложение к ADR → согласование пользователя</strong><small>Подтверждённый либо опровергнутый исход оформляется как вариант архитектурного решения, но не утверждается автоматически.</small></div></div>
</div>

Исследование заканчивается доказанным результатом или обоснованным blocker; оно не превращается автоматически в разработку production runtime.

## 1. Пререквизиты и учёт источников

Прочитать [`01_ARCHITECTURE_RU.md`](01_ARCHITECTURE_RU.md), [`02_ADR_RU.md`](02_ADR_RU.md), [`03_USE_CASES_RU.md`](03_USE_CASES_RU.md), [`04_EVIDENCE_CHAINS_RU.md`](04_EVIDENCE_CHAINS_RU.md), [`06_REUSE_MATRIX_RU.md`](06_REUSE_MATRIX_RU.md), [`07_GLOSSARY_RU.md`](07_GLOSSARY_RU.md) и [`08_CONSENSUS_CONFIDENCE_RU.md`](08_CONSENSUS_CONFIDENCE_RU.md). Сверить установленный host runtime, trust, действующие native sources и версию plugin loader; исторические пути из handoff не считать текущей конфигурацией.

Для каждого теста записать `ID`, `tested version/build`, `hypothesis`, `setup`, `expected`, `observed`, `receipt`, `model-visible evidence`, `analysis`, `next hypothesis/decision`, `verdict`, `blocker`, `cleanup`. Первичные private/raw transcripts не коммитить. Если можно безопасно получить только частичное свидетельство, обозначить его уровень явно.

## 2. Проверка повторного использования до проектирования реализации

Для каждого компонента из `docs/06_REUSE_MATRIX_RU.md`: проверить license, pinned commit, API compatibility, tests, Windows behavior, объём адаптации. Ожидаемые кандидаты:
- `code-yeongyu/codex-rules`: hook plumbing, cache/session generation, dedup/trace, packaging, tests. Отключить broad discovery и auto-loading всех `AGENTS.md`/CLAUDE/etc.
- `Diluka/codex-subpath-agentsmd-hooks`: Windows PowerShell/path/cwd/worktree/scope, reference only, НЕ параллельно установленный runtime.
- `JuliusBrussee/caveman`: reminder/recovery pattern, reference only.
- Agent Plugins manifest: portable `plugin.json` + Codex extension hooks, определить installed-version compatibility.
- Ajv/JSON Schema: validation; JsonLogic or tiny subset for declarative applicability; OPA/Cedar/Casbin only conceptual comparison, не добавлять большие policy engines ради AIR v1.

Сделать `REUSE_DECISION.md`: adopted verbatim/adapted/reference/rejected with evidence, license path и commit. Если код реально заимствован, сохранить LICENSE/NOTICE, attribution.

## 3. Эксперименты целевой host integration

**Минимальный формат свидетельства:** для каждого `R*` иметь `hypothesis`, `setup + isolated scope`, `expected`, `raw receipt reference`, `model-visible/behavior observation where applicable`, `verdict`, `next IF/THEN branch`. Не писать «успешно», если имеется только stdout hook. Для поведенческих тестов использовать минимум два противоположных canary и повторения на свежих isolated sessions; агент фиксирует число прогонов и текстовые результаты без хранения приватных пользовательских prompts.

Временный isolated workspace с синтетическими `AGENTS.md`, Agent Profiles, tiny hook handler; уникальные canary и отдельный тестовый `CODEX_HOME` там, где реально поддерживается. Не подменять desktop проверку CLI. Проверить непосредственно в установленной Desktop:

**R1 Hook dispatch.** `SessionStart(startup,resume,compact)`, `UserPromptSubmit`, `SubagentStart`, `PostCompact`, optional `PostToolUse`: запись receipt → проверка model-visible canary. Контрольный CLI probe при отказе Desktop. Проверить trust/enabled/duplicate hook registrations и Windows invocation (Node direct vs `.cmd`/PowerShell), stdout JSON UTF-8, concurrency.

**R2 Message authority.** Контролируемые конфликтные тесты (native Project vs user, custom Agent Profile vs user, developer `additionalContext` vs user, developer self-delegation within Agent Profile and within hook payload). Проверять фактическое поведение и доступные role/order traces; менять формулировку/полярность и повторять. Факта hook invocation недостаточно.

**R3 Native reload.** В тестовом репозитории `AGENTS.md` A→B→removed и custom `developer_instructions` профиль A→B; проверять до/после compaction, startup/resume и child. Фиксировать, что реально повторно загрузилось и где.

**R4 Compaction recovery.** `SessionStart(source=compact)` получен, injector доставил актуальный полный payload до следующего model call, включая middle/end canary после лимитов. Если compaction нельзя вызвать безопасно, фиксировать непроверенность; не создавать многочасовые шумовые транскрипты.

**R5 Child scoping.** Real custom subagent with role, project path, task context; verify agent_type/task_name/cwd metadata; isolation native vs AIR; relevant Session Directives; отсутствие дублирования Role Profile и чужих scoped policies.

**R6 UserPromptSubmit modes.** A: side-effect-only update Session State при новой persistent directive, без model output; B: short hot canonical excerpt, сохранение фокуса; C: совместный bounded handler, со временем исполнения и доказательством порядка. Внутри одного длинного turn этот hook не срабатывает повторно. Проверить, кто фактически вызывает cheap model/API и доступен ли он в sync hook.

**R7 Limits and failure.** Проверить default `additionalContextLimit`, override (bounded), spill/truncation, latency/timeouts, invalid JSON, permission-denied source, symlink escaping, missing required file, cache corruption, crash during atomic write, restoration after disable.

### R8. Skill escalation + нормативный контракт

Проверить штатное обнаружение [`instruction-conflict-resolution`](../skills/instruction-conflict-resolution/SKILL.md) в host, доступность **одного Shared Policy** через поддерживаемый host route, передачу минимального unresolved case и сохранность настоящего authority. Отдельный отрицательный тест: контракт отсутствует / имеет неподтверждённый источник. В этом случае skill обязан заблокировать только зависимое разрешение, не придумать приоритет. **Shared Policy не редактировать.**

### R9. Availability / blocking отдельного semantic resolver

Синтетический GPA cache HIT, MISS без semantic gap, MISS с gap, resolver timeout, malformed response и unavailable. Проверить, что LLM вызывается только для unresolved semantic relation при отсутствии валидного cache decision; Root не подменяет resolver. Проверить bounded latency и корректный `BLOCKED_RESOLUTION`, не декларируя precompile и synchronous hook как одновременно гарантированные.

## 4. Карта IF → THEN (условные экспериментальные исходы)

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

## 5. Неизвестные архитектурные решения и пороги остановки

- **Schema v1 DEFERRED:** параметры операции, `permit`, `applies_if`, unknown runtime facts, нормализация literals, смысл `require operation`. Прототипы и fixtures допустимы для демонстрации вариантов, выбор нормативной semantics только после отдельного согласования.
- **Shared Policy FROZEN:** не переписывать `agent-policy.md` в процессе исследования. Адаптированный skill уже входит в репозиторий и проверяется как конкретная версия исходников; интеграционная работоспособность пока не доказана.
- **Authority HOST-GATED:** потенциальное повышение Project / Global источников до developer роли и self-delegation проверяется экспериментом и эскалируется при несовместимости.
- **UserPromptSubmit OPEN:** варианты hot reminders / side-effect directives / совместный bounded handler исследуются и сравниваются, но никто не выбирает новый контракт автоматически.
- **Transport BLOCKED:** при отсутствии реального hook или canary proof не обходить ограничения через новый MCP/daemon; сохранить evidence и независимые результаты.

## 6. Приёмка экспериментального задания

1. Версии, cwd и доверенность host определены; результаты Desktop не подменены CLI.
2. По R1–R9 имеются `PASS`, `FAIL`, `INCONCLUSIVE` либо точный `BLOCKED_*` с evidence; не выполненный эксперимент не маркируется PASS.
3. Для H1–H24 существуют только проверенные ветки и явно обозначенные неподтверждённые ветки. Архитектурные расхождения вынесены на user decision.
4. `instruction-conflict-resolution` проверен на совместимость с host source loading; отсутствие Shared Policy блокирует только зависимое действие.
5. Составлена host capability/delivery matrix с наблюдаемыми roles, scopes, events, payload limits и recovery guarantees.
6. Ни один производственный policy/config/Agent Profile/Shared Policy не изменён без отдельного разрешения; откат проверен.
7. Результаты приведены к цепочкам «гипотеза → проверка → наблюдение → анализ → следующая гипотеза/решение» и представлены для согласования архитектуры.

**Итоговый статус:** `EXPERIMENTS_COMPLETE`, `PARTIAL` или `BLOCKED_*` с уровнями доказательств. Это не статус реализованного AIR.

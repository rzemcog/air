<!-- @style: ./air.css -->
<!-- @script: ./air.js -->
<!-- @page: air-docs -->

# AIR — use cases и проблемы, которые мы решаем

**Статус:** согласованные задачи и проверяемые гипотезы. Метрики взяты из прежних forensic-отчётов; AIR ещё не запускался на машине пользователя. Связанные исследования: [`04_EVIDENCE_CHAINS_RU.md`](04_EVIDENCE_CHAINS_RU.md). Экспериментальная проверка: [`05_EXPERIMENTAL_TZ_RU.md`](05_EXPERIMENTAL_TZ_RU.md).

## Классы требований

- **P0:** восстановление и доставка применимых инструкций, отсутствие конфликтующих дублей, корректная authority/scope, наблюдаемость результата.
- **P1:** длительная сессия, краткие напоминания, пользовательские директивы, кешируемая семантическая резолюция, управляемая миграция источников.
- **P2:** удобство ручных правок, переносимость в другой harness, интеграция менеджмента skills в будущем.

| UC | Боль и источник | Целевое поведение AIR | Проверяемая приёмка | Приоритет |
|---|---|---|---|---|
| **UC01 — Compaction recovery** | В срезе ~9ч36м зафиксировано 38 `compacted`; в финальном хвосте ещё 2. Повторные чтения инструкций наблюдались, но потеря конкретного текста из контекста **не доказана**. [E03] | Восстанавливать актуальные managed policies и session directives при подтверждённом lifecycle, учитывать native reload и generation. | На настоящем Windows Codex Desktop canary из начала/середины/конца payload распознаётся после compaction; native body не дублируется; отсутствие события → честный blocker. | P0 |
| **UC02 — Доставка, которую можно проверить** | Ранее чтение файлов, отправку сообщения и фактическое поведение смешивали. Controlled marker показал получение в одном активном ходе, но не устойчивость. [E01] | Различать `source_loaded → prepared → hook_dispatched → model_visible_probe → behavior_sample`. | Trace не заявляет `delivered` по `exit 0`; E2E canary и transcript-level проверка отдельно от hook receipt. | P0 |
| **UC03 — Human progress reinforcement** | При строгом уже прочитанном `output-policy.md` в срезе: 254 interim progress, 67 сообщений длиннее 40 слов, 110 с предложением длиннее 20 слов по эвристике; после узкой коррекции наблюдался рецидив. [E01,E03] | Выборочно напоминать точный канонический фрагмент §2/Style/Communication, без переписывания правила и без шума на каждом tool call. | A/B на сопоставимых задачах: доля compliant progress, частота инъекций, latency, токены; `UserPromptSubmit` не считать механизмом intra-turn reinforcement. | P1 |
| **UC04 — Контракт приоритетов** | Требуемая логическая цепь `User > Agent > Project > Global` пока не доказана при developer-level `additionalContext` и native профилях. [D01] | Разрешать столкновения до отправки текста, делегировать полномочия строго для конкретного profile/payload при подтверждённом runtime. | Поляризованные тесты native/profile/hook/user; при несовместимости `BLOCKED_AUTHORITY`, а не утверждение об успешном override. | P0 |
| **UC05 — Child scoping** | D1 подтверждает spawn child, но `message`/`send_message` в JSONL могут быть encrypted; reading skill зафиксировано уже после первого root-progress (~17 мин). [E02] | Выбирать инструкции для конкретного child на основании проверенных role/path/context facts, не копировать native profile второй раз. | Субагент видит ровно ожидаемые canary; unknown role/scope даёт blocker по child, а не слепое наследование Root. | P0 |
| **UC06 — Conflict resolution без ручного переписывания всей политики** | Исторический bootstrap имеет global/shared/project/profile; источник чтения не гарантирует правильное согласование. Потребность в structured rules и разрешении конфликтов согласована в текущем дизайне. [D01] | Структурированные Rules + открытые versioned Vocabularies, дешёвый semantic resolver лишь для смысловых неопределённостей; GPA и conflict cache. | Unit/contract tests для parsing, references, cross-vocabulary candidate coverage, authority, unknown facts; inspectable решение и отдельный effective view. | P0/P1 |
| **UC07 — Session Directives** | Пользовательские длительные уточнения могут появляться/отменяться в разных turns; исторические логи **не доказывают**, что такое состояние уже терялось. [D02] | Записывать add/revoke/supersede директивы per session и восстанавливать после resume/compact/child без перегонки текущего user prompt в developer. | Replay/duplicate/fork/parallel tests; directives действительно видны в следующем lifecycle; неопределённый user intent не выдумывать. | P1 |
| **UC08 — Разделение исходников и доставки** | Native `AGENTS.md`, user bootstrap и hook-политики могут начать загружать одинаковые тела, а конфликтующую native инструкцию невозможно удалить фильтрацией AIR payload. [D01] | Source inventory и per-event Delivery Plan: `native` либо `AIR` на конкретный source; откат migration. | Source-to-delivery ledger, delta on edit, нет двойного чтения; native conflict → review+blocker. | P0 |
| **UC09 — Устойчивость Windows hooks** | Предыдущая Windows-проверка стороннего PowerShell helper выявила `AuthorizationManager check failed`; обход process-scoped `-ExecutionPolicy Bypass` помог именно тому тесту, но не является разрешением ставить AIR так же. [E06] | Корректный запуск hook, quoting, UTF-8/JSON, trust, symlink/path safety, atomic files; установка без постоянного daemon. | Windows Desktop smoke, permission error, timeout, rollback, isolated plugin registration. | P0 |
| **UC10 — Следы работы и контроль границ** | За долгий прогон root инициировал 431 `apply_patch` против 45 у child; Goal Observer вызывался один раз и указал стагнацию AC2. Это сигнал о workflow, но не доказательство дефекта transport AIR. [E04,E05] | AIR предоставляет диагностику инструкций и source-scoping, чтобы агенту реализации было на чём проверять delivery. Goal Observer/Root orchestration остаются отдельными будущими задачами. | Trace per event без raw policy/prompt, доказательство policy delivery; никаких обещаний исправить распределение работы Root самим AIR. | P1/P2 |
| **UC11 — Ручная корректировка и повторное использование** | Непрозрачное LLM-разрешение заставило бы повторять спор при малой правке источника. Это **дизайн-риск**, не наблюдение из логов. [D03] | User-readable GPA output и versioned conflict decisions с provenance, осторожной инвалидацией и контролируемыми исправлениями. | Изменение одного Rule инвалидирует релевантные решения; новая третья норма не использует некорректный прежний pair-decision. | P1 |
| **UC12 — Устранение стократного перечитывания и лишних источников** | Исторические отчёты фиксируют повторные чтения policies и 88 чтений `SKILL.md` для 16 skills в 24h текстовом экспорте. Причинность с compaction не доказана. [E07] | Применять source fingerprints и точные scopes, доставлять готовое содержимое, не отправлять агенту ссылки с просьбой заново читать исходники. | Replay/rotation: cache hit без ненужного resolver call; изменение source приводит к новой валидированной доставке. | P1 |

## Сценарии первого реально работающего вертикального среза

1. Из выбранного файла с правилами и declared Vocabulary получается валидный Rule IR либо понятная ошибка.
2. При начале/возобновлении test session подтверждается доступность только выбранных управляемых инструкций.
3. При compaction payload восстанавливается и canary наблюдается следующей моделью; native источники обрабатываются согласно реально установленному контракту Codex.
4. Для child с заданным профилем доставляются только применимые правила.
5. Новый пользовательский запрет сохраняется как Session Directive, повторная обработка того же turn не создаёт дубль, отмена снимает его.
6. Два конфликтующих Rule разрешаются по авторитетам; неоднозначный смысл отправляется дешёвому resolver и его результат проходит проверку; cache miss/timeout не скрывается.
7. Отключение plugin возвращает исходную конфигурацию. Проверка не требует изменения рабочей сетевой инфраструктуры.

## Какие результаты AIR пока НЕ подтверждены

Исторические расследования относятся к поведению Codex и Zapret Maintainer, **не к испытаниям реализованного AIR**. Нет прямого доказательства, что compaction удаляла конкретное правило; нет подтверждённого runtime-рецепта изменения developer authority; нет подтверждённого улучшения compliance за счёт hook reminders; нет измеренных latency/стоимости semantic resolver. Соответствующие эксперименты обязательны в ТЗ.

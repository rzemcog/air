# AIR — архитектура, ADR и единое ТЗ для агента

**Срез:** 2026-10-19. **Пакет:** architecture-candidate-2 (редакционная ревизия).
**AIR = Agent Instruction Runtime.** Это план и техническое задание; реализация плагина и тесты на Windows **не проводились в этом пакете**.

## Цели пакета

1. Сохранить консенсус текущего чата и прежнего handoff без терминологического дрейфа.
2. Дать одному агенту **единое ТЗ с реальными экспериментами и условными ветками IF X THEN Y**, без отдельной фазы согласования каждой мелочи.
3. Честно разделить дизайн, подтверждённые host contracts и неизвестные особенности установленного Desktop.
4. Проверить reuse по каждому компоненту, не повторяя уже выполненных исследований без причины.
5. Сохранить **независимую критику с НЕПРИМЕНЁННЫМИ патчами** для дальнейшего совместного review.

## Обязательное чтение для следующего агента

1. `01_AIR_ARCHITECTURE_RU.md` — архитектура, граница Policy/Skill и lifecycle.
2. `07_GLOSSARY_RU.md` — полный словарь сущностей AIR с примерами и разграничениями.
3. `02_ADR_RU.md` — принятые решения, hypotheses и открытые гейты.
4. `03_AGENT_IMPLEMENTATION_TZ_RU.md` — **единственное текущее ТЗ** для исследовательских экспериментов **и** реализации.
5. `04_CONSENSUS_CONFIDENCE_RU.md` — где consensus и что точно/вероятно работает или не работает.
6. `05_REUSE_MATRIX_RU.md` — компонентные references и reuse decisions.

Далее:
- `06_CRITICAL_REVIEW_RU.md` — независимая критика Sol-6. **НЕ является утверждённой архитектурой**.
- `PATCHES_UNAPPLIED/` — 7 неизменённых предложений Sol-6 для отдельного согласования; см. `PATCHES_UNAPPLIED/README.md`.
- `REFERENCE_SNAPSHOTS/` — исторические выжимки и пользовательские вложения для точечной сверки. Актуальное состояние Windows проверяется отдельным экспериментом.

## Правила работы с пакетом

Агент начинает с текущих документов AIR и переходит к историческим материалам только для проверки конкретного вопроса. Результаты локальных тестов и испытаний Codex Desktop фиксируются раздельно. Изменения глобального bootstrap и агентных профилей проходят через permission preflight, резервную копию, согласованный diff и rollback.

Предложения из `PATCHES_UNAPPLIED/` требуют отдельного обсуждения и одобрения. Восстановленная Git-история содержит реконструированные исторические снимки; новая документация сопровождается реальными коммитами текущей работы.

## Текущее состояние

`DESIGN CONSOLIDATED / IMPLEMENTATION NOT STARTED / DESKTOP E2E UNVERIFIED`.

Подтверждённая историческая запись: `~/.agents/AGENTS.md → ENTRYPOINT.md → ~/.agents/shared/` — bootstrap workflow в handoff. **Реальной snapshot установленного `~/.agents` нет**. Прежде чем проектировать чтение `AGENTS.md` как `Global` или `Project`, проверить actual scope/location Codex.

Самые существенные `RUNTIME_GATE`: `SessionStart(compact)`/SubagentStart фактическая доставка, developer vs user precedence, live agent profiles, дублирование native, Session Directives extraction. Самые существенные `SCHEMA_GATE`: formal `permit`, unknown runtime fact, vocabulary operation schemas, hash context semantics. Известная внутренняя коллизия: прежний approved `UserPromptSubmit` hot-reminder vs новый proposed side-effect-only session extraction.

## Пакет и происхождение

Исходное приложение пользователя: `agents-policies-self-contained-handoff-2026-10-18-v2(1).zip` (более 60 МБ, сюда целиком не вкладывается намеренно). Для пакета прочитаны исходные короткие `README_START_HERE.md`, `HANDOFF_COMPACT_RU.md`, `ARCHITECTURE_DECISIONS_RU.md`, `AGENTS_POLICIES_TZ_RU.md`, а также точечный `REUSE_LINKS.md`. Бинарные evidence и raw JSONL **не читались**. Дополнительно рассмотрены приложенные `agent-policy(2).md` и `SKILL(20261018-161925).md`, сохранённые под понятными именами.

Сведения о внешних open-source компонентах разделены в reuse matrix: prior handoff references vs текущая README/docs validation vs неосмотренные исходники.

`SHA256_MANIFEST.tsv` — checksum каждого включённого файла кроме самого manifest. Проверены структура ZIP, наличие обязательных документов и применимость каждого proposal patch в режиме `--dry-run` **к исходной базовой версии**. Это не означает проверки содержимого AIR на реальном ПК.

## Git-история

Новые документы AIR хранятся в каталоге `07_AIR/` существующей реконструированной истории handoff. Первый коммит фиксирует предоставленную пользователю версию AIR `afa3490`, следующий документирует текущую редакционную правку. История до AIR маркирована `RECONSTRUCTED` и описана в корневом `GIT_HISTORY_NOTICE.md`. Все новые исправления можно просмотреть через `git log --oneline -- 07_AIR` и `git diff afa3490..HEAD -- 07_AIR`.

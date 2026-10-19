# AIR — архитектура, ADR и единое ТЗ для агента

**Срез:** 2026-10-19. **Пакет:** architecture-candidate-1.  
**AIR = Agent Instruction Runtime.** Это план и техническое задание; реализация плагина и тесты на Windows **не проводились в этом пакете**.

## Цели пакета

1. Сохранить консенсус текущего чата и прежнего handoff без терминологического дрейфа.
2. Дать одному агенту **единое ТЗ с реальными экспериментами и условными ветками IF X THEN Y**, без отдельной фазы согласования каждой мелочи.
3. Честно разделить дизайн, подтверждённые host contracts и неизвестные особенности установленного Desktop.
4. Проверить reuse по каждому компоненту, не повторяя уже выполненных исследований без причины.
5. Сохранить **независимую критику с НЕПРИМЕНЁННЫМИ патчами** для дальнейшего совместного review.

## Обязательное чтение для следующего агента

1. `01_AIR_ARCHITECTURE_RU.md` — архитектура, glossary и lifecycle.
2. `02_ADR_RU.md` — принятые решения, hypotheses и открытые гейты.
3. `03_AGENT_IMPLEMENTATION_TZ_RU.md` — **единственное текущее ТЗ** для исследовательских экспериментов **и** реализации.
4. `04_CONSENSUS_CONFIDENCE_RU.md` — где consensus и что точно/вероятно работает или не работает.
5. `05_REUSE_MATRIX_RU.md` — компонентные references и reuse decisions.

Далее:
- `06_CRITICAL_REVIEW_RU.md` — независимая критика Sol-6. **НЕ является утверждённой архитектурой**.
- `PATCHES_UNAPPLIED/` — proposal diff. **Не применять без согласования с пользователем**.
- `REFERENCE_SNAPSHOTS/` — точечно при уточнениях (ранее согласованные handoff/ТЗ/reuse и предоставленные policy/skill). Не считать файлами, установленными на машине.

## Что не делать

- Не читать весь старый handoff/JSONL/Git историю подряд, не искать доказательства там, где достаточно утверждённой выжимки.
- Не запускать Zapret Maintainer и не выполнять live network mutations/AC.
- Не создавать новые MCP, daemon, внешнюю БД или Skill Manager в текущей задаче.
- Не смешивать `Policy` и `Skill` как исполняемые сущности.
- Не выдавать результат `npm test` за real Codex Desktop E2E.
- Не менять user global bootstrap/agent profiles без permission preflight + backup + controlled diff + rollback.
- Не применять roast-патчи автоматически.

## Текущее состояние

`DESIGN CONSOLIDATED / IMPLEMENTATION NOT STARTED / DESKTOP E2E UNVERIFIED`.

Подтверждённая историческая запись: `~/.agents/AGENTS.md → ENTRYPOINT.md → ~/.agents/shared/` — bootstrap workflow в handoff. **Реальной snapshot установленного `~/.agents` нет**. Прежде чем проектировать чтение `AGENTS.md` как `Global` или `Project`, проверить actual scope/location Codex.

Самые существенные `RUNTIME_GATE`: `SessionStart(compact)`/SubagentStart фактическая доставка, developer vs user precedence, live agent profiles, дублирование native, Session Directives extraction. Самые существенные `SCHEMA_GATE`: formal `permit`, unknown runtime fact, vocabulary operation schemas, hash context semantics. Известная внутренняя коллизия: прежний approved `UserPromptSubmit` hot-reminder vs новый proposed side-effect-only session extraction.

## Пакет и происхождение

Исходное приложение пользователя: `agents-policies-self-contained-handoff-2026-10-18-v2(1).zip` (более 60 МБ, сюда целиком не вкладывается намеренно). Для пакета прочитаны исходные короткие `README_START_HERE.md`, `HANDOFF_COMPACT_RU.md`, `ARCHITECTURE_DECISIONS_RU.md`, `AGENTS_POLICIES_TZ_RU.md`, а также точечный `REUSE_LINKS.md`. Бинарные evidence и raw JSONL **не читались**. Дополнительно рассмотрены приложенные `agent-policy(2).md` и `SKILL(20261018-161925).md`, сохранённые под понятными именами.

Сведения о внешних open-source компонентах разделены в reuse matrix: prior handoff references vs текущая README/docs validation vs неосмотренные исходники.

`SHA256_MANIFEST.tsv` — checksum каждого включённого файла кроме самого manifest. Проверены структура ZIP, наличие обязательных документов и применимость каждого proposal patch в режиме `--dry-run` **к исходной базовой версии**. Это не означает проверки содержимого AIR на реальном ПК.

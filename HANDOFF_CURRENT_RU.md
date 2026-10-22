<!-- @style: ./docs/air.css -->
<!-- @script: ./docs/air.js -->

# AIR — актуальный handoff

**Актуализация:** 22 октября 2026. **Стадия:** архитектура и эксперименты. Исполняемый AIR runtime ещё не создан, Windows Desktop E2E для AIR не проведён.

## Продолжение работы

1. Проверить `git status --short` и `git log -4 --oneline`.
2. Прочитать [README](README.md), [архитектуру](docs/01_ARCHITECTURE_RU.md), [ADR](docs/02_ADR_RU.md), [словарь](docs/07_GLOSSARY_RU.md) и [статусы согласования](docs/08_CONSENSUS_CONFIDENCE_RU.md).
3. Рабочее задание: [эксперименты R1–R9 / H1–H24](docs/05_EXPERIMENTAL_TZ_RU.md). [ТЗ реализации](docs/10_IMPLEMENTATION_DRAFT_TZ_RU.md) имеет статус DRAFT и не заменяет экспериментальное задание.
4. Для доказательных ограничений читать [use cases](docs/03_USE_CASES_RU.md) и [исторические наблюдения](docs/04_EVIDENCE_CHAINS_RU.md). Для поиска готовых компонентов — [матрицу reuse](docs/06_REUSE_MATRIX_RU.md).
5. Для изменения оформления применять [skill по MdStyled](skills/mdstyled-documentation/SKILL.md) и [инструкцию просмотра](docs/README_VISUAL_PREVIEW_RU.md).
6. После правок запускать `python tools/verify_package.py` и `git diff --check`, обновлять `SHA256SUMS` после окончательного изменения отслеживаемых файлов.

## Согласованные границы

- **Policy** задаёт нормы: что запрещено, обязательно, разрешено и при каких условиях. **Skill** задаёт процедуру достижения результата.
- Архитектура **harness-agnostic**. Первый проверяемый Host Adapter нацелен на Codex Desktop / Windows.
- `Global + Project + Agent` (GPA) разрешаются отдельно от пользовательских `Session Directives`. Semantic Resolver вызывается для неоднозначных отношений и валидирует результат; недостоверный cache и ошибка резолюции не считаются доказательством совместимости.
- Canonical Sources, Vocabulary, Rules, IR, Conflict Decisions, Delivery Plan, Payload, Session State и Trace разделены. Host native sources не дублируются через AIR.
- [Skill разрешения конфликтов](skills/instruction-conflict-resolution/SKILL.md) использует один предоставленный Host Adapter контракт Shared Policy. Изменение Shared Policy в данное задание не входит.
- Значения `parameters`, `permit`, `applies_if`, `require operation`, unknown facts и literals для Schema v1 остаются **НЕ СОГЛАСОВАНЫ**.
- Семь [архитектурных предложений P01–P07](docs/09_UNAPPLIED_PROPOSALS_RU.md) остаются **PROPOSED / UNAPPLIED**; их патчи хранятся в `proposals/`.

## Ограничения исполнения

Эксперименты проводить изолированно, с проверяемым состоянием host и rollback. Не изменять production-профили, native policies, Shared Policy или глобальный bootstrap без отдельного утверждения. Не начинать разработку спорной Schema v1, не переносить результаты других проектов на AIR без проверки. Отчёты о прошлых запусках из [исторических наблюдений](docs/04_EVIDENCE_CHAINS_RU.md) являются вторичными сведениями: первичные логи не входят в репозиторий и не доказывают работоспособность AIR.

## Текущее следующее действие

Выполнить preflight и первые host probes из `docs/05_EXPERIMENTAL_TZ_RU.md`, собрать воспроизводимые positive/negative outcomes. При технической неопределённости сообщить конкретный blocker и предложить выбор, не объявлять неподтверждённые эксперименты завершёнными.

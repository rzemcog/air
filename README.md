<!-- @style: ./docs/.mdstyled/air.css -->
<!-- @script: ./docs/.mdstyled/air.js -->
<!-- @page: air-docs -->

# AIR · Agent Instruction Runtime

**Артефакты архитектуры и исследований · редакция 22 октября 2026 · Codex Desktop / Windows как первая host integration**

AIR находится на стадии проектирования. Архитектура AIR Core описана независимо от конкретного harness. Текущая задача для агента: **проверить host contracts и закрыть/локализовать архитектурные неизвестные**. ТЗ реализации остаётся черновиком до последующего согласования. Код AIR и проверенные Windows Desktop E2E ещё не созданы.

<div class="air-kpi-row" aria-label="Текущее состояние документации">
  <div class="air-kpi"><strong>CURRENT</strong>Эксперименты R1–R9</div>
  <div class="air-kpi"><strong>DRAFT</strong>ТЗ реализации</div>
  <div class="air-kpi"><strong>OPEN</strong>Schema v1</div>
  <div class="air-kpi"><strong>SEPARATE</strong>Delivery / Compliance</div>
</div>

## Начало работы

1. Прочитать [`docs/01_ARCHITECTURE_RU.md`](docs/01_ARCHITECTURE_RU.md), [`docs/02_ADR_RU.md`](docs/02_ADR_RU.md), [`docs/07_GLOSSARY_RU.md`](docs/07_GLOSSARY_RU.md).
2. Исполнить **только экспериментальное задание** [`docs/05_EXPERIMENTAL_TZ_RU.md`](docs/05_EXPERIMENTAL_TZ_RU.md). Оно включает host probes R1–R9, карту H1–H24 и evidence-first workflow с локальными blockers.
3. Для будущего этапа есть [`docs/10_IMPLEMENTATION_DRAFT_TZ_RU.md`](docs/10_IMPLEMENTATION_DRAFT_TZ_RU.md). Статус DRAFT: само по себе не разрешает разработчику определить спорную Schema v1 или изменить Shared Policy.
4. При чтении результатов пользоваться цепочками [`docs/04_EVIDENCE_CHAINS_RU.md`](docs/04_EVIDENCE_CHAINS_RU.md) и [`docs/03_USE_CASES_RU.md`](docs/03_USE_CASES_RU.md), а решения о reuse проверять по [`docs/06_REUSE_MATRIX_RU.md`](docs/06_REUSE_MATRIX_RU.md).

Схемы и настройка визуального чтения: [**Визуальное оформление MdStyled**](docs/README_VISUAL_PREVIEW_RU.md).

## Карта рабочих файлов

| Путь | Назначение |
|---|---|
| `docs/README_VISUAL_PREVIEW_RU.md` | Как открыть визуальную документацию в MdStyled, офлайн CSS/JS |
| `docs/01_ARCHITECTURE_RU.md` | Архитектура AIR Core и Host Adapter, диаграммы resolver/delivery |
| `docs/02_ADR_RU.md` | Согласованные и открытые решения |
| `docs/03_USE_CASES_RU.md` | Проблемы, use cases, ожидаемое поведение |
| `docs/04_EVIDENCE_CHAINS_RU.md` | Предыдущие гипотезы/наблюдения и ограничения доказательств |
| `docs/05_EXPERIMENTAL_TZ_RU.md` | **Текущее исполняемое ТЗ экспериментов**, R1–R9 / H1–H24 |
| `docs/06_REUSE_MATRIX_RU.md` | Готовые компоненты для адаптации и ссылки на исходные исследования |
| `docs/07_GLOSSARY_RU.md` | Нормативная терминология |
| `docs/08_CONSENSUS_CONFIDENCE_RU.md` | Консенсус и уровни технической подтверждённости |
| `docs/09_UNAPPLIED_PROPOSALS_RU.md` | Открытые предложения Sol-6, не применённые к архитектуре |
| `docs/10_IMPLEMENTATION_DRAFT_TZ_RU.md` | **Черновик** разработки после закрытия gates, с диаграммой зависимостей |
| `skills/instruction-conflict-resolution/SKILL.md` | **Адаптированный skill**, v0.2.0, для эскалированных конфликтов |
| `skills/instruction-conflict-resolution/MIGRATION_NOTES.md` | Исходник, изменения и ограничения проверок skill |
| `changes/APPLIED_instruction_conflict_resolution.patch` | Применённый patch исходного SKILL.md, отдельно от предложений |
| `proposals/*.patch` | Семь **непринятых** архитектурных патчей к исторической baseline |

## Консенсус и замороженные решения

- Policy задаёт нормативные ограничения; Skill задаёт процедуру и последовательность работы.
- Архитектура harness-agnostic; первая проверяемая интеграция Codex Desktop Windows.
- Отдельный дешёвый Semantic Resolver вызывается на неразрешимых структурно отношениях при отсутствии валидного cached decision. Невалидность или недоступность вызывает локальную блокировку.
- `instruction-conflict-resolution` использует **один Shared Policy contract, передаваемый Host Adapter**. В репозитории skill адаптирован, **Shared Policy не менялся**; требуется R8 runtime proof.
- Семантика Schema v1 (`parameters`, `permit`, `applies_if`, unknown facts, literals, `require operation`) **DEFERRED**.
- Две линии ТЗ существуют одновременно: эксперименты = CURRENT; реализация = DRAFT.

## Исходные материалы и история

Исходный архив `agents-policies-self-contained-handoff-2026-10-18-v2(1).zip` содержал первичные JSONL, большие архивы evidence, старые policies и исторические handoff. В текущем рабочем дереве сохранены сжатые наблюдения и адреса источников, без дублирования private raw logs. Историческая Git-история из handoff реконструирована; она не равна доказательству live Windows runtime. Восстановление прошлого evidence проводится по конкретному спорному утверждению.

Запрещено в ходе экспериментального задания менять production-проекты, существующие native Agent Profiles, Shared Policy или глобальный bootstrap без явного разрешения, снимка состояния и rollback. Семь unapplied архитектурных предложений нельзя считать утверждёнными только потому, что они лежат в Git.

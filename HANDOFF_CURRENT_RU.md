<!-- @style: ./docs/air.css -->
<!-- @script: ./docs/air.js -->
<!-- @page: air-docs -->

# AIR — handoff для продолжения работы

**Состояние:** 22 октября 2026. **Текущий предмет работы:** визуальная документация MdStyled, проверяемая на реальном Windows VS Code. AIR runtime **не реализован**. Архитектура ещё согласовывается.

## 1. С чего начать следующему агенту

1. Открой репозиторий с сохранённой `.git`, проверь `git status --short`, `git log -4 --oneline`.
2. Прочитай этот файл и [`README.md`](README.md).
3. Для вопросов Markdown/HTML/CSS/JS **применяй** [`skills/mdstyled-documentation/SKILL.md`](skills/mdstyled-documentation/SKILL.md), затем [`docs/MDSTYLED_INTEGRATION_NOTES_RU.md`](docs/MDSTYLED_INTEGRATION_NOTES_RU.md) и [`docs/00_RENDER_TEST_RU.md`](docs/00_RENDER_TEST_RU.md).
4. Для архитектуры и её статусов читай [`docs/01_ARCHITECTURE_RU.md`](docs/01_ARCHITECTURE_RU.md), [`docs/02_ADR_RU.md`](docs/02_ADR_RU.md), [`docs/07_GLOSSARY_RU.md`](docs/07_GLOSSARY_RU.md), [`docs/08_CONSENSUS_CONFIDENCE_RU.md`](docs/08_CONSENSUS_CONFIDENCE_RU.md).
5. Выполни `python tools/verify_package.py` и `git diff --check` до начала правок и после них. Если исправляешь пакет, перегенерируй `SHA256SUMS` последним шагом перед commit.

## 2. Последний запрос и выполненная работа

Пользователь установил [MdStyled](https://github.com/OsamaAbuSitta/MDStyled) для VS Code и хочет качество оформления не хуже интерактивной документации: HTML/CSS/JS, компактные схемы, адаптивность, хороший контраст. Прежние Mermaid-диаграммы были высокими, с обрезкой подписей.

**Подтверждённый пользователем дефект:** HTML-схема на скриншоте превратилась в слитный текст. Предыдущее решение добавляло inline fallback CSS в Markdown. Пользователь обоснованно отверг его: это маскировка проблемы, а не исправление загрузки CSS.

**Текущее изменение в этом репозитории:**

- Удалены ручные `<style>` fallback из Markdown. Только [`docs/air.css`](docs/air.css) и [`docs/air.js`](docs/air.js) задают оформление/интерактивность.
- CSS и JS подключаются штатными директивами `@style`/`@script`, пути определяются относительно текущего Markdown.
- Удалён дублирующий `docs/mdstyled.config.json`.
- Переключатели графа переделаны с `data-air-*`/`button` на разрешённые `class`/`id`/`a`: в `src/previewProvider.ts` MDStyled применяется HTML-sanitizer, который не сохраняет произвольные `data-air-*`.
- Добавлен независимый runtime-probe [`docs/00_RENDER_TEST_RU.md`](docs/00_RENDER_TEST_RU.md) для CSS и JS, а также [`docs/MDSTYLED_INTEGRATION_NOTES_RU.md`](docs/MDSTYLED_INTEGRATION_NOTES_RU.md).
- Создан [`skills/mdstyled-documentation/SKILL.md`](skills/mdstyled-documentation/SKILL.md), регламент работы над визуальной документацией.

**СТАТУС:** файловая структура и исходный контракт MDStyled проверены; **реальный предпросмотр в Windows у пользователя после исправления ещё НЕ подтверждён**. Нельзя писать «исправлено» без его проверки. Отдельно проверяй, не подменяет ли MdStyled встроенный VS Code Markdown Preview.

## 3. Как установлен реальный контракт MdStyled

Проверены исходники публичного репозитория `OsamaAbuSitta/MDStyled` (main, 2026-10-22):

- [`src/engine/config.ts`](https://github.com/OsamaAbuSitta/MDStyled/blob/main/src/engine/config.ts): директивы и пути к файлам CSS/JS обрабатываются относительно каталога `.md`.
- [`src/engine/index.ts`](https://github.com/OsamaAbuSitta/MDStyled/blob/main/src/engine/index.ts): вызов загрузчиков стилей и скриптов.
- [`src/engine/renderer.ts`](https://github.com/OsamaAbuSitta/MDStyled/blob/main/src/engine/renderer.ts): сами файлы читаются через `fs`, затем MdStyled вставляет CSS в `<style>` итогового webview. **Это не то же самое, что ручной inline fallback в `.md`.**
- [`src/previewProvider.ts`](https://github.com/OsamaAbuSitta/MDStyled/blob/main/src/previewProvider.ts): sanitization, допустимые HTML атрибуты, диагностика `CSS length`, webview.

Из этих данных нельзя заключить, что установленная на ПК версия идентична `main`, или что ошибка уже устранена. Диагноз требует результата `00_RENDER_TEST_RU.md` и/или консоли DevTools.

## 4. Следующее проверяемое действие по MdStyled

Открыть **MdStyled: Open Preview** на [`docs/00_RENDER_TEST_RU.md`](docs/00_RENDER_TEST_RU.md). Зафиксировать три индикатора: внешняя CSS-карточка, состояние JS, `Computed CSS`. При отказе: `Help → Toggle Developer Tools → Console`, запись `[MdStyled] Preview loaded, CSS length:` и ошибки. Если CSS не загрузился, сравни путь директивы с расположением CSS. Если CSS есть, но дизайн не действует, исследуй sanitization/селекторы. Не возвращать `<style>` в `.md`.

## 5. Архитектура AIR: принятые границы

- **Policy** задаёт нормативные ограничения: при каких условиях что обязательно, запрещено, разрешено или предпочтительно. **Skill** задаёт последовательность действий для получения результата. В будущем планируется интеграция функций управления skills.
- Архитектура **harness-agnostic**; первая интеграция/эксперименты направлены на Codex Desktop / Windows через Host Adapter.
- `Global + Project + Agent` (GPA) разрешается отдельно от пользовательских `Session Directives`. Resolver выделенный и дешёвый; Root не занимается массовой семантической резолюцией. При недостоверном cache MISS вызывается resolver; при недоступности не предполагается совместимость.
- Разделены Canonical Source, Vocabulary, Rule, Deterministic IR, Policy Graph, Conflict Decision, Resolution, Delivery Plan, Payload, Session State и Trace. Native-delivery не должна дублироваться через AIR; поведение проверяется реальными host probes.
- Адаптированный [`skills/instruction-conflict-resolution/SKILL.md`](skills/instruction-conflict-resolution/SKILL.md) обрабатывает эскалированные конфликты по единому Shared Policy контракту от Host Adapter. Существующий **Shared Policy не менять**, пока пользователь не одобрит.
- `parameters`, `permit`, `applies_if`, `require operation`, unknown facts и literals в **Schema v1 пока НЕ СОГЛАСОВАНЫ**. Не превращать обсуждавшиеся варианты в стандартизованный формат.

## 6. Задания, запреты и проверки

| Часть | Статус | Файл |
|---|---|---|
| Эксперименты R1–R9 + условная карта H1–H24 | **CURRENT** | [`docs/05_EXPERIMENTAL_TZ_RU.md`](docs/05_EXPERIMENTAL_TZ_RU.md) |
| ТЗ реализации | **DRAFT** | [`docs/10_IMPLEMENTATION_DRAFT_TZ_RU.md`](docs/10_IMPLEMENTATION_DRAFT_TZ_RU.md) |
| Обоснование через use cases и evidence | **REFERENCE** | [`docs/03_USE_CASES_RU.md`](docs/03_USE_CASES_RU.md), [`docs/04_EVIDENCE_CHAINS_RU.md`](docs/04_EVIDENCE_CHAINS_RU.md) |
| Компоненты для переиспользования | **REFERENCE** | [`docs/06_REUSE_MATRIX_RU.md`](docs/06_REUSE_MATRIX_RU.md) |
| Семь замечаний к архитектуре `P01–P07` | **PROPOSED, UNAPPLIED** | [`docs/09_UNAPPLIED_PROPOSALS_RU.md`](docs/09_UNAPPLIED_PROPOSALS_RU.md), `proposals/*.patch` |

Запреты: не перезапускать посторонний Zapret-проект, не менять production-политики/профили/глобальный bootstrap, не применять P01–P07 без согласования, не подменять runtime-проверку скриншотом стороннего Chromium. История `.git` содержит **реконструкцию исходных материалов**; не выдавать её за журнал выполненных live-экспериментов AIR.

## 7. Последняя проверка состояния

Команда: `python tools/verify_package.py` проверяет локальные ссылки, декларации MDStyled-ассетов, запрет ручного CSS и неподдерживаемых `data-air-*`, сохранность R1–R9 / H1–H24, историческую применимость семи непринятых патчей и SHA256. `git diff --check` проверяет пробелы и маркеры конфликтов. Коммит и итоговый архив создаются по завершении текущего изменения; на следующем заходе проверяй фактический `git log`, а не предполагаемый hash из текста.

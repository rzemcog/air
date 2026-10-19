# AIR · Agent Instruction Runtime

**Артефакты для реализации · 19 октября 2026 · Windows Codex Desktop first**

Этот Git-репозиторий содержит актуальную архитектуру AIR, решения, проверяемые use cases, доказательную историю прежних экспериментов и **единое исполняемое ТЗ**, объединяющее новые эксперименты с реализацией. Код AIR ещё не написан; Windows Desktop E2E AIR ещё не выполнялись.

## Как начать

1. Прочитать [`docs/05_IMPLEMENTATION_TZ_RU.md`](docs/05_IMPLEMENTATION_TZ_RU.md) как задание исполнителю; ознакомиться с [`docs/01_ARCHITECTURE_RU.md`](docs/01_ARCHITECTURE_RU.md), [`docs/02_ADR_RU.md`](docs/02_ADR_RU.md) и [`docs/07_GLOSSARY_RU.md`](docs/07_GLOSSARY_RU.md).
2. Проверить use cases [`docs/03_USE_CASES_RU.md`](docs/03_USE_CASES_RU.md) против цепочек исторических наблюдений [`docs/04_EVIDENCE_CHAINS_RU.md`](docs/04_EVIDENCE_CHAINS_RU.md).
3. Root назначает независимые эксперименты субагентам и работает по таблице `IF → THEN` **без отдельного этапа handoff**. При опасном/концептуальном неопределённом ответе блокируется только зависимый компонент.
4. На каждый реальный host experiment записывать tested build, гипотезу, setup, expected/observed, trace и verdict. Не заменять proof заявлением инструмента или модели.

## Файлы

| Путь | Для чего |
|---|---|
| `docs/01_ARCHITECTURE_RU.md` | Модель AIR, граница Policy/Skill, Rule/Vocabulary, runtime, cache/delivery |
| `docs/02_ADR_RU.md` | Согласованные решения и явно открытые вопросы |
| `docs/03_USE_CASES_RU.md` | Пользовательские боли, приоритеты, сценарии, acceptance |
| `docs/04_EVIDENCE_CHAINS_RU.md` | Гипотезы → проверки → наблюдения → выводы → следующие тесты, со ссылками на исходные журналы |
| `docs/05_IMPLEMENTATION_TZ_RU.md` | Единое ТЗ: subagents, experiments, 24 IF→THEN gate, AC01–AC10, старт реализации |
| `docs/06_REUSE_MATRIX_RU.md` | Что можно reuse/adapt/reference и что ещё needs source review |
| `docs/07_GLOSSARY_RU.md` | Терминологический контракт с примерами |
| `docs/08_CONSENSUS_CONFIDENCE_RU.md` | Консенсус и уровни доказанности: точно/вероятно/непроверено |
| `docs/09_UNAPPLIED_PROPOSALS_RU.md`, `proposals/` | Отдельные замечания Sol-6 и патчи; **не утверждены и не применены** |

## Источники и ограничения

В исходном пользовательском ZIP `agents-policies-self-contained-handoff-2026-10-18-v2(1).zip` было значительно больше данных: primary JSONL, архивы завершённого прогона, предыдущие варианты policies, исторические handoff и forensic audits. Новый пакет сохраняет проверяемую **выжимку и адреса источников**, но не дублирует многомегабайтные журналы, файлы других проектов, private diagnostics и старые handoff. При спорном факте исследователь может вернуться к оригинальному ZIP и проверить ровно указанное место.

Сводки по Zapret Maintainer используются **только как evidence поведения агентов Codex**, а не как план возобновления Zapret. Исходные JSONL могут содержать частные сведения; в AIR Git их не публиковать.

Из исходного ZIP сохранена реконструированная Git-история handoff, включая предыдущие коммиты AIR. **Состояние рабочего дерева этого коммита очищено** от прошлых документов. Ранее синтетическая история не доказывает, что коммиты соответствовали живым изменениям на Windows-хосте.

## Правила ведения проекта

- Концептуально принятые решения маркированы `CONSENSUS`/`ACCEPTED`; непроверенные host facts остаются `RUNTIME_GATE`.
- Никаких автоматических изменений живых `.agents`, native профилей, production проектов до отдельного permission preflight, backup и плана отката.
- Актуальные artifacts редактируются новым Git commit, старые черновики и отработанные логи в этот репозиторий не возвращаются.
- `proposals/*.patch` создаются **отдельно от базовых файлов** и применяются только после нового консенсуса.

# Decision record / идеи и гипотезы из нескольких сессий

Термины: **УТВЕРЖДЕНО** — прямо согласовано пользователем; **ПРЕДПОЧТЕНИЕ** — рабочая рекомендация, не равна утверждению деталей; **ГИПОТЕЗА** — проверить реализацией; **ОТЛОЖЕНО** — не реализовать в MVP; **ОГРАНИЧЕНИЕ** — обязательно сохранять. Это решения о *будущем* plugin, не утверждение, что он уже установлен.

## Output Policy / Ultracave

- **УТВЕРЖДЕНО** §2: события вместо ритуальных прогресс-сообщений; один event/update, одно короткое предложение default, до 20 слов в предложении, второе предложение только для важного следствия/безопасности/смысла; отсутствие annunciation skills/tools/checks; исключения при обязательной точной техинформации.
- **УТВЕРЖДЕНО** заменить blanket ban `hedging` на `unsupported speculation`: точная uncertainty и отрицания обязательны. Текст см. `01_CURRENT/output-policy.md`.
- **УТВЕРЖДЕНО** §3 native Ultracave compression как есть: agent-facing, включая persistent specifications, handoffs, task-state, recovery, journals; payload only; сохранять negation/ownership/dependencies/order/AC/evidence. Нет потребности в ещё одном патче §3.
- **ЗАВЕРШЕНО РАНЕЕ (ПО СЛОВАМ ПОЛЬЗОВАТЕЛЯ)** provenance manifest и skill-adaptation provenance updater. Не возвращать к обсуждению с нуля.
- **УТВЕРЖДЕНО** удалить устаревший §6 fallback на original skills. Сохранить §1,4,5.
- **ПОДТВЕРЖДЁННЫЙ РИСК** наличие правила в model context не гарантирует его соблюдение. Отдельно измерять human progress по JSONL и не путать delivery с enforcement.

## Agents Policies: first implementation

- **УТВЕРЖДЕНО (НАПРАВЛЕНИЕ)** отдельный plugin `Agents Policies`, reuse `codex-rules` вместо нового движка, ограниченная явная source selection.
- **УТВЕРЖДЕНО** приоритет локальной установки Codex Desktop Windows; не вводить дополнительный постоянный daemon, внешнюю БД, новую memory fabric, сторонний ACP/MCP без нужды.
- **УТВЕРЖДЕНО** native `AGENTS.md` оставить Codex. Plugin управляет ENTRYPOINT + выбранными shared policies, не объединяя произвольные `AGENTS.md` из других scopes в один developer-level blob.
- **УТВЕРЖДЕНО** выбранные политики должны поддерживать full delivery на recovery/compaction и краткие hot reminders для `output-policy`, `style`, `communication`. Hot extraction от канонических heading, без дублирования policy bodies в коде.
- **ПРЕДПОЧТЕНИЕ / ПОСЛЕДНЯЯ РЕВИЗИЯ SOL-6** оставить startup bootstrap через `AGENTS.md → ENTRYPOINT.md → shared` на первом этапе, чтобы избежать двойного чтения; при `SessionStart(compact)` повторно inject полный обязательный bundle. Startup-migration целиком в plugin — возможно только синхронно с правкой EntryPoint, если измерения требуют.
- **УТВЕРЖДЕНО ПО СМЫСЛУ** `SubagentStart` получает applyable policies; subagent не должен слепо наследовать Root context.
- **УТВЕРЖДЕНО** `UserPromptSubmit` для hot sections; не читать полные политики при каждом user message, если нет изменения hash. Но хот-напоминание собственно должно срабатывать по правилу даже при прежнем hash, если выбран этот режим: distinct cache policies для full и hot.
- **ПОДТВЕРЖДЁННЫЙ ФАКТ** `UserPromptSubmit` не активируется внутри одного длинного turn; это *не решение* для многочасового прогресса без нового user message.
- **ГИПОТЕЗА / ВЫСОКИЙ ПРИОРИТЕТ** ограниченный, event/phase-based intra-turn hot reminder через hook, возможно `PostToolUse`; выбирать триггер и budget по измеренным overhead/behavior, не включать на каждый tool call. Требуется проверка в настоящем Codex Desktop.
- **УТВЕРЖДЕНО** cache хранит факт успешной injection по session/generation/hash, **не** остаток внутреннего model context; после compaction full bundle надо forced replay независимо от cache. `PostCompact` только invalidation, `SessionStart(compact)` delivers.
- **УТВЕРЖДЕНО** trace для policy delivery: source paths, SHA256, event, injected scope, mode, status, без raw content по умолчанию. Не общий Agent Audit.
- **ПРЕДПОЧТЕНИЕ** `~/.agents/policies.toml` как первый способ выбора файлов/директорий, явные scopes и precedence; UI file picker позже, если реальный Codex plugin settings SDK это позволяет.
- **УТВЕРЖДЕНО** брать `codex-subpath-agentsmd-hooks` как **reference** для Windows/subpath resolution; не ставить параллельно как runtime plugin.
- **ОГРАНИЧЕНИЕ** доверие к policy sources (никаких произвольных untrusted project Markdown с повышением в developer context), контроль symlink traversal, корректный error при усечении, платформенные различия Node/PowerShell, отсутствие секретов в логах.
- **ГИПОТЕЗА** установить performance budgets: bytes/tokens/hook latency, ручное расширение limit только по измеренным данным. Default для hook `additionalContextLimit` ~2500 tokens; нельзя считать усечённый текст полным.

## Goal Observer vs You Should Know / отложено

- **УТВЕРЖДЕНО: ОТЛОЖЕНО** дорабатывание Goal Observer приоритетом ниже Agents Policies. В тесте он активировался один раз, самостоятельно себя не вызывает.
- **ИДЕЯ** `~/.agents/agents/goal-observer.md` как *канонический* prompt (пользователь имел в виду именно этот путь), Codex-native custom TOML adapter под `~/.codex/agents/goal-observer.toml` или project path; по официальной документации Markdown в `.agents/agents` автоматически Codex не регистрируется.
- **ПРЕДПОЧТЕНИЕ** модель Observer read-only, independent judgement, вызовы после material batches (3–5 meaningful actions), blockers, repeated failures, strategy shifts, pre-done. Trigger orchestration не должна целиком зависеть от Root. Избегать recursion/false-positive.
- **REFERENCE** `yimengbenxin/codex-goal-supervisor` — возможно переиспользовать judge/checkpoint, но НЕ переносить альтернативный `North Star` source-of-truth поверх canonical goal YAML.
- **РАЗДЕЛЕНЫ НАЗНАЧЕНИЯ** `You Should Know` — проактивная полезная заметка пользователю; Goal Observer — контроль progression/AC. `pirate/codex-structured-steering` — концептуальный аналог первого. Параллельное использование теоретически полезно, но не одобрено к немедленной установке.

## Agent Audit / encrypted agent-to-agent / отложено

- **ОГРАНИЧЕНИЕ** native collaboration JSONL часто записывает `encrypted_content`; plaintext нельзя восстановить просто из экспортированного JSONL. Отсутствие поля != отсутствие делегирования.
- **ГИПОТЕЗА НА ПРОВЕРКУ** `PreToolUse` может выдать `tool_input` для native `spawn_agent` / `send_message`; coverage нестабильна/может исключать специализирующиеся вызовы. Сначала smoke в конкретной Windows Codex Desktop, *потом* делать вывод.
- **ОТЛОЖЕНО** отдельный `Agent Audit` минимальный, детерминированный; он не должен загрязнять `Agents Policies`. Plaintext logging только opt-in, с security/redaction и сроком хранения.
- **ОТЛОЖЕНО И УСЛОВНО** MCP wrapper `delegate_task` / запуск отдельного `codex exec`: не прозрачная замена внутреннего `spawn_agent`, высокая сложность; использовать только если штатные hooks не покрывают нужный путь.

## Root orchestration / отдельная проблема

- **УТВЕРЖДЕНО** Root по умолчанию координатор, не основной исполнитель: scope and AC assignment дочерним исполнителям, parallel независимых файлов/тестов, самостоятельно только trivial lower-overhead, integration, privilege gates, audit and acceptance.
- **ОГРАНИЧЕНИЕ** live mutation router/NFQUEUE/production state — serial guarded, предварительно установленная host identity `ssh router`, proper preflight/rollback, no background races.
- **ПОДТВЕРЖДЁННЫЙ ДЕФЕКТ** фактические 431 Root vs 45 child apply_patch вызовов, повторные долгие Run failures, один Goal Observer call за ~10h. Plugin доставки сам по себе этого не чинит: отдельный action item после MVP.
- **ОГРАНИЧЕНИЕ** никаких возобновлений `Zapret Maintainer`, новых AC/тестов или router mutations в рамках исправления workflow.

## Вопросы, которые следующая сессия должна проверить, а не предполагать

1. Поддерживает ли установленная Windows Codex Desktop сборка `SessionStart(compact)`, `SubagentStart`, `UserPromptSubmit`, `PostToolUse` в заявленном виде? Plugin compatibility/host plugin settings API?
2. Какой startup flow реально установлен: global `AGENTS.md`, `ENTRYPOINT`, shared files, Caveman hooks? Есть ли собственное повторное чтение после compaction?
3. Можно ли захватывать policy injection evidence через hook stdout и лог, а не только JSONL? Каков actual limit/truncation и compaction ordering?
4. Как избежать двух читателей одного policy source, конфликтов priority/order и утечки untrusted project content в developer context?
5. Если жаркое напоминание §2 каждые N substantive steps нужно, как измерить соблюдение vs overhead vs шум без избыточной инъекции?

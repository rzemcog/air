# Компактный handoff (агентный workflow)

## Цель / состояние

- `zapret-maintainer` приостановлен пользователем 18.10.2026 после ~9ч58м продолжения. Root завершил turn с `PAUSED_BY_USER`; новые AC не закрыты. Это результат транскрипта, **не** текущее наблюдение за машиной.
- AC `DONE` по финальному ledger: AC1, AC7, AC10, AC11 (исторически). Прочие, включая AC2, AC13: `NOT_DONE`.
- Конец run: AC2 child narrow capture/reap correction staged; live AC2 acceptance отсутствует. AC13 coordinator WIP, target compile обнаружил Ucode syntax error; не закрыт.
- Workflow audit 9h36 preliminary: Root 431 vs children 45 `apply_patch`, 29 `spawn_agent`, 68 `followup_task`, 38 compactions, 254 progress (67 >40 слов, ~110 sentence >20), Goal Observer вызван один раз. **Не final counts**. Итог: delegation nominally works, Root всё ещё исполнитель; §2 читался, но соблюдался слабо; observer не автономен.

## Утверждено

- `output-policy §2`: одно event/update, одно предложение по умолчанию, ≤20 слов/предложение; допустим второй sentence для результата/последствия; не объявлять skill/tool/проверки; `unsupported speculation`, не запрет доказанной неопределённости. §3 native Ultracave **без новых патчей**. Старый §6 удалён; provenance уже сделан.
- Отдельный local plugin `Agents Policies`: reuse `codex-rules`, только выбранные trust-listed sources. Native `AGENTS.md` остаётся Codex. MVP: `SessionStart(compact)` force reload full policies, scope-aware `SubagentStart`, `UserPromptSubmit` hot excerpts, hash/generation cache, policy-only trace. Сначала проверить runtime contracts и дублирование startup bootstrap.
- `UserPromptSubmit` не поддерживает intra-turn reminder внутри 10-часовой операции. Event/phase-based `PostToolUse` reinforcement **гипотеза**, не часть обязательного MVP.
- Основной config candidate `~/.agents/policies.toml`; UI не подтверждён, отложен. Plaintext agent-to-agent audit, MCP wrapper, Goal Observer, You Should Know, enforced delegation: отдельный backlog.
- Root по умолчанию оркестратор, однако policy loader сам не гарантирует такое поведение. Никогда не параллелить live mutations общего роутера/NFQUEUE.

## Следующая операция

1. Подтвердить фактическую версию Codex Desktop, hooks/плагины, установленные `.agents`, permissions. Read-only inspection, backup, diff against approved docs.
2. Изучить конкретный код/лицензию `https://github.com/code-yeongyu/codex-rules`, затем опционально `codex-subpath-agentsmd-hooks`, официальный hooks contract; переиспользовать минимальные части.
3. Реализовать `Agents Policies` с проверкой через isolated Windows test project, реальную delivery на compact/subagent и trace без raw secrets; compare model-visible and behavior separately. No Zapret execution.
4. Документировать tests/limitations/rollback. После плагина отдельно лечить Root delegation и observer independence.

## Границы данных

- Реальное содержимое рабочей системы и текущий `~/.agents` здесь отсутствуют. Все snapshots в `04_REFERENCES` помечены historical/proposed. Не применять их как current files без сравнения.
- Full forensic and delta отдельно в `03_EVIDENCE`; large JSONL только по необходимости через индекс исходников. Нельзя использовать reconstructed Git как доказательство выполнения live-тестов.

## Приложенные исходники

В отличие от предыдущей lean-версии, **все raw evidence для этого handoff находятся в ЭТОМ архиве**. См. `03_EVIDENCE/RAW_SOURCE_INDEX.md`; отдельные ZIP/7z прикладывать не требуется. Большие JSONL не читать при запуске.

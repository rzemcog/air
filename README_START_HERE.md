# START HERE: Agents Policies / workflow handoff (18.10.2026)

**Основной фокус:** исправить delivery/recovery правил в Codex Desktop Windows. **Zapret Maintainer = PAUSED_BY_USER**, не возобновлять ни AC, ни роутер без отдельного поручения.

## Порядок чтения (экономия контекста)

1. `HANDOFF_COMPACT_RU.md` (главный рабочий контекст).
2. `02_DECISIONS/ARCHITECTURE_DECISIONS_RU.md` (утверждения/гипотезы/отложенные идеи).
3. `01_CURRENT/AGENTS_POLICIES_TZ_RU.md` (ТЗ plugin) и `01_CURRENT/output-policy.md` (утверждённый артефакт).
4. `NEXT_SESSION_PROMPT_RU.md` для старта реализации.

**Только если возник конкретный вопрос**: `HISTORY/EVOLUTION_GRAPH.md`, `04_REFERENCES/*`, `03_EVIDENCE/*`, `git diff`, большой evidence-архив по `03_EVIDENCE/RAW_SOURCE_INDEX.md`.

## Важно

- `.git/` является **синтетической реконструкцией сохранившихся версий**, не оригинальной Git-историей машины пользователя. Читать `GIT_HISTORY_NOTICE.md` при использовании git evidence.
- `04_REFERENCES/bootstrap/` и `shared-historical/` = прежние/предложенные snapshots. Не устанавливать поверх актуальных `~/.agents` без сравнения.
- `01_CURRENT/output-policy.md` = **согласованный артефакт**, но его установка в пользовательскую систему не подтверждена.
- Полные 10-часовые логи умышленно исключены из лёгкого handoff. Размер архива ≠ размер model context; контекст расходуется при чтении. Эта структура избегает лишнего чтения.

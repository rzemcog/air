# START HERE: единый самодостаточный handoff (18.10.2026)

**Для новой сессии приложи только этот ZIP.** Другие архивы не требуются.

## Обязательное чтение (коротко)

1. `HANDOFF_COMPACT_RU.md`
2. `02_DECISIONS/ARCHITECTURE_DECISIONS_RU.md`
3. `01_CURRENT/AGENTS_POLICIES_TZ_RU.md`
4. `01_CURRENT/output-policy.md`

Далее использовать `NEXT_SESSION_PROMPT_RU.md`. Это и есть активный контекст.

## Не читать без конкретной необходимости

- `03_EVIDENCE/RAW_SOURCE_INDEX.md` даёт **локальные пути внутри ZIP** для полного 10-часового source 7z, трёх D1 JSONL и 24-часового forensic-архива. Исторические reports/skills/scans также внутри.
- `05_PRIMARY_EVIDENCE` хранит первичные доказательства; `06_HISTORICAL_REFERENCES` хранит только уникальные ранее собранные исходники.
- `HISTORY/EVOLUTION_GRAPH.md` и `.git` хранят реконструированную историю выбранных документов. Пожалуйста, не трактуй synthetic commits как git-log репозитория пользователя.

**Данные в ZIP не равны загруженному model context**: гигабайты логов не нужно читать, пока не требуется проверка конкретного утверждения.

`Zapret Maintainer`: PAUSED_BY_USER, AC2 и общий goal NOT_DONE. Не продолжать Zapret, SSH-mutating, `/goal`/AC, тесты на роутере. Следующая работа: только реализация `Agents Policies` и исправление workflow.

Актуальные `~/.agents` и working tree пользовательской Windows в ZIP отсутствуют. Приложенные файлы помечены historical/proposed или agreed artifact, их установку на ПК следует проверить.

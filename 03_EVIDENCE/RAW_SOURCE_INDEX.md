# Индекс исходных доказательств (не входят в компактный ZIP)

Это исходники *вне* данного ZIP. При необходимости приложить отдельный файл с указанным SHA-256. Ссылка на исходник не означает, что он автоматически доступен новой сессии.

- `прогона-закончен.7z` | 46926362 bytes | `sha256:bc95e4a1d7460963f1ed836c75f9ecd51c5597875ee76d1e48deb0c492679239` | Финальный транскрипт около 10 часов; полный source
- `codex_hermes_output_workflow_handoff_2026-10-18(1).zip` | 15427980 bytes | `sha256:06abb9872213f6c69a8314bba795e3bf508a5e16cd1bf425bc360d62188498ef` | Исторические 70 файлов; pre-current reference
- `agents-policies-complete-handoff-2026-10-18.zip` | 62505770 bytes | `sha256:72f02192b9b79bd4f85b3fdeb55422864ff81bc9d1654017ff580e2998f84a5f` | Предыдущий полный handoff 109 файлов; raw evidence и snapshots

Исторические архивы содержат дополнительные вложенные архивы и JSONL. Это evidence, а не обязательное чтение для Agents Policies.

### Сохранённые контрольные точки

- 9h36 срез Root: 431 root `apply_patch` vs 45 child; 29 `spawn_agent`; 68 `followup_task`; 38 compactions; 254 progress. Это **не** финальные totals.
- Финальный JSONL охватывает 03:06:09–13:03:45 UTC 18.10.2026; 60 unchanged / 4 changed / 1 added JSONL относительно 9h среза.
- 13:00:12 UTC safe-stop; к 13:03:45 Root reported `PAUSED_BY_USER`; AC1/AC7/AC10/AC11 DONE historically; остальные NOT_DONE.
- Конечная целевая ОС/версия роутера, production q300 PID, исторические root state см. только evidence, **не считать текущее состояние известным**.
- Поскольку old JSONL и full archival evidence не в этом ZIP, заключения здесь опираются на уже проведённый forensic, а не на повторный независимый разбор.

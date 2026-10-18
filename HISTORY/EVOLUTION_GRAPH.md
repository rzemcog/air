# Схема эволюции workflow и политик

**Это карта решений и результатов аудита, а не история каждой операции.**

```mermaid
flowchart TD
    A["Bootstrap: AGENTS → ENTRYPOINT → shared"] --> B["D1 / старый forensic: проблемы delivery и эффективности"]
    B --> C["Согласование §2 Caveman / §3 Ultracave"]
    C --> D["9ч36м срез: Root преобладает; §2 нарушается"]
    D --> E["До 13:03:45 UTC: завершающий delta, safe-stop"]
    E --> F["PAUSED_BY_USER; новых DONE нет"]
    F --> G["Принятое направление: Agents Policies MVP"]
    G --> H["Следующий шаг: reuse codex-rules; full, hot, subagent, trace"]
    H --> I["Отдельный backlog: Root delegation, Observer, Agent Audit"]
```

## Цепочка версий файлов, не execution evidence

```mermaid
flowchart LR
    O["Historical output-policy"] --> C["Candidate v2"]
    C --> A["Approved output-policy"]
    Q["Original bootstrap"] --> R["Proposed AGENTS + ENTRYPOINT"]
    R -.-> S["Сверка с реально установленной конфигурацией"]
    A --> S
```

Git tags (все synthetic): `snapshot-baseline` → `snapshot-bootstrap-proposed` → `snapshot-output-candidate` → `snapshot-approved-output` → `snapshot-handoff`. Это логически реконструированные versions; установка на ПК не подтверждалась.

Нужны реальные traces операции? Смотреть конкретный JSONL сегмент из внешнего evidence-архива, не Git diff.

# Адаптация instruction-conflict-resolution в AIR

Исходник: приложенный пользователем `SKILL(20261018-161925).md`, SHA256 `c8b1606cc28a8d7c2a5cebbae78dde4d7e8cae3a1373e0b34d777050c0a97047`. Взят только этот исходник, а не историческая догадка о версии skill.

Адаптация от 2026-10-22 (v0.2.0): удалена относительная ссылка на Shared Policy, добавлен контракт host-provided authority, поддержана эскалация из AIR, сохранены минимальная блокировка, ownership и ручное разрешение. Нормативная иерархия не дублируется. Для отсутствующего/недостоверного Shared Policy введена безопасная остановка только затронутого решения. Убрана связка metadata с конкретным harness; поиск skill выполняет native discovery host.

Полный применённый diff: [`../../changes/APPLIED_instruction_conflict_resolution.patch`](../../changes/APPLIED_instruction_conflict_resolution.patch).

**Shared Policy НЕ изменён.** Его адаптация отложена. Runtime discovery/visibility skill и Shared Policy потребуют эксперимента R8: см. [`../../docs/05_EXPERIMENTAL_TZ_RU.md`](../../docs/05_EXPERIMENTAL_TZ_RU.md). До этого runtime integration skill не доказана.

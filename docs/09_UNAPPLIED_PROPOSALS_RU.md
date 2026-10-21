<!-- @style: ./air.css -->
<!-- @script: ./air.js -->
<!-- @page: air-docs -->

# AIR — предложения по результатам критической проверки

**Статус:** `PROPOSED`, **в базовые документы не внесено**. Каждый файл `../proposals/Pxx_*.patch` содержит конкретную текстовую поправку к историческому базовому коммиту `4cbd0c7`. Эти изменения требуют отдельного обсуждения и согласия пользователя. В основном ТЗ уже упомянуты соответствующие *риски и тестовые blockers*, но не все предложенные способы их устранения.

| Патч | Суть предложения | Почему отдельно от принятой архитектуры | Файл |
|---|---|---|---|
| **P01** Semantic candidate coverage | Проверять семантически близкие операции разных vocabularies, даже если их registered IDs не совпадают. | Формальное значение `operation` не задаёт тождество смыслов между namespaces; поиск кандидатов с high recall ещё нужно спроектировать и измерить. | [`P01_semantic_coverage.patch`](../proposals/P01_semantic_coverage.patch) |
| **P02** Native authority | Для конфликтующих native instructions описать явную author-owned миграцию или blocker: фильтрация AIR Payload не устраняет native текст из модели. | Нет доказанного host-механизма удаления ранее доставленной native инструкции. | [`P02_native_authority.patch`](../proposals/P02_native_authority.patch) |
| **P03** Resolver latency | Сформулировать offline/precompile path при cache miss и проверить честный fail-visible режим, вместо синхронного LLM ожидания в каждом hook. | Стоимость и доступность дешёвой модели внутри synchronous hook неизвестны. | [`P03_resolver_latency.patch`](../proposals/P03_resolver_latency.patch) |
| **P04** Directive provenance | Добавить явную модель idempotency key, event ordering, fork lineage и scope как обязательное требование к Session State. | Нативная идентификация turns/forks ещё не проверена на Desktop. | [`P04_directives_provenance.patch`](../proposals/P04_directives_provenance.patch) |
| **P05** Unknown facts и permit | Принять 3-valued applicability и узкую семантику explicit `permit`; не схлопывать unknown с false. | Это нормативное решение, раньше пользователем не утверждено. | [`P05_unknown_and_permit.patch`](../proposals/P05_unknown_and_permit.patch) |
| **P06** Delivery evidence order | Поставить доказательство фактического model-visible transport как gate на заявление о готовом plugin, сохраняя параллельную разработку core. | ТЗ уже запрещает `DONE` без E2E; предложенный патч усиливает порядок acceptance. | [`P06_delivery_acceptance.patch`](../proposals/P06_delivery_acceptance.patch) |
| **P07** Manual corrections | Хранить user corrections отдельно от генерируемого `effective.md` с привязкой к source hashes и явной stale policy. | Формат UX/override не согласован. | [`P07_manual_corrections.patch`](../proposals/P07_manual_corrections.patch) |

**Состояние обсуждения:** ни один P01–P07 не принят. Применение не является частью стартового ТЗ. Исполнитель AIR должен исследовать соответствующие риски, но если реализация требует выбрать одну из неутверждённых моделей, фиксирует `BLOCKED_*` и запрашивает решение вместо молчаливого переноса предложенного патча в базу.

**Базовая применимость патчей:** предложения писались к раннему состоянию документации и не обязаны применяться к текущей редакции без перебазирования. Применённый patch skill хранится отдельно в [`../changes/APPLIED_instruction_conflict_resolution.patch`](../changes/APPLIED_instruction_conflict_resolution.patch) и НЕ входит в P01–P07.

**Коллизия при возможном rebase:** P01 добавлял probe с обозначением `R8`; в текущем экспериментальном ТЗ `R8` уже назначен проверке conflict-resolution skill. При обсуждении P01 потребуется выбрать новое обозначение.

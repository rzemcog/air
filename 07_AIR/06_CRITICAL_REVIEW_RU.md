# AIR — независимая критическая прожарка и предложения

**Правило:** это НЕ применённые изменения. Базовые документы `01`–`05` фиксируют обсуждённое; `PATCHES_UNAPPLIED/*.patch` содержат предложения Sol-6, которые требуют обсуждения и согласования.

## Где чертовски правы

**1. Граница Policy и Skill.** Policy отвечает, при каких условиях что обязательно, запрещено, разрешено или предпочтительно. Skill определяет способ и последовательность достижения результата. Это базовое архитектурное разделение языка правил и процедур исполнения.

**2. Grammar fixed, vocabulary extensible.** Это действительно разумная ось расширения. Она позволяет типизировать поведение, не захардкоживая все операции `test.run`/`docker.*` в AIR Core. Описания vocabulary нужны людям и semantic resolver, а Format Schema обеспечивает проверку формы.

**3. Source ownership/delivery разнесены.** Одна инструкция может влиять на GPA Resolution, но текст должен быть доставлен ровно одним назначенным транспортом. Очень важный антидубликационный invariant.

**4. Resolution Overlay и model-visible payload выполняют разные функции.** Root получает применимые инструкции; внутренняя карта решений обеспечивает воспроизводимость, анализ и ручную коррекцию.

**5. Два уровня кэширования и Session State.** Отдельные conflict decisions сокращают повторный семантический анализ. Директивы пользователя сохраняются в устойчивом состоянии сессии для compaction и resume.

**6. Замена `confidence` на формальный validation + user review.** Самооценка уверенности resolver малоценна; структурные гарантии и проверяемые артефакты существеннее. При этом semantic truth всё равно не доказана.

**7. Host/format/contracts разделены.** Стандарт Agent Plugins полезен на упаковке, а собственный AIR vocabulary остаётся внутренним языком; хорошая перспектива нескольких harness без premature host framework.

## Где ошибаемся или переоцениваем доказательства

### CR-01 (CRITICAL): candidate selection по equality of operation symbols может пропустить конфликт

`test.run` и `network.probe.execute` / `evidence.acquire` могут описывать перекрывающиеся действия, хотя имена разные. Особенно разные Extension Vocabularies. Детерминированные filters безопасны только если гарантированно не отсекут связанный конфликт. Иначе вся архитектура обещает, что resolver устранил конфликт, которого он даже не увидел.

**Предложение:** явный coverage contract: для совпадающих symbols всегда сравнить; для разных symbols применять bounded semantic discovery/declared relations; если не хватает покрытия — не утверждать «полностью resolved». Внутри `description` нельзя создавать невидимые operative constraints, которые полностью обходят структурные поля. См. `P01`.

### CR-02 (CRITICAL): resolved payload не может подавить конфликтующую native инструкцию

AIR умеет исключить global rule из **своего** payload, но уже native-delivered `AGENTS.md` может остаться в model context и спорить с Agent Profile. Это физический предел assembly. Developer self-delegation может помочь текущему user, но не делает native lower-priority rule исчезнувшей. У нас есть риск перепутать resolved view с модельной реальностью.

**Предложение:** моделировать `Effective Context` как native + AIR (+ user), а не только AIR body; проверять native native conflicts и при необходимости migrate authored source с approval. См. `P02`.

### CR-03 (HIGH): синхронный LLM resolver на lifecycle hook может быть плохой dependency

Hook должен отработать быстро и корректно. Если он дожидается сети/локальной модели, получаем новые точки отказа, задержку каждого первого prompt/compaction, гонки с session state. «Дешёвая модель» означает дешёвые токены, не обязательно низкую latency и стабильность.

**Предложение:** fast path strictly cache hit/validated LKG, cold path bounded; cache-miss policy обязана быть определена заранее, иначе заблокирован только требующий резолюции delivery branch. Не маскировать отсутствие resolver сырым конфликтующим bundle. См. `P03`.

### CR-04 (HIGH): `UserPromptSubmit` side-effect может записать неправильное состояние

Извлечение «persisting user directives» из естественного диалога включает scope, отмены, ссылки «теперь так», неоднозначность и state races. При ошибке cheap model session state будет устойчиво хранить ложное утверждение. Дополнительно root context уже может не соответствовать state при fork/parallel turns/resume.

**Предложение:** явно определить idempotent event identity/generation, атомарный compare-and-swap, provenance, область действия, manual inspection и запрет на выдачу неподтверждённого state как точной цитаты. См. `P04`.

### CR-05 (HIGH): `permit` семантически не равен «сними запрет»

В деонтической логике permission не обязательно отменяет обязательство или запрет; иначе наша модель внедрит неконтролируемый override. Разрешение выполнить действие не предписывает его выполнить. Порядок source authority разрешает конфликт, но только после доказательства пересечения applicability.

**Предложение:** описать `permit` как explicit exception только при явной matching target, иначе как permissive statement; включить конфликтные fixtures. Для unknown facts задать fail-closed/fail-open semantics по типу правила, а не вычислять false молча. См. `P05`.

### CR-06 (MEDIUM-HIGH): «deterministic fields» не значит «deterministic domain facts»

`agent.role` может не прийти из `SubagentStart`; `task.kind` часто является semantic inference; `relevant`/`sufficient` — субъективные selectors, даже если имеют type `identifier`. Если schema принимает произвольный `identifier`, это не доказательство, что система знает его фактический смысл.

**Предложение:** classification `observed fact / configured fact / inferred fact`, tri-state applicability `true/false/unknown` и запрет выдавать unknown за false. См. `P05`.

### CR-07 (MEDIUM): fine-grained cache decisions контекстно зависимы

Pair-hash reuse невалиден при изменении третьего правила, scope, authority policy или схемы. Full-bundle cache проще. Не создавать графовую БД; сначала измерить, окупает ли precision cache cost.

**Предложение:** dependency/context fingerprint и conservative invalidation; отдельно сохранять `equivalent` и `conflict`. См. `P01` и `P03`.

### CR-08 (MEDIUM): множество уровней/schema/vocabulary/IR/graph может задержать главный fix

Историческая подтверждённая проблема — delivery recovery, а полноценный structured language ещё гипотеза. Пользователь согласен реформировать policy format, но не доказано, что all-policy migration нужна для первого рабочего hook. Поэтому единый агентский процесс должен реализовывать независимые компоненты, не игнорируя критические transport blockers. Это не требование разделить работу на две отдельные пользовательские стадии.

**Предложение:** acceptance criteria выстроить по dependency graph и дать `BLOCKED` для неподдерживаемого transport, не «доделывать DSL вместо нужного recovery». См. `P06`.

### CR-09 (MEDIUM): «весь natural language только в description» слишком категорично без разграничения labels

Human-readable names в YAML, descriptions vocabulary, user-facing error messages неизбежно содержат natural language. Не вся строка — нормативное правило. Сам детерминированный parser может хранить free-text label, но не использовать его для control decisions. Нужны 2 категории: nonnormative `display/description` и normative `description` внутри Rule; semantic resolver получает их с разными trust tags.

**Предложение:** explicit trust/role tagging semantic text. См. `P01`.

### CR-10 (MEDIUM): portable plugin manifest != host-neutral AIR

Root `plugin.json` даёт package boundary, но hooks всё равно host-specific и version/trust dependent. Нельзя отсюда автоматически вывести поддержку Hermes или portable semantic scope. Переносимость core проверяется контрактным тестом, не названием файла.

**Предложение:** portable package and Codex Integration separate interface; не создавать абстрактный framework до второго harness. В базовом документе это уже почти верно; отдельный patch не требуется.

### CR-11 (MEDIUM): ручное исправление generated `effective.md` теряется

Простой edit generated file и rebuild создают конфликт с кэшем. Потребуется отдельный assertion/override artifact с pinned source/context hash, author и explicit activation. Не применять старую correction к другим hash без review. См. `P07`.

### CR-12 (MEDIUM): роль developer может превратить не доверенный project текст в более сильную инструкцию

Структура YAML и human-readable description из репозитория — тоже входные данные. Скомпилированный project policy через developer `additionalContext` может получить больше власти, чем native project AGENTS. Нужен explicit trust-list и ограничение source authority; возможность отказа. См. `P02`.

## Замечания по порядку обсуждения

- Много прежних «очевидных» инвариантов оказалось инвариантами **пожелания**, а не verified host contract. Отлично, что теперь введены runtime gates.
- Слишком быстро предлагалась полная семантическая дедупликация в hook. Нужно выровнять costs/latency/errors, а не оптимизировать tokens ценой блокировки session.
- Граф полезен как способ представления отношений, но иногда 2 maps и список edge tuples эффективнее и надёжнее.
- Нельзя продавать «полная детерминированность» там, где домен описывается свободным `description`, а действие классифицируется LLM.

## Индекс НЕПРИМЕНЁННЫХ патчей

| Файл | Меняет | Что предлагаю |
|---|---|---|
| `P01_semantic_coverage.patch` | `01_AIR_ARCHITECTURE_RU.md` | Не обещать полноту конфликтов при exact-symbol candidate selection; ограничить semantic relation и provenance. |
| `P02_authority_native.patch` | `01_AIR_ARCHITECTURE_RU.md` | Блокировать невоспроизводимый resolved vs native контекст и исключить elevation project data. |
| `P03_resolver_cache_miss.patch` | `03_AGENT_IMPLEMENTATION_TZ_RU.md` | Fast-path и bounded cold resolver; cache miss error policy. |
| `P04_session_state_provenance.patch` | `03_AGENT_IMPLEMENTATION_TZ_RU.md` | Конкурентность, idempotence, ambiguous directives; защита состояния. |
| `P05_tristate_permit.patch` | `01_AIR_ARCHITECTURE_RU.md` | Tri-state applicability и явный контракт разрешений. |
| `P06_delivery_first_acceptance.patch` | `03_AGENT_IMPLEMENTATION_TZ_RU.md` | Acceptance dependency order без второго «этапа». |
| `P07_manual_corrections.patch` | `01_AIR_ARCHITECTURE_RU.md` | Manual assertion sidecar поверх generated artifacts. |

**Это именно предложения.** Ни один patch не применён к базовым документам и не превращён автоматически в ADR. Для принятия выбрать патч и обсудить корректировку. Можно принимать по одному.

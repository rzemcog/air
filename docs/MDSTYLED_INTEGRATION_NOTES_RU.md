<!-- @style: ./air.css -->
<!-- @script: ./air.js -->
<!-- @page: air-docs -->

# Интеграция AIR Docs с MdStyled

## Проверенный контракт по исходному коду

Исходный репозиторий: https://github.com/OsamaAbuSitta/MDStyled (проверен 2026-10-22).

- `src/engine/config.ts`: `<!-- @style: ./air.css -->` извлекается из Markdown; путь разрешается относительно каталога Markdown-файла.
- `src/engine/renderer.ts`: CSS читается из файла через `fs.promises.readFile` и встраивается в `<style>` **самим расширением**. Это штатное поведение, отличное от ручного `<style>` в документации.
- `src/previewProvider.ts`: HTML проходит через `sanitize-html`; разрешены `id`, `class`, `style`, `href` и узкий набор `data-*`. Произвольные `data-air-*` отсутствуют в списке; переключатели AIR поэтому реализованы без них.
- `src/previewProvider.ts`: в DevTools есть диагностическое сообщение `[MdStyled] Preview loaded, CSS length: ... bytes`.

## Что изменено в AIR

1. Один источник оформления `docs/air.css`; один источник интерактивности `docs/air.js`.
2. Удалены все ручные `<style>` в Markdown, в том числе fallback, и дублирующий `mdstyled.config.json`.
3. Сценарные переключатели используют ссылки `<a>` и классы, сохранённые sanitization.
4. Диагностика не симулирует CSS: [`00_RENDER_TEST_RU.md`](00_RENDER_TEST_RU.md) показывает отсутствие внешнего CSS именно как отсутствие внешнего CSS.

## Не подтверждено

Фактическое поведение локальной версии MDStyled в Windows VS Code. Исправление интеграции сделано на основе текущего публичного исходного кода; пользовательский runtime пока не наблюдался.

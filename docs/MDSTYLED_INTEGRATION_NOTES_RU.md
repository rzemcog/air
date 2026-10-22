<!-- @style: ./air.css -->
<!-- @script: ./air.js -->

# Интеграция AIR Docs с MdStyled

## Проверенный контракт по исходному коду

Исходный репозиторий: https://github.com/OsamaAbuSitta/MDStyled (проверен 2026-10-22).

- `src/engine/config.ts`: `<!-- @style: ./air.css -->` извлекается из Markdown; путь разрешается относительно каталога Markdown-файла.
- `src/engine/renderer.ts`: CSS читается из файла через `fs.promises.readFile` и встраивается в `<style>` **самим расширением**. Это штатное поведение, отличное от ручного `<style>` в документации.
- `src/previewProvider.ts`: HTML проходит через `sanitize-html`; разрешены `id`, `class`, `style`, `href` и узкий набор `data-*`. Произвольные `data-air-*` отсутствуют в списке; переключатели AIR поэтому реализованы без них.
- `src/previewProvider.ts`: диагностическое сообщение `[MdStyled] Preview loaded, CSS length: ... bytes` включает CSS встроенных расширений и само по себе не доказывает загрузку `air.css`.
- `src/engine/renderer.ts`: оболочка `<div class="mdstyled-root">` не содержит класса `air-docs`. Директива `@page` поддерживается `src/engine/transformer.ts` и создаёт дополнительную вложенную оболочку `.mdstyled-root.PAGE_CLASS`. Внешний `.mdstyled-root` существует всегда; тема AIR сейчас использует его.
- `src/engine/index.ts` выбирает `options.templateOverride` **вместо** CSS/JS документа. `src/extension.ts` использует этот режим для `MdStyled Edit`, а `MdStyled: Open Preview` сбрасывает override. У встроенных интерактивных шаблонов есть оглавление «ON THIS PAGE» и сворачиваемые заголовки.
- Диагностика отдельно проверяет `window.mdstyled`, `--air-css-loaded` и `--air-root-css-ready`.

## Что изменено в AIR

1. Один источник оформления `docs/air.css`; один источник интерактивности `docs/air.js`.
2. Удалены все ручные `<style>` в Markdown, в том числе fallback, и дублирующий `mdstyled.config.json`.
3. В предыдущей ревизии ошибочно удалили поддерживаемую директиву `@page`; корневые селекторы привязаны к `.mdstyled-root`; пробы проверяют загрузку файла и применение CSS отдельно.
4. Сценарные переключатели используют ссылки `<a>` и классы, сохранённые sanitization.
5. Диагностика не симулирует CSS: [`00_RENDER_TEST_RU.md`](00_RENDER_TEST_RU.md) показывает отсутствие внешнего CSS именно как отсутствие внешнего CSS.

## Не подтверждено

По скриншоту пользователя кастомные стили и JS AIR не применены, но проявляются элементы встроенного шаблона. Подмена через `templateOverride` подтверждена исходниками, фактическая команда открытия пользователем не подтверждена. Проверка обычного `MdStyled: Open Preview` ещё требуется. Фактическое поведение локальной версии MDStyled в Windows VS Code. Исправление интеграции сделано на основе текущего публичного исходного кода; пользовательский runtime пока не наблюдался.

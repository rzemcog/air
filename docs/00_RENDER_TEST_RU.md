<!-- @style: ./air.css -->
<!-- @script: ./air.js -->

# Диагностика внешних CSS и JavaScript в MdStyled

Это минимальная проверка **реального подключения файлов**, а не fallback с тем же CSS внутри Markdown. Открывать командой **MdStyled: Open Preview**.

## 1. CSS отдельно от JavaScript

<div id="air-css-probe" class="air-css-probe">Контрольная область внешнего CSS</div>

Если `air.css` загрузился, появится **зелёная карточка с толстой бирюзовой рамкой и надписью «CSS ПОДКЛЮЧЕН»**. При отсутствии CSS останется обычный текст. Для этой проверки JS не требуется.

## 2. JavaScript и независимая проверка CSS

<div class="air-js-probe">JavaScript: <strong id="air-js-status">не подтверждён</strong>. MdStyled runtime: <strong id="air-renderer-status">не проверен</strong>. CSS-файл: <strong id="air-css-status">не проверен</strong>. Корневой CSS: <strong id="air-root-status">не проверен</strong>.</div>

Если JS исполняется, появится «подтверждён». Затем JS независимо проверит API `window.mdstyled`, CSS-переменную из **внешнего** `air.css` и CSS-переменную корневого `.mdstyled-root`.

## 3. Как диагностировать сбой в установленном расширении

1. Открой **Help → Toggle Developer Tools → Console**.
2. Найди `[MdStyled] Preview loaded, CSS length: ... bytes` и `[AIR] external CSS: loaded/missing`. Значение `CSS length` включает CSS встроенных расширений и само по себе **не подтверждает** загрузку `air.css`.
3. Если CSS length мал или в составе CSS есть `Failed to load`, проверь разрешение путей `./air.css` относительно этого `.md`.
4. Если CSS length достаточный, но карточки нет, проверь итоговый `<style>` и CSS errors в DevTools: проблема возникает после чтения файла, в рендере/санитизации.
5. Если CSS-файл подтверждён, а корневой CSS нет, проверь `.mdstyled-root` в итоговом DOM. MDStyled 1.0.1 не реализует директиву `@page`.
6. Если нет диагностических сообщений, проверь версию расширения и то, что открыт именно **MdStyled Preview**, а не встроенный Markdown Preview.

**Ограничение:** эти проверки не заменяют фактического теста в установленной пользователем версии MDStyled.

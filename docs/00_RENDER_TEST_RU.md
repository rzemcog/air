<!-- @style: ./air.css -->
<!-- @script: ./air.js -->
<!-- @page: air-docs -->

# Проверка оформления MdStyled

Откройте через **MdStyled: Open Preview**. Три проверки ниже помогают локализовать проблему. В обычном VS Code Markdown Preview результат может отличаться.

<div style="background:#233247;border:1px solid #6481ac;color:#fff;padding:14px;border-radius:12px;margin:16px 0">
  <strong style="display:block">A. Встроенный стиль</strong>
  Если этот текст находится в тёмной карточке с рамкой, расширение сохраняет HTML и inline CSS.
</div>

<div class="air-node air-node--core" style="margin:12px 0">
  <strong>B. Внешний air.css</strong><small>Должна быть самостоятельная карточка с фиолетовой рамкой и внутренними отступами. Если сплошной текст, внешний CSS не загрузился.</small>
</div>

<div id="air-js-check" style="padding:12px;border:1px solid #62758e;border-radius:10px;margin:12px 0">
  C. JavaScript: <span id="air-js-status">не подтверждён</span>
</div>

<details>
<summary>Диагностика в VS Code</summary>

1. Откройте Help → Toggle Developer Tools → Console.
2. Проверьте ошибки вида `Failed to load`, `Refused to apply style`, CSP и `air.css`.
3. При необходимости закройте и откройте MdStyled Preview снова.

</details>

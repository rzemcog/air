/* Optional enhancement only. All architecture diagrams are readable without JS. */
(() => {
  const init = () => {
    document.querySelectorAll('.air-visual[data-air-filterable]').forEach((flow) => {
      flow.classList.add('air-enhanced');
      flow.querySelectorAll('.air-flow-tools[hidden]').forEach(tools => tools.removeAttribute('hidden'));
      flow.querySelectorAll('[data-air-filter]').forEach(btn => {
        btn.setAttribute('aria-pressed', btn.dataset.airFilter === 'all' ? 'true' : 'false');
      });
    });
  };
  document.addEventListener('click', (event) => {
    const button = event.target.closest('[data-air-filter]');
    if (!button) return;
    const flow = button.closest('.air-visual[data-air-filterable]');
    if (!flow) return;
    const focus = button.dataset.airFilter;
    flow.dataset.airActivePath = focus;
    flow.querySelectorAll('[data-air-filter]').forEach(b => {
      b.setAttribute('aria-pressed', String(b === button));
    });
    flow.querySelectorAll('.air-path[data-air-path]').forEach(lane => {
      lane.classList.toggle('air-dimmed', focus !== 'all' && lane.dataset.airPath !== focus);
    });
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true});
  else init();
})();

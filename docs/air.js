/* MdStyled-compatible: use class/id/href; sanitizer strips custom data-* attributes. */
(() => {
  const filterKeys = ['all','hit','deterministic','semantic','blocked','confirmed','refuted','unknown'];
  function init(){
    document.querySelectorAll('.air-visual.air-filterable').forEach(flow=>{
      flow.classList.add('air-enhanced');
      flow.querySelectorAll('.air-flow-filter--all').forEach(a=>a.setAttribute('aria-pressed','true'));
    });
  }
  document.addEventListener('click',event=>{
    const link=event.target.closest('a.air-flow-filter');
    if(!link)return;
    const flow=link.closest('.air-visual.air-filterable');
    if(!flow)return;
    event.preventDefault();
    const key=filterKeys.find(k=>link.classList.contains('air-flow-filter--'+k));
    if(!key)return;
    flow.querySelectorAll('.air-flow-filter').forEach(a=>a.setAttribute('aria-pressed',String(a===link)));
    flow.querySelectorAll('.air-path').forEach(lane=>{
      lane.classList.toggle('air-dimmed',key!=='all' && !lane.classList.contains('air-lane--'+key));
    });
  });
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();

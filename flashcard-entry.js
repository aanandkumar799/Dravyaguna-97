document.addEventListener('DOMContentLoaded',()=>{
  const params=new URLSearchParams(window.location.search);
  if(params.get('mode')!=='flash') return;
  const flashButton=document.querySelector('[data-mode="flash"]');
  if(!flashButton) return;
  flashButton.click();
  const target=document.getElementById('quick-revision')||document.getElementById('search');
  if(target) requestAnimationFrame(()=>target.scrollIntoView({behavior:'smooth',block:'start'}));
});

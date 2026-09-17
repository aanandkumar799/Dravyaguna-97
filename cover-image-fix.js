/* Dravyaguna-97: homepage cover images use the static curated registry only. */
(function(){'use strict';
const key=u=>String(u||'').split('?')[0].toLowerCase();
async function load(){
  const list=document.getElementById('plant-list');
  if(!list)return;
  try{
    const r=await fetch(new URL('data/curated-image-manifest.json',location.href),{cache:'no-store'});
    if(!r.ok)return;
    const manifest=await r.json();
    const records=new Map((manifest.records||[]).map(x=>[`${String(x.plant_id).toLowerCase()}::${x.part}`,x]));
    const cards=[...list.querySelectorAll('.plant-card')];
    await Promise.all(cards.map(async card=>{
      const link=card.querySelector('a.view-plant[href*="plant.html?id="]');
      const img=card.querySelector('.plant-image img');
      if(!link||!img)return;
      const id=new URL(link.href,location.href).searchParams.get('id');
      const rec=records.get(`${String(id||'').toLowerCase()}::whole_plant`);
      if(!rec){img.removeAttribute('src');img.alt=(img.alt||id||'Plant')+' — curated image unavailable';return;}
      const candidates=Array.isArray(rec.image_path_candidates)?rec.image_path_candidates:(rec.image_path?[rec.image_path]:[]);
      for(const raw of candidates){
        const u=new URL(raw,location.href).href;
        if(key(u)===key(img.src))return;
        const ok=await new Promise(resolve=>{const probe=new Image();probe.onload=()=>resolve(true);probe.onerror=()=>resolve(false);probe.src=u});
        if(ok){img.src=u;img.dataset.curated='true';img.removeAttribute('data-fallback');img.title='Curated repository image';return;}
      }
      img.removeAttribute('src');img.alt=(img.alt||id||'Plant')+' — curated image unavailable';
    }));
  }catch(e){console.warn('Curated cover registry unavailable',e)}
}
function start(){let tries=0;const timer=setInterval(()=>{if(document.getElementById('plant-list')){clearInterval(timer);load()}else if(++tries>50)clearInterval(timer)},200)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();

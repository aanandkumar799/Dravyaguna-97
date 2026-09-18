/* Dravyaguna-97: cover images are registry-controlled and verification-gated. */
(function(){'use strict';
const url=file=>new URL(file,location.href).href;
const norm=v=>String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/\s+/g,' ').trim();
function placeholder(label){return new URL('favicon.svg',location.href).href;}
async function get(file){try{const r=await fetch(url(file),{cache:'no-store',headers:{Accept:'application/json'}});return r.ok?await r.json():null}catch(e){return null}}
async function load(){
  const list=document.getElementById('plant-list');if(!list)return;
  const [manifest,plants]=await Promise.all([get('data/curated-image-manifest.json?v=5'),get('plants.json?v=97')]);
  const records=Array.isArray(manifest?.records)?manifest.records:[];
  const approved=new Map();
  for(const r of records){
    if(!r||String(r.part)!=='whole_plant'||!(r.image_path||r.source_media_url))continue;
    if(!['verified','verified-external','verified-local'].includes(String(r.verification_status||'').toLowerCase()))continue;
    if(!r.source_url||!r.source_name||!r.verified_botanical_name)continue;
    const id=String(r.plant_id||'');if(id&&!approved.has(id))approved.set(id,r);
  }
  const plantMap=new Map((Array.isArray(plants)?plants:[]).map(p=>[String(p?.id||''),p]));
  const cards=[...list.querySelectorAll('.plant-card')];
  await Promise.all(cards.map(async card=>{
    const link=card.querySelector('a.view-plant[href*="plant.html?id="]');
    const img=card.querySelector('.plant-image img');if(!link||!img)return;
    const id=new URL(link.href,location.href).searchParams.get('id');
    const rec=approved.get(String(id||''));
    const plant=plantMap.get(String(id||''))||await get(`data/plants/${encodeURIComponent(id||'')}.json?v=97`);
    const actual=norm(plant?.identity?.botanical_name||plant?.botanical_name||'');
    if(!rec||!actual||norm(rec.verified_botanical_name)!==actual){
      img.src=placeholder(plant?.identity?.name||plant?.name||id||'Plant');
      img.alt=(plant?.identity?.name||plant?.name||id||'Plant')+' — verified plant photograph unavailable';
      img.removeAttribute('data-curated');
      return;
    }
    img.src=rec.image_path||rec.source_media_url;img.dataset.curated='true';img.dataset.verified='true';img.title='✓ Exact botanical species verified • Whole plant • '+rec.source_name;
    img.addEventListener('error',()=>{img.src=placeholder(plant?.identity?.name||plant?.name||id||'Plant');img.removeAttribute('data-curated');},{once:true});
  }));
}
function start(){let tries=0;const timer=setInterval(()=>{if(document.getElementById('plant-list')){clearInterval(timer);load()}else if(++tries>50)clearInterval(timer)},200)}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();

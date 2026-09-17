(()=>{
  'use strict';
  async function get(url){try{const r=await fetch(url,{cache:'no-store'});return r.ok?await r.json():null}catch(e){return null}}
  function plantId(img){
    const explicit=img.dataset.plantId||img.closest('[data-plant-id]')?.dataset?.plantId;
    if(explicit)return String(explicit);
    const link=img.closest('.plant-card')?.querySelector('a.view-plant[href*="id="]');
    if(link){try{return String(new URL(link.href,location.href).searchParams.get('id')||'')}catch(e){}}
    return '';
  }
  async function verify(){
    const list=document.getElementById('plant-list');if(!list)return;
    const manifest=await get('data/curated-image-manifest.json');
    const records=Array.isArray(manifest?.records)?manifest.records:[];
    const approved=new Map();
    for(const r of records){
      if(r?.part!=='whole_plant'||!r.image_path||!['verified','verified-external'].includes(r.verification_status))continue;
      const key=String(r.plant_id);if(!approved.has(key))approved.set(key,r);
    }
    list.querySelectorAll('img[data-botanical]').forEach(img=>{
      const pid=plantId(img),r=approved.get(pid);
      if(!r){img.removeAttribute('src');img.alt=(img.alt||'Plant')+' — verified exact-species photograph unavailable';return;}
      img.src=r.image_path;img.dataset.verified='true';img.dataset.source=r.source_url;img.title='✓ Exact species verified • Whole plant • '+(r.source_name||'verified source');
      img.addEventListener('error',()=>{img.removeAttribute('src');img.alt=(img.alt||'Plant')+' — approved photograph unavailable';},{once:true});
    });
  }
  const run=()=>setTimeout(verify,100);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  const target=document.getElementById('plant-list')||document.body;new MutationObserver(run).observe(target,{childList:true,subtree:true});
})();
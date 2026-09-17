(()=>{
  'use strict';
  const root=location.pathname.replace(/[^/]*$/,'');
  const url=file=>new URL(file,location.href).href;
  async function get(file){try{const r=await fetch(url(file),{cache:'no-store',headers:{Accept:'application/json'}});return r.ok?await r.json():null}catch(e){return null}}
  const norm=v=>String(v||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/\s+/g,' ').trim();
  function plantId(img){
    const explicit=img.dataset.plantId||img.closest('[data-plant-id]')?.dataset?.plantId;
    if(explicit)return String(explicit);
    const link=img.closest('.plant-card')?.querySelector('a.view-plant[href*="id="]');
    if(link){try{return String(new URL(link.href,location.href).searchParams.get('id')||'')}catch(e){}}
    return '';
  }
  async function verify(){
    const list=document.getElementById('plant-list');if(!list)return;
    const manifest=await get('data/curated-image-manifest.json?v=2');
    const records=Array.isArray(manifest?.records)?manifest.records:[];
    const approved=new Map();
    for(const r of records){
      if(!r||String(r.part)!=='whole_plant'||!r.image_path||!/^https?:\/\//i.test(String(r.image_path)))continue;
      if(!['verified','verified-external'].includes(String(r.verification_status)))continue;
      if(!r.source_url||!r.source_name||!r.verified_botanical_name)continue;
      const key=String(r.plant_id||'');
      if(key&&!approved.has(key))approved.set(key,r);
    }
    const imgs=[...list.querySelectorAll('img[data-botanical],img[data-plant-id]')];
    await Promise.all(imgs.map(async img=>{
      const pid=plantId(img),r=approved.get(pid);if(!pid)return;
      let plant=null;
      try{plant=await get(`data/plants/${encodeURIComponent(pid)}.json?v=97`)}catch(e){}
      const actual=norm(plant?.identity?.botanical_name||plant?.botanical_name||img.dataset.botanical||'');
      if(!r||!actual||norm(r.verified_botanical_name)!==actual){
        img.src=`data:image/svg+xml;charset=UTF-8,${encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#edf5ef"/><text x="400" y="220" text-anchor="middle" font-family="Arial,sans-serif" font-size="76">🌿</text><text x="400" y="305" text-anchor="middle" font-family="Arial,sans-serif" font-size="30" fill="#1b4332">${img.alt||'Plant'}</text><text x="400" y="350" text-anchor="middle" font-family="Arial,sans-serif" font-size="18" fill="#6b756f">Verified cover photo not yet approved</text></svg>`)}`;
        img.alt=(img.alt||'Plant')+' — verified whole-plant photograph unavailable';
        img.removeAttribute('data-cover-verified');
        img.dataset.coverUnavailable='true';
        return;
      }
      img.src=r.image_path;img.dataset.coverVerified='true';img.dataset.source=r.source_url;img.title='✓ Exact botanical species verified • Whole plant • '+r.source_name;
      img.addEventListener('error',()=>{img.src=`data:image/svg+xml;charset=UTF-8,${encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520"><rect width="800" height="520" fill="#edf5ef"/><text x="400" y="260" text-anchor="middle" font-family="Arial,sans-serif" font-size="24" fill="#1b4332">Approved photograph unavailable</text></svg>')}`;img.removeAttribute('data-cover-verified');},{once:true});
    }));
  }
  const run=()=>setTimeout(verify,80);
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',run);else run();
  const target=document.getElementById('plant-list')||document.body;
  new MutationObserver(run).observe(target,{childList:true,subtree:true});
})();

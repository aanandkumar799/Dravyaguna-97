(()=>{
  'use strict';
  const esc=v=>String(v??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#039;');
  async function get(url){try{const r=await fetch(url,{cache:'no-store'});return r.ok?await r.json():null}catch(e){return null}}
  async function verify(){
    const list=document.getElementById('plant-list');if(!list)return;
    const [index,manifest]=await Promise.all([get('plant-index.json'),get('data/curated-image-manifest.json')]);
    const records=Array.isArray(manifest?.records)?manifest.records:[];
    const approved=new Map();
    for(const r of records){
      if(!r?.image_path||!['verified','verified-external'].includes(r.verification_status))continue;
      if(r.part!=='whole_plant')continue;
      const key=String(r.plant_id);if(!approved.has(key))approved.set(key,r);
    }
    list.querySelectorAll('img[data-botanical]').forEach(img=>{
      const card=img.closest('[data-plant-id],.plant-card,article,li')||img.parentElement;
      const pid=img.dataset.plantId||card?.dataset?.plantId||'';
      const r=approved.get(String(pid));
      if(!r){img.removeAttribute('src');img.alt=(img.alt||'Plant')+' — verified whole-plant photograph unavailable';return;}
      img.src=r.image_path;img.dataset.verified='true';img.dataset.source=r.source_url;img.title='Verified exact-species whole-plant photograph — '+(r.source_name||'source');
      img.addEventListener('error',()=>{img.removeAttribute('src');img.alt=(img.alt||'Plant')+' — approved image unavailable';},{once:true});
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',verify);else verify();
  const target=document.getElementById('plant-list')||document.body;new MutationObserver(()=>verify()).observe(target,{childList:true,subtree:true});
})();
(()=>{
  'use strict';
  const PARTS=[
    ['whole_plant','Whole plant','Exact species; overall specimen must be visible.'],
    ['habit','Habit / growth form','Exact species; growth architecture must be visible.'],
    ['root','Root','Exact species; actual root must be documented.'],
    ['stem','Stem / twig','Exact species; stem or twig must be documented.'],
    ['leaf','Leaf','Exact species; diagnostic leaf morphology must be visible.'],
    ['flower','Flower / inflorescence','Exact species; actual flower or inflorescence must be visible.'],
    ['fruit','Fruit','Exact species; actual fruit must be visible.'],
    ['seed','Seed','Exact species; actual seed must be documented.'],
    ['bark','Bark','Exact species; bark character must be visible.']
  ];
  const BAD=/\b(map|diagram|microscope|histology|chemical|medicine|tablet|capsule|powder|painting|logo|flag|person|animal|poster|chart|illustration|drawing|herbarium\s+sheet)\b/i;
  const root=location.pathname.replace(/[^/]*$/,'');
  const esc=v=>String(v??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#039;');
  const host=()=>document.getElementById('plant-gallery-host')||document.querySelector('.image-gallery');
  async function get(url){try{const r=await fetch(url,{cache:'no-store',headers:{Accept:'application/json'}});return r.ok?await r.json():null}catch(e){return null}}
  function validRecord(r,pid,botanical,part){
    if(!r||String(r.plant_id)!==pid||String(r.part)!==part||!r.image_path)return false;
    if(!/^https?:\/\//i.test(r.image_path))return false;
    if(String(r.verification_status||'')!=='verified-external'&&String(r.verification_status||'')!=='verified')return false;
    if(String(r.verified_botanical_name||'').trim().toLowerCase()!==String(botanical||'').trim().toLowerCase())return false;
    if(!r.source_url||!r.source_name)return false;
    if(BAD.test(String(r.title||'')+' '+String(r.source_name||'')))return false;
    return true;
  }
  function sourceLabel(r){return `${esc(r.source_name||'Verified source')} ✓`}
  function card(name,label,note,r){
    if(!r)return `<figure class="gallery-item botanical-missing"><div class="image-loading">🌿 Verified photograph unavailable</div><figcaption><strong>${esc(label)}</strong><small>${esc(note)}</small><small>No sufficiently verified species-and-part image is currently approved.</small></figcaption></figure>`;
    return `<figure class="gallery-item botanical-verified"><img src="${esc(r.image_path)}" alt="${esc(name+' — '+label)}" loading="lazy" decoding="async" class="plant-gallery-image"><figcaption><strong>${esc(label)}</strong><small>${esc(note)}</small><a class="gallery-source" href="${esc(r.source_url)}" target="_blank" rel="noopener noreferrer">Source: ${sourceLabel(r)} ↗</a></figcaption></figure>`;
  }
  async function build(){
    const h=host();if(!h)return;
    const id=new URLSearchParams(location.search).get('id');if(!id)return;
    h.innerHTML='<div class="image-loading" style="grid-column:1/-1">🔎 Loading only independently verified botanical photographs…</div>';
    const p=await get(`${root}data/plants/${encodeURIComponent(id)}.json`);if(!p){h.innerHTML='';return;}
    const index=await get(`${root}plant-index.json`);const manifest=await get(`${root}data/curated-image-manifest.json`);
    const ref=(index?.plants||[]).find(x=>String(x?.id)===String(id));
    const botanical=String(p?.identity?.botanical_name||p?.botanical_name||ref?.botanical_name||'').trim();
    const name=String(p?.identity?.name||p?.name||ref?.name||id).trim();
    const records=Array.isArray(manifest?.records)?manifest.records:[];
    const used=new Set();const approved={};
    for(const [part,label,note] of PARTS){
      const candidates=records.filter(r=>validRecord(r,String(id),botanical,part));
      const r=candidates.find(x=>!used.has(String(x.image_path)));
      if(r){used.add(String(r.image_path));approved[part]=r;}
    }
    h.innerHTML=PARTS.map(([part,label,note])=>card(name,label,note,approved[part])).join('');
    h.querySelectorAll('img.plant-gallery-image').forEach(img=>{
      img.addEventListener('error',()=>{const f=img.closest('.gallery-item');if(f){f.classList.remove('botanical-verified');f.classList.add('botanical-missing');f.innerHTML='<div class="image-loading">🌿 Verified photograph unavailable</div><figcaption><strong>Image removed</strong><small>The approved source could not be loaded.</small></figcaption>';}});
      img.addEventListener('click',()=>{const modal=document.getElementById('image-modal'),mi=document.getElementById('modal-image');if(modal&&mi){mi.src=img.currentSrc||img.src;mi.alt=img.alt;modal.classList.add('show');modal.setAttribute('aria-hidden','false');document.getElementById('close-modal')?.focus();}});
    });
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',build);else build();
})();
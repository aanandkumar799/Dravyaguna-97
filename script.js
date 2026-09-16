document.addEventListener('DOMContentLoaded', () => {
  const plantList = document.getElementById('plant-list');
  const searchInput = document.getElementById('searchInput') || document.getElementById('search');
  if (!plantList) return;

  const databaseURL = new URL('plants.json', window.location.href).href;
  let masterPlants = [];
  let searchTimer = null;
  let showAllPlants = false;
  let categoryFilter = 'all';
  const initialPlantLimit = 24;

  const esc = v => String(v ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#039;');
  const normalize = v => String(v ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').replace(/\s+/g,' ').trim();
  const allText = v => Array.isArray(v) ? v.map(allText).join(' ') : (v && typeof v === 'object' ? Object.values(v).map(allText).join(' ') : String(v ?? ''));
  const identity = p => p?.identity || {};
  const name = p => identity(p).name || p?.name || '';
  const botanical = p => identity(p).botanical_name || '';
  const family = p => identity(p).family || '';
  const sanskrit = p => identity(p).sanskrit_name || '';
  const english = p => identity(p).english_name || '';
  const category = p => p?.category === 'Supplementary' ? 'Supplementary' : 'NCISM-97';
  const order = p => Number.isFinite(Number(p?.order)) ? Number(p.order) : 9999;
  const image = p => (p?.images || {}).whole_plant || (p?.images || {}).habit || (p?.images || {}).leaf || '';

  function score(p, q) {
    const query = normalize(q); if (!query) return 0;
    const fields = [[name(p),1000],[sanskrit(p),900],[botanical(p),850],[english(p),800],[family(p),700],[p.id,650],[allText(p),100]];
    let s = 0;
    fields.forEach(([v,pts]) => { const x=normalize(v); if(x===query)s+=pts; else if(x.startsWith(query))s+=Math.floor(pts*.6); else if(x.includes(query))s+=Math.floor(pts*.45); });
    return s;
  }

  function searchPlants(q) {
    let list = masterPlants.filter(p => categoryFilter === 'all' || category(p) === categoryFilter);
    if (!normalize(q)) return [...list];
    return list.map(p=>({p,s:score(p,q)})).filter(x=>x.s>0).sort((a,b)=>b.s-a.s || order(a.p)-order(b.p)).map(x=>x.p);
  }

  function card(p) {
    const img=image(p), c=category(p), n=name(p), id=String(p.id||'');
    return `<article class="plant-card"><div class="plant-image">${img?`<img src="${esc(img)}" alt="${esc(n)}" loading="lazy" data-fallback="true"><div class="plant-placeholder" hidden>🌿</div>`:'<div class="plant-placeholder">🌿</div>'}</div><div class="plant-card-content"><div class="plant-card-top"><span class="plant-number">${c==='NCISM-97'?'#'+order(p):'Supplementary'}</span><span class="syllabus-marker">${c}</span></div><h3>${esc(n)}</h3>${sanskrit(p)?`<p class="plant-sanskrit">${esc(sanskrit(p))}</p>`:''}${botanical(p)?`<p class="plant-botanical"><em>${esc(botanical(p))}</em></p>`:''}${english(p)?`<p class="plant-english">${esc(english(p))}</p>`:''}${family(p)?`<p class="plant-family"><strong>Family:</strong> ${esc(family(p))}</p>`:''}<a class="view-plant" href="./plant.html?id=${encodeURIComponent(id)}">View Plant →</a></div></article>`;
  }

  function render(q='') {
    const results=searchPlants(q);
    const info=document.getElementById('search-result-info');
    if(info) info.textContent=q ? `${results.length} result${results.length===1?'':'s'} found for “${q}”` : `${results.length} ${categoryFilter==='all'?'total records':categoryFilter+' records'}`;
    if(!results.length){plantList.innerHTML='<div class="no-results"><div style="font-size:3rem">🔎</div><h3>No plants found</h3><p>Try another name, Sanskrit name, botanical name, family, formulation or therapeutic term.</p></div>';return;}
    const visible=q||showAllPlants?results:results.slice(0,initialPlantLimit);
    plantList.innerHTML=visible.map(card).join('')+(!q&&!showAllPlants&&results.length>initialPlantLimit?`<div class="plant-list-actions"><p>Showing ${initialPlantLimit} of ${results.length} records.</p><button type="button" id="show-all-plants">Show all ${results.length}</button></div>`:'');
    plantList.querySelectorAll('img[data-fallback="true"]').forEach(img=>img.addEventListener('error',()=>{img.hidden=true;if(img.nextElementSibling)img.nextElementSibling.hidden=false},{once:true}));
    document.getElementById('show-all-plants')?.addEventListener('click',()=>{showAllPlants=true;render(searchInput?.value||'');});
  }

  function renderControls(){
    const panel=document.querySelector('.search-panel'); if(!panel || document.getElementById('categoryFilter')) return;
    const wrap=document.createElement('div'); wrap.style='display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 4px';
    wrap.innerHTML=`<button type="button" id="categoryFilter" data-value="all">All records</button><button type="button" data-category="NCISM-97">Students • 97 NCISM drugs</button><button type="button" data-category="Supplementary">Teachers / Doctors / General Reference</button>`;
    panel.insertBefore(wrap, document.getElementById('plant-list'));
    wrap.querySelectorAll('button').forEach(btn=>{btn.style='border:1px solid #d8e0d9;background:#edf5ef;color:#1b4332;border-radius:9px;padding:9px 12px;font:inherit;font-weight:700;cursor:pointer';btn.addEventListener('click',()=>{categoryFilter=btn.dataset.category||'all';showAllPlants=false;wrap.querySelectorAll('button').forEach(b=>b.style.opacity='0.65');btn.style.opacity='1';render(searchInput?.value||'');});});
  }

  async function load(){
    try{
      const r=await fetch(databaseURL,{cache:'no-store',headers:{Accept:'application/json'}}); if(!r.ok)throw Error('HTTP '+r.status);
      const data=await r.json(); if(!Array.isArray(data))throw Error('plants.json must contain an array');
      masterPlants=data.filter(p=>p&&typeof p.id==='string').sort((a,b)=>order(a)-order(b)||name(a).localeCompare(name(b)));
      renderControls(); plantList.setAttribute('aria-busy','false'); render(searchInput?.value||'');
      console.log(`DravyaGuna library loaded: ${masterPlants.length} records (97 NCISM + supplementary)`);
    }catch(e){console.error(e);plantList.innerHTML=`<div class="plant-error"><h3>Unable to load the plant library</h3><p>${esc(e.message||'Please refresh the page.')}</p></div>`;}
  }

  if(searchInput) searchInput.addEventListener('input',e=>{clearTimeout(searchTimer);if(!e.target.value.trim())showAllPlants=false;searchTimer=setTimeout(()=>render(e.target.value),80);});
  load();
});
